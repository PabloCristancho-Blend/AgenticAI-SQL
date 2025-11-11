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

def get_bedrock_prompt():
    expert_prompt = (
        "Con base en la petición del usuario, proporciona una querry SQL optimizada y eficiente. "
        "Asegúrate de que la querry sea correcta y esté adaptada a la solicitud específica del usuario."
        "Solo devuelve la querry SQL sin explicaciones adicionales. (Importante seguir esta regla)."
        "Si la petición del usuario no es clara o no se puede convertir en una querry SQL válida, responde con 'No puedo generar una querry SQL para esa solicitud.'"
    )
    return expert_prompt

def get_bedrock_response(llm, user_input, expert_prompt):
    """
    Envía el historial de conversación al modelo de AWS Bedrock
    y devuelve la respuesta del asistente experto.
    """

    # Construcción del mensaje completo
    full_prompt = f"{expert_prompt}\n\n{user_input}"

    try:
        response = llm.invoke(full_prompt)
        print(type(response))
        return response.content.strip()

    except (ClientError, Exception) as e:
        return f"Error al invocar el modelo: {e}"