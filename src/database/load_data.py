from pathlib import Path
import json
import sqlite3


# Ubicación principal del proyecto
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# Carpetas y archivo de base de datos
FICHAS_DIR = BASE_DIR / "outputs" / "fichas"
DATABASE_PATH = BASE_DIR / "data" / "consultor_ia.db"


def cargar_datos():
    connection = sqlite3.connect(DATABASE_PATH)
    cursor = connection.cursor()

    # Recorrer las fichas JSON
    for ficha_path in FICHAS_DIR.glob("*.json"):

        print(f"Cargando: {ficha_path.name}")

        datos = json.loads(
            ficha_path.read_text(encoding="utf-8")
        )

        # Insertar proyecto
        cursor.execute("""
            INSERT OR IGNORE INTO proyectos (
                codigo_proyecto,
                nombre_proyecto,
                empresa,
                sector,
                objetivo_general,
                problema_identificado,
                conclusiones,
                fuente
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            datos["codigo_proyecto"],
            datos["nombre_proyecto"],
            datos["empresa"],
            datos["sector"],
            datos["objetivo_general"],
            datos["problema_identificado"],
            datos["conclusiones"],
            datos["fuente"]
        ))

        # Obtener ID del proyecto
        cursor.execute("""
            SELECT id
            FROM proyectos
            WHERE codigo_proyecto = ?
        """, (datos["codigo_proyecto"],))

        proyecto_id = cursor.fetchone()[0]

        # Insertar resultados
        for resultado in datos["resultados_principales"]:
            cursor.execute("""
                INSERT INTO resultados (
                    proyecto_id,
                    resultado
                )
                VALUES (?, ?)
            """, (proyecto_id, resultado))

        # Insertar indicadores
        for indicador in datos["indicadores"]:
            cursor.execute("""
                INSERT INTO indicadores (
                    proyecto_id,
                    indicador
                )
                VALUES (?, ?)
            """, (proyecto_id, indicador))

        # Insertar objetivos pendientes
        for objetivo in datos["objetivos_pendientes"]:
            cursor.execute("""
                INSERT INTO objetivos_pendientes (
                    proyecto_id,
                    objetivo
                )
                VALUES (?, ?)
            """, (proyecto_id, objetivo))

    connection.commit()
    connection.close()

    print("Datos cargados correctamente.")


if __name__ == "__main__":
    cargar_datos()