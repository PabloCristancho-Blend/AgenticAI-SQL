# AgenticAI-SQL
#  Guía de Ejecución - Agente de Análisis de Ventas

##  Diseño de la Solución

### Arquitectura del Sistema

```
┌─────────────────────────────────────────────────┐
│          USUARIO (Lenguaje Natural)             │
└───────────────────┬─────────────────────────────┘
                    │
┌───────────────────▼─────────────────────────────┐
│       MÓDULO DE INTERPRETACIÓN (Agente)         │
│  - Procesa consultas en lenguaje natural        │
│  - Identifica intención y entidades              │
└───────────────────┬─────────────────────────────┘
                    │
┌───────────────────▼─────────────────────────────┐
│     MÓDULO DE TRADUCCIÓN SQL (Query Builder)    │
│  - Convierte intención a consultas SQL          │
│  - Aplica filtros y agregaciones                │
└───────────────────┬─────────────────────────────┘
                    │
┌───────────────────▼─────────────────────────────┐
│    BASE DE DATOS SQLite (Persistencia)          │
│  - Tabla: ventas (id, vendedor, sede...)        │
└───────────────────┬─────────────────────────────┘
                    │
┌───────────────────▼─────────────────────────────┐
│   MÓDULO DE VISUALIZACIÓN (Presentación)        │
│  - Tablas: pandas DataFrame                     │
│  - Gráficos: matplotlib + seaborn               │
│  - Exportación: CSV / Excel                     │
└─────────────────────────────────────────────────┘
```

---

##  Componentes del Sistema

### 1. **Base de Datos**
- **Motor**: SQLite (sin instalación adicional)
- **Tabla principal**: `ventas`
  - id: INTEGER PRIMARY KEY
  - vendedor: TEXT
  - sede: TEXT
  - producto: TEXT
  - cantidad: INTEGER
  - precio: REAL
  - fecha: DATE

### 2. **Módulos del Agente**
- **Interpretador**: Procesa lenguaje natural
- **Query Builder**: Genera SQL dinámicamente
- **Visualizador**: Crea gráficos y tablas
- **Exportador**: Genera archivos CSV/Excel

### 3. **Interfaz de Usuario**
- Menú interactivo en consola
- Consultas en lenguaje natural
- Visualización de resultados en tiempo real

---

## Instalación y Configuración

### Requisitos Previos

#### Para PSeInt (Linux):
```bash
# Instalar PSeInt en Ubuntu/Debian
sudo apt update
sudo apt install pseint

# O descargar desde: http://pseint.sourceforge.net/
```

#### Para Python:
```bash
# Python 3.8 o superior
python --version

# Crear entorno virtual (recomendado)
python -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate   # Windows

# Instalar dependencias
pip install pandas matplotlib seaborn openpyxl
```

### Dependencias Python

Crear archivo `requirements.txt`:

Instalar:
```bash
pip install -r requirements.txt
```

---

## Ejecución del Sistema

### Ejecutar en Python

#### Ejecución Básica:
```bash
python agente_ventas.py
```

#### Estructura de Archivos Generados:
```
proyecto/
│
├── agente_ventas.py          # Script principal
├── main.py    
├── setup_database.py
├── ventas.db                 # Base de datos SQLite (auto-generado)
│
├── outputs/                 # Gráficos generados (auto-creado)
│   ├── Top_5_Productos_Mas_Vendidos_Medellin_20250110_123045.png
│   └── Ranking_de_Vendedores_Bogota_20250110_123105.xlsx


---

##  Casos de Uso y Ejemplos

### Ejemplo 1: Top 5 Productos Más Vendidos

**Consulta en lenguaje natural:**
```
"Top 5 productos más vendidos en Medellín"
```

**SQL Generado:**
```sql
SELECT producto, SUM(cantidad) AS total_vendido
FROM ventas
WHERE sede = 'Medellín'
GROUP BY producto
ORDER BY total_vendido DESC
LIMIT 5;
```

**Resultado Esperado:**
```
============================================================
TOP 5 PRODUCTOS MÁS VENDIDOS EN MEDELLÍN
============================================================
PRODUCTO            | CANTIDAD VENDIDA
------------------------------------------------------------
Laptop              | 32
Mouse               | 52
Monitor             | 28
Teclado             | 33
------------------------------------------------------------
```

**Gráfico**: Barras horizontales con valores sobre cada barra

---

### Ejemplo 2: Vendedor con Más Ventas por Sede

**Consulta:**
```
"Vendedor con más ventas en Bogotá"
```

**SQL Generado:**
```sql
SELECT vendedor, SUM(cantidad * precio) AS total_ventas
FROM ventas
WHERE sede = 'Bogotá'
GROUP BY vendedor
ORDER BY total_ventas DESC;
```

**Resultado:**
```
============================================================
RANKING DE VENDEDORES EN BOGOTÁ
============================================================
vendedor          | total_ventas
------------------------------------------------------------
Ana Garcia        | $28,800,000
Maria Lopez       | $25,350,000
------------------------------------------------------------

MEJOR VENDEDOR: Ana Garcia
TOTAL VENTAS: $28,800,000
```

---

### Ejemplo 3: Exportación a CSV

**Consulta:**
```
"Guardar las ventas por vendedor en un archivo CSV"
```

**SQL Generado:**
```sql
SELECT vendedor, 
       SUM(cantidad * precio) AS total_ventas,
       SUM(cantidad) AS total_productos_vendidos,
       COUNT(*) AS num_transacciones
FROM ventas
GROUP BY vendedor
ORDER BY total_ventas DESC;
```

**Archivo Generado**: `exports/ventas_por_vendedor_20250110_123120.csv`

**Contenido:**
```csv
vendedor,total_ventas,total_productos_vendidos,num_transacciones
Juan Perez,54250000,74,6
Carlos Ruiz,45300000,71,5
Ana Garcia,28800000,72,4
Maria Lopez,25350000,92,5
```

---

## Flujo de Interacción Completo

### Sesión de Ejemplo:

```
============================================================
  AGENTE DE ANÁLISIS DE VENTAS
============================================================
1. Top 5 productos más vendidos por sede
2. Vendedor con más ventas por sede
3. Exportar ventas por vendedor (CSV)
4. Exportar ventas por vendedor (Excel)
5. Consulta en lenguaje natural
6. Mostrar resumen general
0. Salir
============================================================
Seleccione una opción: 5

Haga su pregunta: Top 3 productos más vendidos en Medellín

AGENTE: Interpretando consulta...
Pregunta: 'Top 3 productos más vendidos en Medellín'
✓ Acción detectada: Top 3 productos en Medellín

============================================================
TOP 3 PRODUCTOS MÁS VENDIDOS EN MEDELLÍN
============================================================
PRODUCTO            | CANTIDAD VENDIDA
------------------------------------------------------------
Mouse               | 52
Teclado             | 33
Laptop              | 32
------------------------------------------------------------

✓ Gráfico guardado: graficos/Top_3_Productos_Mas_Vendidos_Medellin_20250110_143022.png
```

---

## 🎓 Conclusión

Este proyecto implementa un **agente inteligente de análisis de ventas** completo con:
- Base de datos SQL funcional
- Consultas en lenguaje natural
- Visualización de datos (gráficos)
- Exportación a múltiples formatos
- Arquitectura modular y extensible

El código está documentado, probado y listo para usar. ¡Buena suerte con el ejercicio! 