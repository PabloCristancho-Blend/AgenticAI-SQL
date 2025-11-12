from datetime import datetime, timezone
from mcp.server.fastmcp import FastMCP
import sqlite3
import pandas as pd
import json
from pathlib import Path
import matplotlib.pyplot as plt
import os

mcp = FastMCP("sales-db-server")

DB_PATH = "./src/ventas.db"

def get_db_connection():
    """Establece conexión con la base de datos"""
    return sqlite3.connect(DB_PATH)


@mcp.tool()
def get_ventas_ventas(top:int) -> str:
    """Devuelve todas las ventas en formato JSON."""
    query = f"SELECT * FROM ventas LIMIT {top};"
    try:
        conn = get_db_connection()
        df = pd.read_sql_query(query, conn)
        conn.close() 
        df.to_json("./temp/registro-temp.json", orient="records", indent=2, force_ascii=False)
        registros = df.to_json(orient="records", indent=2, force_ascii=False)
        return registros
        
    except Exception as e:
        return json.dumps({"error": str(e), "query": query})

@mcp.tool()
def get_ventas_mes(mes: str) -> str:
    """Devuelve el resultado de una consulta generada automáticamente a partir de una pregunta natural."""
    query = "SELECT * FROM ventas WHERE fecha LIKE '%" + mes + "%';"
    
    try:
        conn = get_db_connection()
        df = pd.read_sql_query(query, conn)
        conn.close()
        return df.to_json(orient="records", indent=2, force_ascii=False)
    except Exception as e:
        return json.dumps({"error": str(e), "query": query})
    
@mcp.tool()
def get_ventas_sede(sede: str) -> str:
    """Devuelve el resultado de una consulta generada automáticamente a partir de una pregunta natural."""
    query = "SELECT * FROM ventas WHERE sede = '" + sede + "';"
    
    try:
        conn = get_db_connection()
        df = pd.read_sql_query(query, conn)
        conn.close()
        return df.to_json(orient="records", indent=2, force_ascii=False)
    except Exception as e:
        return json.dumps({"error": str(e), "query": query})

@mcp.tool()
def get_ventas_vendedor(vendedor: str) -> str:
    """Devuelve el resultado de una consulta generada automáticamente a partir de una pregunta natural."""
    query = "SELECT * FROM ventas WHERE vendedor = '" + vendedor + "';"
    try:
        conn = get_db_connection()
        df = pd.read_sql_query(query, conn)
        conn.close()
        registros = df.to_json(orient="records", indent=2, force_ascii=False)

        # Crear archivo temporal
        df.to_json("registro-temp.json", orient="records", indent=2, force_ascii=False)

        return registros
    except Exception as e:
        return json.dumps({"error": str(e), "query": query})
    
@mcp.tool()
def exportar_csv():
    nombre_json = "./temp/registro-temp.json"
    """
    Lee un archivo JSON de ventas y lo convierte a CSV.
    Guarda el CSV con el mismo nombre que el JSON, cambiando la extensión.
    """
    try:
        # Verificar que el archivo JSON exista
        if not os.path.exists(nombre_json):
            return json.dumps({"error": f"El archivo {nombre_json} no existe."})

        # Leer el archivo JSON con pandas
        df = pd.read_json(nombre_json)

        # Crear nombre del CSV con la misma base del JSON
        base_nombre = os.path.splitext(nombre_json)[0]  # quita la extensión .json
        nombre_csv = base_nombre + ".csv"

        # Exportar a CSV
        df.to_csv(nombre_csv, index=False)

        print(f"✅ Archivo CSV generado en: {os.path.abspath(nombre_csv)}")
        return nombre_csv

    except Exception as e:
        return json.dumps({"error": str(e), "archivo": nombre_json})

    # @mcp.tool()
    # def graficar_ventas(consulta_sql: str, columna_x: str, columna_y: str, nombre_archivo: str = "grafico_ventas.png") -> str:
    #     """
    #     Genera un gráfico de barras a partir de una consulta SQL SELECT.
    #     Ejemplo de uso:
    #       graficar_ventas("SELECT producto, SUM(monto) as total FROM ventas GROUP BY producto", "producto", "total")
    #     """
    #     try:
    #         # Validar que sea SELECT
    #         if not consulta_sql.strip().upper().startswith("SELECT"):
    #             return json.dumps({"error": "Solo se permiten consultas SELECT."})
            
    #         conn = get_db_connection()
    #         df = pd.read_sql_query(consulta_sql, conn)
    #         conn.close()
            
    #         if columna_x not in df.columns or columna_y not in df.columns:
    #             return json.dumps({"error": f"Las columnas '{columna_x}' o '{columna_y}' no existen en el resultado."})
            
    #         # Crear gráfico
    #         plt.figure(figsize=(8, 5))
    #         plt.bar(df[columna_x], df[columna_y])
    #         plt.xlabel(columna_x)
    #         plt.ylabel(columna_y)
    #         plt.title("Gráfico de Ventas")
    #         plt.xticks(rotation=45, ha='right')
    #         plt.tight_layout()
            
    #         # Guardar imagen
    #         output_path = Path("/home/juanacosta/Documentos/GitHub/AgenticAI-SQL/src") / nombre_archivo
    #         plt.savefig(output_path, dpi=120)
    #         plt.close()
            
    #         return json.dumps({
    #             "exito": True,
    #             "archivo": str(output_path),
    #             "filas_graficadas": len(df)
    #         }, ensure_ascii=False)
        
    #     except Exception as e:
    #         return json.dumps({"error": str(e)})
    
if __name__ == "__main__":
    mcp.run(transport="stdio")