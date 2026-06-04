# services/ortografia.py
from spellchecker import SpellChecker

_spell = None

def _get_spell() -> SpellChecker:
    global _spell
    if _spell is None:
        _spell = SpellChecker(language="es")
    return _spell

def corregir(texto: str) -> tuple:
    spell = _get_spell()
    palabras = texto.split()
    corregidas = []
    hubo = False
    for p in palabras:
        candidato = spell.correction(p)
        if candidato and candidato.lower() != p.lower():
            corregidas.append(candidato)
            hubo = True
        else:
            corregidas.append(p)
    return " ".join(corregidas), hubo