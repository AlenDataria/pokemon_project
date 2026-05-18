import logging

from httpx import AsyncClient

from config.settings import BASE_URL, POKEMON_PAGE_SIZE
from pokemon_etl.extract.client import get_pokemon, get_cached_resource
import asyncio
import httpx
import time

logger = logging.getLogger(__name__)

#FUNZIONE SCARICA PAGINA
async def fetch_pokemon_page (client:AsyncClient, offset:int, limit:int=POKEMON_PAGE_SIZE):
    url = f"{BASE_URL}/pokemon?limit={limit}&offset={offset}"
    logger.info(f"Fetching pokemon page offset= {offset}, limit= {limit}")
    return await get_pokemon(client, url)

#FUNZIONE ESTRAI ID
def extract_id (pokemon_url:str):
    return pokemon_url.rstrip("/").split("/")[-1]

#FUNZIONE INGESTION
async def ingest_pokemon ():

    offset = 0
    limit = POKEMON_PAGE_SIZE

    seen_species = set()
    seen_abilities = set()
    seen_types = set()

    semaphore = asyncio.Semaphore(20)

    async with httpx.AsyncClient() as client:

        while True:
            page = await fetch_pokemon_page(client=client,offset=offset,limit=limit)
            results = page.get("results", [])
            if not results:
                break

            logger.info(f"Processing page with {len(results)} pokemon")

            pokemon_tasks = []

            for pokemon in results:

                pokemon_id = extract_id(pokemon["url"])

                logger.debug(f"Ingestion pokemon id= {pokemon_id}")

                pokemon_tasks.append(
                    get_cached_resource(
                    client=client,
                    semaphore=semaphore,
                    resource="pokemon",
                    identifier=pokemon_id
                    )
                )

            pokemon_results = await asyncio.gather(*pokemon_tasks)

            for pokemon_data in pokemon_results:

                #ingestion species
                species_url = pokemon_data["species"]["url"]
                species_id = extract_id(species_url)

                if species_id not in seen_species: #deduplico
                    await get_cached_resource(
                        client=client,
                        semaphore=semaphore,
                        resource="pokemon-species",
                        identifier=species_id
                    )
                    seen_species.add(species_id)

                #ingestion abilities
                for ability in pokemon_data.get("abilities", []):
                    ability_url = ability["ability"]["url"]
                    ability_id = extract_id(ability_url)

                    if ability_id not in seen_abilities: #deduplico
                        await get_cached_resource(
                            client=client,
                            semaphore=semaphore,
                            resource="ability",
                            identifier=ability_id
                        )
                        seen_abilities.add(ability_id)

                #ingestion type
                for type_entry in pokemon_data.get("types", []): #deduplico
                    type_url = type_entry["type"]["url"]
                    type_id = extract_id(type_url)
                    if type_id not in seen_types:
                        await get_cached_resource(
                            client=client,
                            semaphore=semaphore,
                            resource="type",
                            identifier=type_id
                        )
                        seen_types.add(type_id) #deduplico

            offset += limit



#FUNZIONE CALL CLI
def run_extract ():
    start = time.perf_counter()
    logger.info(f"Starting pokemon ingestion")
    asyncio.run(ingest_pokemon())
    elapsed = time.perf_counter() - start
    logger.info(f"Finished pokemon ingestion in {elapsed:.2f} seconds")
