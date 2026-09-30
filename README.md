## 3. Estructura del proyecto

El proyecto está organizado separando la extracción de documentos, generación de fichas, base de datos, herramientas de consulta y agente.

## 4. Tecnologías utilizadas

- Python
- Gemini API
- Google GenAI SDK
- PyMuPDF
- Pydantic
- SQLite
- python-dotenv
- Git

## 5. Instalación y ejecución

Instalar las dependencias:

py -m pip install -r requirements.txt

Configurar la variable GEMINI_API_KEY en el archivo .env.

Para procesar los documentos:

py src\extraction\extract_text.py

Para generar las fichas estructuradas:

py -m src.extraction.generate_fichas

Para crear y cargar la base de datos:

py src\database\database.py
py src\database\load_data.py

Para ejecutar el agente:

py -m src.agent.agent

## 6. Fichas estructuradas

Las fichas contienen información de identificación y contexto de cada proyecto, incluyendo código, nombre, empresa, sector, objetivo general, problema identificado, resultados principales, indicadores, objetivos pendientes, conclusiones y fuente.

Estos campos fueron seleccionados para facilitar consultas posteriores sobre los proyectos y mantener la trazabilidad hacia los informes originales.

## 7. Base de datos

Se utiliza SQLite para almacenar las fichas estructuradas.

La elección de SQLite responde al alcance de la prueba, ya que permite realizar consultas relacionales sin necesidad de instalar o administrar un servidor de base de datos.

## 8. Herramientas del agente

La solución implementa dos herramientas principales:

1. Búsqueda documental sobre el texto procesado de los informes.
2. Consulta SQL sobre la información estructurada almacenada en SQLite.

El agente decide qué herramienta utilizar según la pregunta realizada.

## 9. Confiabilidad y trazabilidad

Las respuestas se basan en la información disponible en los informes proporcionados.

El agente muestra la herramienta utilizada y la fuente consultada.

Cuando la información solicitada no se encuentra en los documentos disponibles, el agente debe indicarlo en lugar de inventar información.

## 10. Decisiones técnicas

Gemini se utiliza para generar las fichas estructuradas y para el funcionamiento del agente.

PyMuPDF se utiliza para extraer el contenido textual de los documentos.

SQLite se utiliza para almacenar las fichas y permitir consultas SQL.

La interfaz se mantiene en consola porque el enunciado de la prueba establece que una interfaz por consola es suficiente.

## 11. Supuestos

- Los cuatro informes proporcionados son las fuentes de información de la solución.
- Los documentos utilizados en la prueba son ficticios.
- Las consultas se realizan mediante lenguaje natural.
- La información de las fichas representa los datos principales de cada proyecto.
- La fuente original se conserva para facilitar la trazabilidad.
- La ejecución se realiza localmente.

## 12. Limitaciones conocidas

- La interfaz actual es por consola.
- La calidad de la extracción depende del contenido de los documentos.
- La generación de fichas depende de la disponibilidad de la API de Gemini.
- El uso de la API puede generar costos según el modelo y el consumo.
- SQLite está orientado al volumen de información utilizado en esta prueba.
- Una implementación productiva requeriría pruebas adicionales de seguridad, carga y observabilidad.

## 13. Seguridad

La API Key se almacena en el archivo .env.

El archivo .env está incluido en .gitignore y no debe subirse al repositorio.

El archivo .env.example sirve como plantilla y no contiene una clave real.

## 14. Estimación de costos

El costo de operación para 50 consultores dependerá principalmente del número de consultas diarias, los tokens utilizados, el modelo de Gemini seleccionado y el tamaño de la información procesada.

Para obtener una estimación precisa se debe medir el consumo real de tokens con preguntas representativas y aplicar las tarifas vigentes del modelo seleccionado.

## 15. Mejoras futuras

Como posibles extensiones se podrían incorporar pruebas automatizadas, una interfaz web, exposición de herramientas mediante MCP, automatización del procesamiento de nuevos informes e integración con herramientas empresariales como SharePoint o Power BI.

## 16. Conclusión

La solución implementa un agente de consulta sobre informes de cierre de proyectos, combinando extracción de documentos, fichas estructuradas, SQLite, búsqueda documental y consultas SQL.

El agente permite realizar preguntas en lenguaje natural y proporciona la respuesta junto con la herramienta y fuente utilizadas.
