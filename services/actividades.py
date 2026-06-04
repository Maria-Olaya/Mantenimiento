import json
from pathlib import Path

ACTIVIDADES_PATH = Path(__file__).parent.parent / "actividades.json"

def cargar_actividades() -> list:
    if not ACTIVIDADES_PATH.exists():
        return []
    try:
        with open(ACTIVIDADES_PATH, encoding="utf-8") as f:
            contenido = f.read().strip()
            if not contenido:
                return []
            return sorted(json.loads(contenido))
    except json.JSONDecodeError:
        return []

def _guardar(lista: list):
    with open(ACTIVIDADES_PATH, "w", encoding="utf-8") as f:
        json.dump(lista, f, ensure_ascii=False, indent=2)

def guardar_actividad(nombre: str):
    nombre = nombre.strip()
    if not nombre:
        raise ValueError("El nombre no puede estar vacío.")
    lista = cargar_actividades()
    if nombre.lower() in [a.lower() for a in lista]:
        raise ValueError(f"Ya existe la actividad '{nombre}'.")
    lista.append(nombre)
    _guardar(sorted(lista))

def eliminar_actividad(nombre: str):
    lista = [a for a in cargar_actividades() if a != nombre]
    _guardar(lista)