from pathlib import Path


BASE_DIR = Path.cwd()

DATA_DIR = BASE_DIR / "data"

EXPORTS_DIR = BASE_DIR / "exports"


def ensure_directories() -> None:
    """
    Ensures required runtime directories exist.
    """

    DATA_DIR.mkdir(parents=True, exist_ok=True)

    EXPORTS_DIR.mkdir(parents=True, exist_ok=True)