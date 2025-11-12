from datetime import datetime, timezone
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("clock-server")

@mcp.tool()
def get_time(city:str) -> str:
    """Devuelve la hora actual del sistema en ISO 8601 (UTC)"""
    now = datetime.now().astimezone() # Hora local del sistema
    return f"Hora en {city}: {now.isoformat()}"

if __name__ == "__main__":
    # Comunicación local mediante stdio
    mcp.run(transport="stdio")