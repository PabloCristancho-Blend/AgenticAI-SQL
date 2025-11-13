# Librerias externas:
import asyncio
import os
from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain.agents import create_agent

# Funciones propias:
from functions.aws_langchain import get_bedrock_client

async def ejecutar_agente(agent):
    """Ejecuta el agente según la consulta del usuario"""
    user_input = input("\n Ingrese su consulta: ")
    if not user_input.strip():
        print(" Entrada vacía. Intenta nuevamente.")
        return

    response = await agent.ainvoke({
        "messages": [{"role": "user", "content": user_input}],
    })

    print("\n🔍 Llamados a tools:")
    tool_calls = response["messages"][1].tool_calls

    if tool_calls:
        for call in tool_calls:
            print(f"- {call['name']} con argumentos {call['args']}")
            print(" Respuesta de la tool:")
            for msg in response["messages"]:
                if msg.type == "tool" and msg.name == call["name"]:
                    print(msg.content)
        print("\n Respuesta final del agente:")        
        print(response["messages"][-1].content)
    else:
        print(" No se usaron tools.")
        print(response["messages"][-1].content)


async def main():
    # 1. Definir configuración de servidores MCP
    client = MultiServerMCPClient({
        "db-sql-tool": {
            "transport": "stdio",
            "command": "python",
            "args": ["./servers/db_server.py"],
        },
    })

    # 2. Obtener tools desde servidores MCP
    tools = await client.get_tools()

    # 3. Obtener modelo LLM desde AWS Bedrock
    llm = get_bedrock_client()

    # 4. Crear agente
    agent = create_agent(llm, tools)

    # 5. Interfaz de menú
    while True:
        print("\n" + "="*50)
        print(" MENÚ DE OPCIONES")
        print("="*50)
        print("opción 1: Ejecutar consulta al agente")
        print("opción 2: Limpiar pantalla")
        print("opción 3: Salir\n")

        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            await ejecutar_agente(agent)
        elif opcion == "2":
            os.system("cls" if os.name == "nt" else "clear")
        elif opcion == "3":
            print(" Saliendo del programa...")
            break
        else:
            print(" Opción no válida. Intente nuevamente.")

if __name__ == "__main__":
    asyncio.run(main())