from pokemon_etl.extract.ingest import ingest_pokemon
import asyncio


#FUNZIONE EXTRACT ALL
def extract_all():
    asyncio.run(ingest_pokemon())