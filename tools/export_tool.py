import pandas as pd
from pathlib import Path
from datetime import datetime

class ExportTool:
    """Herramienta para exportar archivos."""
    
    def __init__(self, output_dir: str = "outputs"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    def export_csv(self, df: pd.DataFrame, name: str = None) -> str:
        """Exporta a CSV."""
        try:
            if not name:
                name = f"export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
            elif not name.endswith('.csv'):
                name += '.csv'
            
            filepath = self.output_dir / name
            df.to_csv(filepath, index=False, encoding='utf-8-sig')
            return str(filepath)
        except Exception as e:
            return f"Error: {e}"
    
    def export_excel(self, df: pd.DataFrame, name: str = None) -> str:
        """Exporta a Excel."""
        try:
            if not name:
                name = f"export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
            elif not name.endswith('.xlsx'):
                name += '.xlsx'
            
            filepath = self.output_dir / name
            df.to_excel(filepath, index=False, engine='openpyxl')
            return str(filepath)
        except Exception as e:
            return f"Error: {e}"