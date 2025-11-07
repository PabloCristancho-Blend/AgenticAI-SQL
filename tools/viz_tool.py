import pandas as pd
import plotly.express as px
from pathlib import Path
from datetime import datetime

class VisualizationTool:
    """Herramienta para crear gráficos."""
    
    def __init__(self, output_dir: str = "outputs"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
    def create_chart(self, df: pd.DataFrame, chart_type: str = "bar") -> str:
        """Crea un gráfico."""
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            
            if len(df.columns) < 2:
                return "Error: Se necesitan al menos 2 columnas"
            
            x_col, y_col = df.columns[0], df.columns[1]
            
            if chart_type == "bar":
                fig = px.bar(df, x=x_col, y=y_col, title="Análisis de Ventas")
            elif chart_type == "pie":
                fig = px.pie(df, names=x_col, values=y_col, title="Distribución")
            else:
                fig = px.line(df, x=x_col, y=y_col, title="Tendencia")
            
            filename = f"chart_{timestamp}.html"
            filepath = self.output_dir / filename
            fig.write_html(str(filepath))
            
            return str(filepath)
        except Exception as e:
            return f"Error al crear gráfico: {e}"