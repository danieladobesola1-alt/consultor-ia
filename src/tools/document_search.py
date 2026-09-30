from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent.parent
PROCESSED_DIR = BASE_DIR / "data" / "processed"


def buscar_en_documentos(consulta: str):

    resultados = []

    consulta = consulta.lower().strip()

    if not consulta:
        return resultados

    palabras = [
        palabra
        for palabra in consulta.split()
        if len(palabra) >= 3
    ]

    for archivo in PROCESSED_DIR.glob("*.txt"):

        texto = archivo.read_text(encoding="utf-8")
        texto_lower = texto.lower()

        posiciones = []

        # Encontrar TODAS las apariciones de cada término
        for palabra in palabras:

            inicio_busqueda = 0

            while True:

                posicion = texto_lower.find(
                    palabra,
                    inicio_busqueda
                )

                if posicion == -1:
                    break

                posiciones.append(
                    (posicion, palabra)
                )

                inicio_busqueda = posicion + len(palabra)

        if not posiciones:
            continue

        # Crear ventanas alrededor de cada coincidencia
        ventanas = []

        for posicion, palabra in posiciones:

            inicio = max(0, posicion - 1200)
            fin = min(len(texto), posicion + 2500)

            fragmento = texto[inicio:fin]

            fragmento_lower = fragmento.lower()

            coincidencias = 0

            for termino in palabras:

                if termino in fragmento_lower:
                    coincidencias += 1

            # Dar prioridad a secciones de resultados
            # cuando la pregunta busca indicadores o porcentajes.
            puntaje_seccion = 0

            palabras_resultados = [
                "resultados",
                "indicador",
                "resultado",
                "variación",
                "cumple meta",
                "estado"
            ]

            for palabra_resultado in palabras_resultados:

                if palabra_resultado in fragmento_lower:
                    puntaje_seccion += 3

            # Dar prioridad a fragmentos donde aparezcan
            # valores porcentuales.
            cantidad_porcentajes = fragmento.count("%")

            puntaje = (
                coincidencias * 10
                + puntaje_seccion
                + cantidad_porcentajes
            )

            ventanas.append({
                "posicion": posicion,
                "coincidencias": coincidencias,
                "puntaje": puntaje,
                "fragmento": fragmento.strip()
            })

        # Elegir la ventana más relevante
        mejor_ventana = max(
            ventanas,
            key=lambda ventana: (
                ventana["puntaje"],
                ventana["coincidencias"]
            )
        )

        resultados.append({
            "fuente": archivo.name,
            "coincidencias": mejor_ventana["coincidencias"],
            "puntaje": mejor_ventana["puntaje"],
            "fragmento": mejor_ventana["fragmento"]
        })

    resultados.sort(
        key=lambda resultado: (
            resultado["puntaje"],
            resultado["coincidencias"]
        ),
        reverse=True
    )

    return resultados


if __name__ == "__main__":

    consulta = input("Escribe qué quieres buscar: ")

    resultados = buscar_en_documentos(consulta)

    if not resultados:

        print("No se encontraron resultados.")

    else:

        print(
            f"\nSe encontraron {len(resultados)} documento(s):\n"
        )

        for resultado in resultados:

            print("=" * 80)
            print(f"FUENTE: {resultado['fuente']}")
            print(f"COINCIDENCIAS: {resultado['coincidencias']}")
            print(f"PUNTAJE: {resultado['puntaje']}")
            print("=" * 80)
            print(resultado["fragmento"])
            print()