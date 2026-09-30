from pathlib import Path
import sqlite3


# Ubicación principal del proyecto
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# Base de datos
DATABASE_PATH = BASE_DIR / "data" / "consultor_ia.db"


def consultar_sql(consulta: str):
    """
    Ejecuta una consulta SQL de lectura sobre la base de datos.

    Solo permite consultas SELECT para evitar modificar
    o eliminar información de la base de datos.
    """

    consulta = consulta.strip()

    if not consulta.lower().startswith("select"):
        raise ValueError(
            "Solo se permiten consultas SQL de tipo SELECT."
        )

    connection = sqlite3.connect(DATABASE_PATH)
    connection.row_factory = sqlite3.Row

    cursor = connection.cursor()

    cursor.execute(consulta)

    filas = cursor.fetchall()

    resultados = [dict(fila) for fila in filas]

    connection.close()

    return resultados


if __name__ == "__main__":

    print("Herramienta de consulta SQL")
    print("Ejemplo:")
    print("SELECT codigo_proyecto, empresa, sector FROM proyectos;")
    print()

    consulta = input("Escribe la consulta SQL: ")

    try:
        resultados = consultar_sql(consulta)

        if not resultados:
            print("\nNo se encontraron resultados.")
        else:
            print(f"\nSe encontraron {len(resultados)} resultado(s):\n")

            for resultado in resultados:
                print(resultado)

    except Exception as error:
        print(f"\nError: {error}")