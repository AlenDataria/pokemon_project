import logging
from config.settings import BASE_URL, POKEMON_PAGE_SIZE
from pokemon_etl.extract.client import get_pokemon, get_cached_and_register_resource

logger = logging.getLogger(__name__)

#FUNZIONE SCARICA PAGINA
def fetch_pokemon_page (offset:int, limit:int=POKEMON_PAGE_SIZE):
    url = f"{BASE_URL}/pokemon?limit={limit}&offset={offset}"
    logger.info(f"Fetching pokemon page offset= {offset}, limit= {limit}")
    return get_pokemon(url)

#FUNZIONE ESTRAI ID
def extract_id (pokemon_url:str):
    return pokemon_url.rstrip("/").split("/")[-1]

#FUNZIONE INGESTION
def ingest_pokemon ():

    offset = 0
    limit = POKEMON_PAGE_SIZE

    seen_species = set()
    seen_abilities = set()
    seen_types = set()


    while True:
        page = fetch_pokemon_page(offset=offset,limit=limit)
        results = page.get("results", [])
        if not results:
            break

        logger.info(f"Processing page with {len(results)} pokemon")

        pokemon_results = []

        for pokemon in results:

            pokemon_id = extract_id(pokemon["url"])

            logger.debug(f"Ingestion pokemon id= {pokemon_id}")

            pokemon_data = get_cached_and_register_resource(identifier=pokemon_id, resource="pokemon")

            pokemon_results.append(pokemon_data)

        for pokemon in pokemon_results:

            #ingestion species
            species_url = pokemon["species"]["url"]
            species_id = extract_id(species_url)

            if species_id not in seen_species: #deduplico
                get_cached_and_register_resource(
                    resource="pokemon-species",
                    identifier=species_id
                )
                seen_species.add(species_id)

            #ingestion abilities
            for ability in pokemon.get("abilities", []):
                ability_url = ability["ability"]["url"]
                ability_id = extract_id(ability_url)

                if ability_id not in seen_abilities: #deduplico
                    get_cached_and_register_resource(
                        resource="ability",
                        identifier=ability_id
                    )
                    seen_abilities.add(ability_id)

            #ingestion type
            for type_entry in pokemon.get("types", []): #deduplico
                type_url = type_entry["type"]["url"]
                type_id = extract_id(type_url)
                if type_id not in seen_types:
                    get_cached_and_register_resource(
                        resource="type",
                        identifier=type_id
                    )
                    seen_types.add(type_id) #deduplico

        offset += len(results)







