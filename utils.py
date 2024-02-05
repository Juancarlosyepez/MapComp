import sys
import os

def resource_path(relative_path):
    """Devuelve el camino absoluto al recurso, para ser usado tanto en desarrollo como en el modo empaquetado."""
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)
