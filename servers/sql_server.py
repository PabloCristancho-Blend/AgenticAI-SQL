from datetime import datetime, timezone
from mcp.server.fastmcp import FastMCP
import sqlite3
import pandas as pd
import json
from pathlib import Path

mcp = FastMCP("sales-db-server")

# Ruta a tu base de datos
DB_PATH = "/home/juanacosta/Documentos/GitHub/AgenticAI-SQL/src/ventas.db"

def get_db_connection():
    """Establece conexión con la base de datos"""
    return sqlite3.connect(DB_PATH)

@mcp.tool()
def consultar_ventas(pregunta_sql: str) -> str:
    try:
        # Validación básica de seguridad
        if not pregunta_sql.strip().upper().startswith('SELECT'):
            return json.dumps({
                "error": "Solo se permiten consultas SELECT por seguridad"
            })
        
        conn = get_db_connection()
        df = pd.read_sql_query(pregunta_sql, conn)
        conn.close()
        
        # Convertir a formato JSON legible
        resultado = {
            "filas": len(df),
            "columnas": df.columns.tolist(),
            "datos": df.to_dict(orient='records')
        }
        
        return json.dumps(resultado, indent=2, ensure_ascii=False)
    
    except Exception as e:
        return json.dumps({"error": str(e)})

@mcp.tool()
def obtener_esquema_db() -> str:
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Obtener lista de tablas
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tablas = cursor.fetchall()
        
        esquema = {}
        for tabla in tablas:
            nombre_tabla = tabla[0]
            cursor.execute(f"PRAGMA table_info({nombre_tabla});")
            columnas = cursor.fetchall()
            esquema[nombre_tabla] = [
                {"nombre": col[1], "tipo": col[2], "no_nulo": col[3], "pk": col[5]}
                for col in columnas
            ]
        
        conn.close()
        return json.dumps(esquema, indent=2, ensure_ascii=False)
    
    except Exception as e:
        return json.dumps({"error": str(e)})

@mcp.tool()
def estadisticas_ventas() -> str:
    try:
        conn = get_db_connection()
        
        # Ajusta estas consultas según tu esquema real
        queries = {
            "total_ventas": "SELECT COUNT(*) as total FROM ventas",
            "monto_total": "SELECT SUM(monto) as total FROM ventas",
            "promedio": "SELECT AVG(monto) as promedio FROM ventas"
        }
        
        resultados = {}
        for key, query in queries.items():
            try:
                df = pd.read_sql_query(query, conn)
                resultados[key] = df.to_dict(orient='records')[0]
            except:
                resultados[key] = "No disponible (ajustar consulta según esquema)"
        
        conn.close()
        return json.dumps(resultados, indent=2, ensure_ascii=False)
    
    except Exception as e:
        return json.dumps({"error": str(e)})

@mcp.tool()
def exportar_csv(consulta_sql: str, nombre_archivo: str = "export.csv") -> str:
    try:
        if not consulta_sql.strip().upper().startswith('SELECT'):
            return json.dumps({
                "error": "Solo se permiten consultas SELECT"
            })
        
        conn = get_db_connection()
        df = pd.read_sql_query(consulta_sql, conn)
        conn.close()
        
        # Guardar en la carpeta src
        output_path = Path("/home/juanacosta/Documentos/GitHub/AgenticAI-SQL/src") / nombre_archivo
        df.to_csv(output_path, index=False, encoding='utf-8')
        
        return json.dumps({
            "exito": True,
            "archivo": str(output_path),
            "filas_exportadas": len(df)
        }, ensure_ascii=False)
    
    except Exception as e:
        return json.dumps({"error": str(e)})

if __name__ == "__main__":
    # Comunicación local mediante stdio
    mcp.run(transport="stdio")