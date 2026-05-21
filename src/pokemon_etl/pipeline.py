from pokemon_etl.extract.extract_all import extract_all
from pokemon_etl.transform.transform_all import transform_all
from pokemon_etl.load.load_all import load_all

def run_all():
    extract_all()
    transform_all()
    load_all()