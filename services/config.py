import json
from pathlib import Path

CONFIG_PATH = Path(__file__).parent.parent / "config.json"
DEFAULT_CARPETA = Path.home() / "Documentos" / "Mantenimiento"

def cargar_config() -> dict:
    if not CONFIG_PATH.exists():
        return {"carpeta_fuente": str(DEFAULT_CARPETA)}
    try:
        with open(CONFIG_PATH, encoding="utf-8") as f:
            contenido = f.read().strip()
            if not contenido:
                return {"carpeta_fuente": str(DEFAULT_CARPETA)}
            return json.loads(contenido)
    except json.JSONDecodeError:
        return {"carpeta_fuente": str(DEFAULT_CARPETA)}

def guardar_config(config: dict):
    with open(CONFIG_PATH, "w", encoding="utf-8") as f:
        json.dump(config, f, ensure_ascii=False, indent=2)

def carpeta_fuente() -> Path:
    ruta = Path(cargar_config()["carpeta_fuente"])
    ruta.mkdir(parents=True, exist_ok=True)
    return ruta