from rest_framework import permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from .services.aws_s3 import Aws_S3
from .services.llm_agent import LlmAgent
from dotenv import load_dotenv

load_dotenv()

# Create your views here.


class LlmView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        """
        Handles POST requests to process a user query using AWS S3 and an LLM Agent.

        Parameters:
        request (Request): The request object containing user data.

        Returns:
        Response: A JSON response with the answer from the LLM.
        """

        s3_handler = Aws_S3()
        llm_handler = LlmAgent()

        chunks = s3_handler.load_documents_from_s3(prefix="chunks/")

        user_query = request.data.get("query")

        answer = llm_handler.get_relevent_data(chunks=chunks, user_query=user_query)

        return Response({"LLM's Answer": {answer}}, status=status.HTTP_200_OK)
