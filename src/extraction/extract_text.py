from pathlib import Path
import fitz

# Ubicación principal del proyecto
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# Carpetas de entrada y salida
RAW_DIR = BASE_DIR / "data" / "raw"
PROCESSED_DIR = BASE_DIR / "data" / "processed"

# Crear processed si no existe
PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

# Recorrer los PDF de data/raw
for pdf_path in RAW_DIR.glob("*.pdf"):

    # No procesar el PDF de instrucciones
    if "Prueba_Tecnica_Consultor_IA" in pdf_path.name:
        continue

    print(f"Procesando: {pdf_path.name}")

    # Abrir PDF
    doc = fitz.open(pdf_path)

    # Extraer texto de todas las páginas
    text = ""

    for page in doc:
        text += page.get_text()

    # Crear nombre del archivo .txt
    output_path = PROCESSED_DIR / f"{pdf_path.stem}.txt"

    # Guardar texto
    output_path.write_text(text, encoding="utf-8")

    print(f"Guardado: {output_path.name}")

print("Extracción terminada.")