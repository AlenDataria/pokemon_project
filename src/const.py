from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

RAW_DATA_DIR = BASE_DIR / "data/raw"

#extraction
pokemon_url = "https://pokeapi.co/api/v2/pokemon?limit=100&offset=0"
