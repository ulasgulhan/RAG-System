from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document


def split_text(documents: list[Document], chunk_size=300, chunk_overlap=100) -> list:
    """
    Split documents into smaller chunks.

    Parameters:
    documents (list): A list of Document objects to be split.
    chunk_size (int): The maximum size of each chunk. Default is 300.
    chunk_overlap (int): The overlap size between consecutive chunks. Default is 100.

    Returns:
    list: A list of chunks obtained by splitting the documents.
    """
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        length_function=len,
        add_start_index=True,
    )
    chunks = text_splitter.split_documents(documents)
    print(f"Split {len(documents)} documents into {len(chunks)} chunks.")
    return chunks
