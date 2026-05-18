from pathlib import Path

BASE_URL = "https://pokeapi.co/api/v2"

DATA_DIR = Path("data")

RAW_DIR = DATA_DIR / "raw"
CLEAN_DIR = DATA_DIR / "clean"

POKEMON_PAGE_SIZE = 100