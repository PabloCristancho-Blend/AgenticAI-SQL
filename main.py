from Functions.AWS_Bedrock import *

def run():
    # Task 0: Welcome message.
    print("¡Bienvenido al Generador de Querrys SQL con AWS Bedrock!")

    # Task x: Generate the database schema description.
    # (This part has to be done with an example)

    # Task x: User input and Bedrock response.
    user_request = input("Por favor, ingresa tu petición para generar una querry SQL: ")

    # Task x: Send AWS-Bedrock the request and get the querry.
    client, model_id = get_bedrock_client()
    querry = get_bedrock_response(client, model_id, user_request)
    
    # Task x: Procesar la solicitud.

    # ...

if __name__ == "__main__":
    run()