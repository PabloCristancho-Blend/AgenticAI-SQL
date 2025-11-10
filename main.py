#!/usr/bin/env python3
"""
Agente de Análisis de Ventas con AWS Bedrock
Versión integrada con herramientas de SQL, visualización y exportación
"""

import os
from dotenv import load_dotenv
import boto3
from botocore.exceptions import ClientError
from tools.sql_tool import SQLQueryTool
from tools.viz_tool import VisualizationTool
from tools.export_tool import ExportTool

# Colores para terminal
class Colors:
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    END = '\033[0m'
    BOLD = '\033[1m'

def get_bedrock_client():
    """Crea el cliente de AWS Bedrock"""
    load_dotenv()
    model_id = os.getenv("MODEL_ID")
    region = os.getenv("AWS_REGION", "us-east-1")
    client = boto3.client("bedrock-runtime", region_name=region)
    return client, model_id

def get_bedrock_response(client, model_id, user_input, system_context=""):
    """Envía petición a Bedrock y obtiene respuesta"""
    conversation = [
        {
            "role": "user",
            "content": [{"text": f"{system_context}\n\n{user_input}"}],
        }
    ]
    
    try:
        response = client.converse(
            modelId=model_id,
            messages=conversation,
            inferenceConfig={
                "maxTokens": 2048,
                "temperature": 0,
                "topP": 0.9
            },
        )
        return response["output"]["message"]["content"][0]["text"]
    except (ClientError, Exception) as e:
        return f"Error al invocar el modelo: {e}"

class AgenteVentas:
    """Agente inteligente de análisis de ventas"""
    
    def __init__(self):
        # Inicializar cliente de Bedrock
        self.client, self.model_id = get_bedrock_client()
        
        # Inicializar herramientas
        self.sql_tool = SQLQueryTool()
        self.viz_tool = VisualizationTool()
        self.export_tool = ExportTool()
        
        print(f"{Colors.GREEN}✓ Agente inicializado correctamente{Colors.END}")
    
    def analizar_solicitud(self, solicitud: str) -> dict:
        """Analiza qué debe hacer el agente"""
        # Palabras clave para detectar intención
        necesita_sql = any(kw in solicitud.lower() for kw in 
            ["top", "total", "suma", "cuanto", "cuantos", "vendedor", 
             "producto", "sede", "ventas", "lista", "mejor", "mayor"])
        
        necesita_grafico = any(kw in solicitud.lower() for kw in 
            ["gráfico", "grafico", "gráfica", "grafica", "visualiz", "chart"])
        
        necesita_exportar = any(kw in solicitud.lower() for kw in 
            ["archivo", "csv", "excel", "exporta", "guarda", "guardar"])
        
        return {
            "necesita_sql": necesita_sql,
            "necesita_grafico": necesita_grafico,
            "necesita_exportar": necesita_exportar,
            "formato_export": "excel" if "excel" in solicitud.lower() else "csv"
        }
    
    def generar_sql(self, solicitud: str) -> str:
        """Genera consulta SQL usando Bedrock"""
        prompt_sql = f"""Con base en la petición del usuario, genera SOLO la consulta SQL (sin explicaciones, sin markdown, sin código adicional).

{self.sql_tool.get_schema_info()}

Petición del usuario: {solicitud}

Reglas:
1. Solo consultas SELECT
2. Sin punto y coma al final
3. Sin formato markdown ni bloques de código
4. SQL directo y limpio

Responde ÚNICAMENTE con la consulta SQL:"""
        
        sql = get_bedrock_response(self.client, self.model_id, solicitud, prompt_sql)
        
        # Limpiar la respuesta
        sql = sql.strip().replace("```sql", "").replace("```", "").strip()
        if sql.endswith(";"):
            sql = sql[:-1]
        
        return sql
    
    def procesar_solicitud(self, solicitud: str):
        """Procesa una solicitud completa del usuario"""
        print(f"\n{Colors.BLUE} Analizando tu solicitud...{Colors.END}")
        
        # Analizar qué necesita hacer
        analisis = self.analizar_solicitud(solicitud)
        
        resultado_sql = None
        
        # Paso 1: Ejecutar SQL si es necesario
        if analisis["necesita_sql"]:
            print(f"{Colors.BLUE} Generando consulta SQL...{Colors.END}")
            
            sql = self.generar_sql(solicitud)
            print(f"{Colors.YELLOW}SQL: {sql}{Colors.END}")
            
            resultado_sql = self.sql_tool.execute_query(sql)
            
            if not resultado_sql["success"]:
                print(f"{Colors.RED} Error en SQL: {resultado_sql['error']}{Colors.END}")
                return
            
            df = resultado_sql["dataframe"]
            print(f"{Colors.GREEN}✓ Consulta ejecutada: {len(df)} registros encontrados{Colors.END}\n")
            
            # Mostrar resultados
            if len(df) <= 20:
                print(df.to_string(index=False))
            else:
                print(df.head(20).to_string(index=False))
                print(f"\n... (mostrando 20 de {len(df)} registros)")
        
        # Paso 2: Crear gráfico si es necesario
        if analisis["necesita_grafico"] and resultado_sql and resultado_sql["success"]:
            print(f"\n{Colors.BLUE} Generando gráfico...{Colors.END}")
            
            df = resultado_sql["dataframe"]
            filepath = self.viz_tool.create_chart(df)
            
            print(f"{Colors.GREEN}✓ Gráfico creado: {filepath}{Colors.END}")
            print(f"{Colors.YELLOW} Abre con: xdg-open {filepath}{Colors.END}")
        
        # Paso 3: Exportar si es necesario
        if analisis["necesita_exportar"] and resultado_sql and resultado_sql["success"]:
            print(f"\n{Colors.BLUE} Exportando datos...{Colors.END}")
            
            df = resultado_sql["dataframe"]
            
            if analisis["formato_export"] == "excel":
                filepath = self.export_tool.export_excel(df)
            else:
                filepath = self.export_tool.export_csv(df)
            
            print(f"{Colors.GREEN}✓ Archivo exportado: {filepath}{Colors.END}")
            print(f"{Colors.YELLOW} Abre con: libreoffice {filepath}{Colors.END}")
        
        # Si no necesita nada de lo anterior, dar respuesta general
        if not analisis["necesita_sql"]:
            print(f"\n{Colors.YELLOW} No detecté una consulta de datos específica.{Colors.END}")
            print(f"{Colors.YELLOW}Intenta preguntas como:{Colors.END}")
            print("  - Top 5 productos más vendidos")
            print("  - Ventas totales por sede con gráfico")
            print("  - Guarda las ventas por vendedor en CSV")

