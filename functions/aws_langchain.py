import os
from dotenv import load_dotenv
import boto3
from botocore.exceptions import ClientError

from langchain_aws import ChatBedrock
from dotenv import load_dotenv

def get_bedrock_client():
    load_dotenv()

    model_id = os.getenv("MODEL_ID")
    region = os.getenv("AWS_REGION", "us-east-1")

    llm = ChatBedrock(
        model_id=model_id,  # Ajusta al modelo habilitado en tu cuenta
        region_name=region,                             # Tu región de Bedrock
    )

    return llm