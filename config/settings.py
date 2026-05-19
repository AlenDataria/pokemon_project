from pathlib import Path

BASE_URL = "https://pokeapi.co/api/v2"


BASE_DIR = Path("/Users/rosannadenigro/PycharmProjects/pokemon_project")
DATA_DIR = BASE_DIR / "data"
RAW_DIR = DATA_DIR / "raw"
CLEAN_DIR = DATA_DIR / "clean"

POKEMON_PAGE_SIZE = 100