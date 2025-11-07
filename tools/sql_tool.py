import sqlite3
import pandas as pd
from typing import Dict, Any

class SQLQueryTool:
    """Herramienta para ejecutar consultas SQL."""
    
    def __init__(self, db_path: str = "data/ventas.db"):
        self.db_path = db_path
        
    def execute_query(self, query: str) -> Dict[str, Any]:
        """Ejecuta una consulta SQL."""
        try:
            conn = sqlite3.connect(self.db_path)
            df = pd.read_sql_query(query, conn)
            conn.close()
            
            return {
                "success": True,
                "data": df.to_dict('records'),
                "columns": df.columns.tolist(),
                "row_count": len(df),
                "dataframe": df
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "data": None
            }
    
    def get_schema_info(self) -> str:
        """Retorna información del esquema para el prompt."""
        return """
Esquema de la tabla 'ventas':
- id: INTEGER (clave primaria)
- vendedor: TEXT (nombre del vendedor)
- sede: TEXT (ciudad: Bogotá, Medellín, Cali, Barranquilla)
- producto: TEXT (nombre del producto)
- cantidad: INTEGER (cantidad vendida)
- precio: REAL (precio unitario)
- fecha: DATE (formato YYYY-MM-DD)

Ejemplos de consultas:
- Top productos: SELECT producto, SUM(cantidad) AS total FROM ventas GROUP BY producto ORDER BY total DESC LIMIT 5
- Ventas por sede: SELECT sede, SUM(cantidad*precio) AS total_ventas FROM ventas GROUP BY sede
"""