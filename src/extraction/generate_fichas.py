from pathlib import Path
import json
import os

from dotenv import load_dotenv
from google import genai

from src.schemas.project_schema import ProjectFicha


# Ubicación principal del proyecto
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# Cargar variables del archivo .env
load_dotenv(BASE_DIR / ".env")

# Verificar que exista la API Key
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError(
        "No se encontró GEMINI_API_KEY en el archivo .env"
    )

# Cliente de Gemini
client = genai.Client(api_key=api_key)

# Carpetas
PROCESSED_DIR = BASE_DIR / "data" / "processed"
OUTPUT_DIR = BASE_DIR / "outputs" / "fichas"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def generar_ficha(texto: str) -> ProjectFicha:

    prompt = f"""
Analiza el siguiente informe de cierre de proyecto.

Extrae únicamente información que aparezca explícitamente
en el documento. No inventes datos.

Debes devolver una ficha estructurada con:

- codigo_proyecto
- nombre_proyecto
- empresa
- sector
- objetivo_general
- problema_identificado
- resultados_principales
- indicadores
- objetivos_pendientes
- conclusiones
- fuente

IMPORTANTE:
- Si un dato no aparece en el documento, indica:
  "No especificado en el informe".
- No calcules ni inventes indicadores.
- Conserva las cifras y porcentajes exactamente como aparecen.
- No confundas resultados preliminares con resultados oficiales.
- En "fuente" indica el nombre del archivo analizado.

INFORME:

{texto}
"""

    response = client.models.generate_content(
        model="gemini-3.5-flash-lite",
        contents=prompt,
        config={
            "response_mime_type": "application/json",
            "response_schema": ProjectFicha,
        },
    )

    datos = json.loads(response.text)

    return ProjectFicha.model_validate(datos)


# Procesar todos los TXT
for txt_path in PROCESSED_DIR.glob("*.txt"):

    print(f"Generando ficha: {txt_path.name}")

    texto = txt_path.read_text(encoding="utf-8")

    ficha = generar_ficha(texto)

    output_path = OUTPUT_DIR / f"{txt_path.stem}.json"

    output_path.write_text(
        json.dumps(
            ficha.model_dump(),
            ensure_ascii=False,
            indent=4
        ),
        encoding="utf-8"
    )

    print(f"Ficha guardada: {output_path.name}")


print("Generación de fichas terminada.")