from Functions.AWS_Bedrock import *
from Functions.AWS_LangChain import *

def run():
    # Task 0: Welcome message.
    print("¡Bienvenido al Generador de Querrys SQL con AWS Bedrock!")

    # Task x: Generate the database schema description.
    # (This part has to be done with an example)

    # Task x: User input and Bedrock response.
    user_request = input("Por favor, ingresa tu petición para generar una querry SQL: ")

    # Task x: Send AWS-Bedrock the request and get the querry.
    #   LLM - AWS Bedrock con LangChain
    llm = get_bedrock_client()
    expert_prompt = get_bedrock_prompt()
    querry = get_bedrock_response(llm, user_request, expert_prompt)
    print("\nQuerry SQL generada:")
    print(querry)


    # Task x: Procesar la solicitud.

    # ...

if __name__ == "__main__":
    run()