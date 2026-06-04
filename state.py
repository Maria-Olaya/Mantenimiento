from dataclasses import dataclass, field
from pathlib import Path

@dataclass
class AppState:
    año: int = 0
    mes: int = 0
    modo: str = "nuevo"
    actividades_seleccionadas: list = field(default_factory=list)
    dias_por_actividad: dict = field(default_factory=dict)
    archivos_evidencia: list = field(default_factory=list)
    ruta_informe_guardado: str = ""

    def reset(self):
        self.__init__()