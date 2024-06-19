from io import BytesIO
from langchain_community.vectorstores import Chroma
from dotenv import load_dotenv
import os
import boto3
from langchain_cohere import CohereEmbeddings
import pyarrow as pa
import pyarrow.parquet as pq
from langchain_core.documents import Document

load_dotenv()

COHERE_API_KEY = os.getenv("COHERE_API_KEY")


class Aws_S3:
    def __init__(self):
        self.bucket = os.getenv("BUCKET_NAME")
        self.s3_client = boto3.client("s3")
        self.cohere_embeddings = CohereEmbeddings(
            cohere_api_key=COHERE_API_KEY, model="embed-multilingual-v3.0"
        )
        self.db = Chroma(
            collection_name="docs_store", embedding_function=self.cohere_embeddings
        )
        self.prefix = None

    def upload_content_to_s3_parquet(self, content_df, object_name):
        """
        Uploads a Pandas DataFrame in Parquet format to the specified S3 bucket.

        Parameters:
        content_df (pandas.DataFrame): The DataFrame to upload.
        object_name (str): The name of the object to be created in the S3 bucket.
        """
        try:
            table = pa.Table.from_pandas(content_df)

            out_buffer = BytesIO()
            pq.write_table(table, out_buffer)
            out_buffer.seek(0)

            self.s3_client.upload_fileobj(out_buffer, self.bucket, object_name)
            print(f"Uploaded Parquet file {object_name} to S3 bucket {self.bucket}")

        except Exception as e:
            print(f"Error uploading Parquet content: {e}")
            return False
        return True

    def load_documents_from_s3(self, prefix):
        """
        Loads documents from the specified S3 bucket based on a given prefix.

        Parameters:
        prefix (str): The prefix to filter objects in the S3 bucket.

        Returns:
        list: A list of Document objects loaded from the S3 bucket.
        """

        s3_client = self.s3_client
        bucket = self.bucket

        documents = []
        try:
            # List objects in the S3 bucket with the specified prefix
            response = s3_client.list_objects_v2(Bucket=bucket, Prefix=prefix)

            for obj in response.get("Contents", []):

                # Retrieve each object from the S3 bucket
                file_obj = s3_client.get_object(Bucket=bucket, Key=obj["Key"])
                content_type = file_obj.get("ContentType", "").lower()

                if content_type == "binary/octet-stream":
                    parquet_bytes = file_obj["Body"].read()

                    try:
                        parquet_file = pq.ParquetFile(BytesIO(parquet_bytes))
                        df = parquet_file.read_row_group(0).to_pandas()

                        page_content = df["page_content"].iloc[0]

                        document = Document(
                            page_content=page_content, metadata={"source": obj["Key"]}
                        )
                        documents.append(document)

                    except Exception as e:
                        print(f"Error processing Parquet file {obj['Key']}: {e}")
                        continue

                else:
                    # Process other file types as plain text
                    page_content = file_obj["Body"].read().decode("utf-8")
                    document = Document(
                        page_content=page_content, metadata={"source": obj["Key"]}
                    )
                    documents.append(document)

        except Exception as e:
            print(f"Error loading documents from S3: {e}")

        return documents