def print_banner():
    """Banner del sistema"""
    print(f"""
{Colors.BLUE}{Colors.BOLD}
╔════════════════════════════════════════════════════════╗
║   AGENTE DE ANÁLISIS DE VENTAS CON AWS BEDROCK         ║
╚════════════════════════════════════════════════════════╝
{Colors.END}
""")

def print_menu():
    """Muestra ejemplos de uso"""
    print(f"""
{Colors.YELLOW} Ejemplos de preguntas:{Colors.END}

{Colors.GREEN}1.{Colors.END} Top 5 productos más vendidos
{Colors.GREEN}2.{Colors.END} Vendedor con más ventas en Bogotá
{Colors.GREEN}3.{Colors.END} Ventas totales por sede con gráfico
{Colors.GREEN}4.{Colors.END} Guarda las ventas por vendedor en CSV
{Colors.GREEN}5.{Colors.END} Top 10 productos con mayor ingreso en Excel

{Colors.YELLOW}Comandos:{Colors.END} menu | salir | limpiar
""")

def main():
    """Función principal"""
    load_dotenv()
    
    print_banner()
    
    # Verificar conexión
    print(f"{Colors.BLUE} Verificando AWS Bedrock...{Colors.END}")
    try:
        agente = AgenteVentas()
    except Exception as e:
        print(f"{Colors.RED} Error: {e}{Colors.END}")
        print(f"{Colors.YELLOW} Verifica tu archivo .env con las credenciales AWS{Colors.END}")
        return
    
    print_menu()
    
    # Loop principal
    while True:
        try:
            solicitud = input(f"\n{Colors.BOLD}Tu pregunta > {Colors.END}").strip()
            
            if not solicitud:
                continue
            
            if solicitud.lower() in ['salir', 'exit', 'quit']:
                print(f"\n{Colors.YELLOW} Adios {Colors.END}\n")
                break
            
            if solicitud.lower() in ['menu', 'ayuda', 'help']:
                print_menu()
                continue
            
            if solicitud.lower() in ['limpiar', 'clear']:
                os.system('clear')
                print_banner()
                print_menu()
                continue
            
            # Procesar la solicitud
            agente.procesar_solicitud(solicitud)
            
        except KeyboardInterrupt:
            print(f"\n\n{Colors.YELLOW} Programa interrumpido{Colors.END}\n")
            break
        except Exception as e:
            print(f"{Colors.RED} Error: {e}{Colors.END}")

if __name__ == "__main__":
    main()