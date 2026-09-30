from pathlib import Path
import os

from dotenv import load_dotenv
from google import genai

from src.tools.document_search import buscar_en_documentos
from src.tools.sql_query import consultar_sql


BASE_DIR = Path(__file__).resolve().parent.parent.parent

load_dotenv(BASE_DIR / ".env")

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError(
        "No se encontró GEMINI_API_KEY en el archivo .env"
    )

client = genai.Client(api_key=api_key)


def decidir_herramienta(pregunta: str) -> str:

    prompt = f"""
Eres un agente que consulta informes de cierre de proyectos.

Debes elegir UNA herramienta:

DOCUMENTO:
Utiliza DOCUMENTO cuando la pregunta solicite información
específica contenida dentro de los informes.

Ejemplos:
- ¿Cuál fue el OEE de la Línea 1?
- ¿Qué problema tenía la Clínica Santa Lucía?
- ¿Qué objetivos quedaron pendientes?
- ¿Cuál fue el porcentaje de abandono?
- ¿Qué indicadores tuvo Plásticos del Pacífico?

SQL:
Utiliza SQL únicamente cuando la pregunta solicite
información estructurada de la base de datos.

Ejemplos:
- ¿Qué proyectos existen?
- ¿Qué empresas aparecen?
- ¿Qué sectores tienen los proyectos?
- Lista todos los proyectos.

REGLA:
Si la pregunta pide un indicador, resultado, problema,
conclusión u objetivo específico de un proyecto,
elige DOCUMENTO.

Pregunta:
{pregunta}

Responde únicamente:
documento
o
sql
"""

    response = client.models.generate_content(
        model="gemini-3.5-flash-lite",
        contents=prompt
    )

    herramienta = response.text.strip().lower()

    if herramienta == "sql":
        return "sql"

    return "documento"


def generar_busqueda_documento(pregunta: str) -> str:

    prompt = f"""
Analiza esta pregunta sobre informes de proyectos.

Extrae únicamente las palabras o frases más importantes
para localizar la información solicitada dentro de los
documentos.

No respondas la pregunta.

El resultado debe ser una búsqueda corta de máximo
6 términos importantes.

Conserva nombres de empresas, proyectos, indicadores,
líneas productivas y conceptos específicos.

No incluyas palabras generales como:
cuál, fue, qué, del, de, la, el, los, las.

Pregunta:
{pregunta}

Devuelve únicamente los términos de búsqueda separados
por espacios.
"""

    response = client.models.generate_content(
        model="gemini-3.5-flash-lite",
        contents=prompt
    )

    return response.text.strip()


def generar_respuesta_documento(
    pregunta: str,
    resultados: list
) -> str:

    contexto = ""

    for resultado in resultados:
        contexto += f"""
FUENTE: {resultado["fuente"]}

CONTENIDO:
{resultado["fragmento"]}

----------------------------------------
"""

    prompt = f"""
Responde la pregunta utilizando ÚNICAMENTE la información
contenida en los fragmentos de los informes proporcionados.

No inventes información.

Si la información necesaria no aparece claramente,
indica que no está especificada en los fragmentos.

Pregunta:
{pregunta}

Fragmentos encontrados:

{contexto}

Responde de forma clara y directa en español.
Si la pregunta solicita un porcentaje, cifra, indicador
o resultado, menciona exactamente el valor que aparece
en el informe.

No agregues información externa.
"""

    response = client.models.generate_content(
        model="gemini-3.5-flash-lite",
        contents=prompt
    )

    return response.text.strip()


def generar_respuesta_sql(
    pregunta: str,
    resultados: list
) -> str:

    prompt = f"""
Responde la pregunta utilizando ÚNICAMENTE los resultados
obtenidos de la base de datos.

No inventes información.

Pregunta:
{pregunta}

Resultados de la base de datos:
{resultados}

Responde de forma clara y directa en español.
"""

    response = client.models.generate_content(
        model="gemini-3.5-flash-lite",
        contents=prompt
    )

    return response.text.strip()


def ejecutar_agente(pregunta: str):

    herramienta = decidir_herramienta(pregunta)

    if herramienta == "documento":

        consulta = generar_busqueda_documento(pregunta)

        resultados = buscar_en_documentos(consulta)

        if not resultados:
            return {
                "respuesta": "No se encontró información suficiente en los documentos.",
                "herramienta": "documento",
                "fuente": "No encontrada"
            }

        respuesta = generar_respuesta_documento(
            pregunta,
            resultados
        )

        return {
            "respuesta": respuesta,
            "herramienta": "documento",
            "fuente": resultados[0]["fuente"]
        }

    prompt_sql = f"""
Convierte la siguiente pregunta en una consulta SQL SELECT.

Base de datos SQLite del proyecto.

Tablas disponibles:

proyectos:
id,
codigo_proyecto,
nombre_proyecto,
empresa,
sector,
objetivo_general,
problema_identificado,
conclusiones,
fuente

resultados:
id,
proyecto_id,
resultado

indicadores:
id,
proyecto_id,
indicador

objetivos_pendientes:
id,
proyecto_id,
objetivo

Reglas:

- Utiliza JOIN cuando sea necesario.
- Para identificar un proyecto utiliza codigo_proyecto,
  empresa o nombre_proyecto.
- No inventes nombres de proyectos.
- Solo genera SELECT.
- No utilices INSERT.
- No utilices UPDATE.
- No utilices DELETE.
- No utilices DROP.
- No utilices ALTER.

Pregunta:
{pregunta}

Devuelve únicamente la consulta SQL.
"""

    response = client.models.generate_content(
        model="gemini-3.5-flash-lite",
        contents=prompt_sql
    )

    consulta_sql = response.text.strip()

    consulta_sql = consulta_sql.replace("```sql", "")
    consulta_sql = consulta_sql.replace("```", "")
    consulta_sql = consulta_sql.strip()

    resultados = consultar_sql(consulta_sql)

    if not resultados:
        return {
            "respuesta": "No se encontraron resultados en la base de datos.",
            "herramienta": "sql",
            "fuente": "Base de datos SQLite"
        }

    respuesta = generar_respuesta_sql(
        pregunta,
        resultados
    )

    return {
        "respuesta": respuesta,
        "herramienta": "sql",
        "fuente": "Base de datos SQLite",
        "consulta": consulta_sql
    }


if __name__ == "__main__":

    print("CONSULTOR IA")
    print("Escribe una pregunta sobre los proyectos.")
    print("Escribe 'salir' para terminar.")
    print()

    while True:

        pregunta = input("Pregunta: ")

        if pregunta.lower().strip() == "salir":
            break

        try:

            respuesta = ejecutar_agente(pregunta)

            print("\nRespuesta:")
            print(respuesta["respuesta"])

            print(f"\nHerramienta utilizada: {respuesta['herramienta']}")
            print(f"Fuente: {respuesta['fuente']}")

            if "consulta" in respuesta:
                print(f"Consulta SQL: {respuesta['consulta']}")

            print("\n" + "=" * 80 + "\n")

        except Exception as error:

            print(f"\nError: {error}\n")