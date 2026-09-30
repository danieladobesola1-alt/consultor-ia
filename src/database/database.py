from pathlib import Path
import sqlite3


# Ubicación principal del proyecto
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# Ubicación de la base de datos
DATABASE_DIR = BASE_DIR / "data"
DATABASE_PATH = DATABASE_DIR / "consultor_ia.db"

# Crear carpeta data si no existe
DATABASE_DIR.mkdir(parents=True, exist_ok=True)


def get_connection():
    """
    Crea y devuelve una conexión a la base de datos.
    """
    return sqlite3.connect(DATABASE_PATH)


def create_database():
    """
    Crea las tablas necesarias para almacenar
    la información de los proyectos.
    """

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS proyectos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            codigo_proyecto TEXT NOT NULL UNIQUE,
            nombre_proyecto TEXT NOT NULL,
            empresa TEXT NOT NULL,
            sector TEXT NOT NULL,
            objetivo_general TEXT,
            problema_identificado TEXT,
            conclusiones TEXT,
            fuente TEXT
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS resultados (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            proyecto_id INTEGER NOT NULL,
            resultado TEXT NOT NULL,
            FOREIGN KEY (proyecto_id) REFERENCES proyectos(id)
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS indicadores (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            proyecto_id INTEGER NOT NULL,
            indicador TEXT NOT NULL,
            FOREIGN KEY (proyecto_id) REFERENCES proyectos(id)
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS objetivos_pendientes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            proyecto_id INTEGER NOT NULL,
            objetivo TEXT NOT NULL,
            FOREIGN KEY (proyecto_id) REFERENCES proyectos(id)
        )
    """)

    connection.commit()
    connection.close()


if __name__ == "__main__":
    create_database()
    print("Base de datos creada correctamente.")