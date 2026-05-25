import json
import logging
import httpx
from tenacity import (
    retry,
    stop_after_attempt,
    wait_exponential,
    retry_if_exception_type,
)
from config.settings import BASE_URL, RAW_DIR

logger = logging.getLogger(__name__)

@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=1, max=10),
    retry=retry_if_exception_type(httpx.HTTPError),
    reraise=True,
)

#FUNZIONE CHE CHE CHIAMA API
def get_pokemon(url: str):
    logger.info(f"Requesting {url}")
    response = httpx.get(url, timeout=10)
    response.raise_for_status()
    logger.info(f"Response {response.status_code}")
    return response.json()

#FUNZIONE CHE COSTRUISCE LA CACHE
def _build_cached_resource (resource, identifier):
    return RAW_DIR / resource / f"{identifier}.json"


# controlla se dati gia presenti, se non ci sono li registra
def get_cached_and_register_resource (resource: str, identifier: str,):
    cache_path = _build_cached_resource(resource, identifier)

    cache_path.parent.mkdir(parents=True, exist_ok=True)

    if cache_path.exists():
        logger.info(f"Cache hit: {cache_path}")

        with open(cache_path, "r", encoding="utf-8") as f:
            return json.load(f)

    logger.info(f"Cache miss: {cache_path}")

    url = f"{BASE_URL}/{resource}/{identifier}"

    data = get_pokemon(url)

    with open(cache_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    return data



