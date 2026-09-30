from pydantic import BaseModel
from typing import List, Optional


class ProjectFicha(BaseModel):
    codigo_proyecto: str
    nombre_proyecto: str
    empresa: str
    sector: str
    objetivo_general: str
    problema_identificado: str
    resultados_principales: List[str]
    indicadores: List[str]
    objetivos_pendientes: List[str]
    conclusiones: str
    fuente: str