import os
from dotenv import load_dotenv
import boto3
from botocore.exceptions import ClientError

def get_bedrock_client():
    """Crea el cliente de AWS Bedrock"""
    # Load the environment variables in the actual process (like credentials of AWS etc.) (.env):
    load_dotenv()

    # Bring and Store some necesary variables.
    model_id = os.getenv("MODEL_ID")
    region = os.getenv("AWS_REGION", "us-east-1") # If it doesn't find the environment variable for the region, it takes by default "us-esast-1"

    # Create a Bedrock Runtime client in the selected AWS Region.
    client = boto3.client("bedrock-runtime", region_name=region) # Each region has different models available.
    
    # Return the client, and the model_id.
    return client, model_id

def get_bedrock_response(client, model_id, user_input):
    """
    Envía el historial de conversación al modelo de AWS Bedrock
    y devuelve la respuesta del asistente experto.
    """

    # Prompt base: comportamiento del asistente experto
    expert_prompt = (
        "Con base en la petición del usuario, proporciona una querry SQL optimizada y eficiente. "
        "Asegúrate de que la querry sea correcta y esté adaptada a la solicitud específica del usuario."
        "Solo devuelve la querry SQL sin explicaciones adicionales. (Importante seguir esta regla)."
        "Si la petición del usuario no es clara o no se puede convertir en una querry SQL válida, responde con 'No puedo generar una querry SQL para esa solicitud.'"
    )

    # Building the conversation with the system and user messages.
    conversation = [
        {
            "role": "user",
            "content": [
                {"text": f"{expert_prompt}\n\n{user_input}"}
            ],
        }
    ]

    try:
        response = client.converse(
            modelId=model_id,
            messages=conversation,
            inferenceConfig={
                "maxTokens": 2048,
                "temperature": 0,
                "topP": 0.9},
        )

        response_text = response["output"]["message"]["content"][0]["text"]
        return response_text

    except (ClientError, Exception) as e:
        return f"Error al invocar el modelo: {e}"