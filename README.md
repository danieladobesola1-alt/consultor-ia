\# Consultor IA



Agente de consulta sobre informes de cierre de proyectos, desarrollado como parte de la Prueba Técnica Consultor IA.



\## Descripción



El proyecto procesa informes de cierre de proyectos en formato PDF, extrae su contenido, genera fichas estructuradas utilizando Gemini y almacena la información en una base de datos SQLite.



El agente permite realizar preguntas en lenguaje natural y decide qué herramienta utilizar:



\- \*\*Búsqueda documental:\*\* para consultar información específica dentro de los informes.

\- \*\*Consulta SQL:\*\* para consultar información estructurada almacenada en la base de datos.



La respuesta indica la herramienta utilizada y la fuente de información.



\## Estructura del proyecto



```text

consultor-ia/

├── data/

│   ├── raw/

│   ├── processed/

│   └── consultor\_ia.db

├── outputs/

│   └── fichas/

├── src/

│   ├── extraction/

│   │   ├── extract\_text.py

│   │   └── generate\_fichas.py

│   ├── database/

│   │   ├── database.py

│   │   └── load\_data.py

│   ├── tools/

│   │   ├── document\_search.py

│   │   └── sql\_query.py

│   ├── agent/

│   │   └── agent.py

│   └── schemas/

│       └── project\_schema.py

├── tests/

├── .env

├── .env.example

├── .gitignore

├── requirements.txt

└── README.md

