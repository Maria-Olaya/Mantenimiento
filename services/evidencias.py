import shutil
from pathlib import Path
from services.config import carpeta_fuente

def _carpeta_evidencias(año: int, mes: int) -> Path:
    p = carpeta_fuente() / f"{año}_{mes:02d}" / "evidencias"
    p.mkdir(parents=True, exist_ok=True)
    return p

def copiar_evidencias(archivos: list, año: int, mes: int):
    destino = _carpeta_evidencias(año, mes)
    for src in archivos:
        src = Path(src)
        dst = destino / src.name
        if dst.exists():
            stem, suffix = src.stem, src.suffix
            i = 2
            while dst.exists():
                dst = destino / f"{stem}_{i}{suffix}"
                i += 1
        shutil.copy2(src, dst)

def contar_evidencias(año: int, mes: int) -> int:
    p = _carpeta_evidencias(año, mes)
    return len([f for f in p.iterdir() if f.is_file()])