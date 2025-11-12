# Librerias externas:
import asyncio
from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain.agents import create_agent

# Funciones propias:
from functions.aws_langchain import get_bedrock_client

async def main():
    
    # 1. Definir configuración de servidores MCP
    client = MultiServerMCPClient({
        "db-sql-tool": {
            "transport": "stdio", # Local subprocess communication
            "command": "python",
             # Absolute path to your math_server.py file
            "args": ["./servers/db_server.py"],
        },
    })

    # 2. Obtener tools desde servidores MCP.
    tools = await client.get_tools()

    # 3. Obtener modelo LLM desde AWS Bedrock.
    llm = get_bedrock_client()

    # 3. Crear agente con modelo LLM
    agent = create_agent(
            llm,
            tools,
        )

    # 4. Llamar agente
    user_input = input("Ingrese su consulta: \n")

    response = await agent.ainvoke({
            "messages": [{"role": "user", "content": user_input}],
        })

    # 5. Imprimir resultados con base a si se usaron tools o no.
    print("Llamados a tools:")
    tool_calls = response["messages"][1].tool_calls
    if tool_calls:
        for call in tool_calls:
            print(f"- {call["name"]} con argumentos {call["args"]}")
            print("Respuesta de la tool:")
            for msg in response["messages"]:
                x = type(msg)
                if msg.type == "tool" and msg.name == call["name"]:
                    print(msg.content)
                    
            print("Respuesta final del agente:")        
            print(response["messages"][-1].content)
    else:
        print("No se usaron tools.")
        print(response["messages"][-1].content)


if __name__ == "__main__":
    asyncio.run(main())
