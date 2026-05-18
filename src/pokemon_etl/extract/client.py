import json
import logging
from pathlib import Path

import httpx
from polars.catalog.unity import client
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

#FUNZIONE GET.JSON CHE CHE CHIAMA API
async def get_pokemon(client:httpx.AsyncClient, url: str):
    logger.info(f"Requesting {url}")
    response = await client.get(url, timeout=10)
    response.raise_for_status()
    logger.info(f"Response {response.status_code}")
    return response.json()


def _build_cached_resource (resource, identifier):
    return RAW_DIR / resource / f"{identifier}.json"


# controlla se dati gia presenti, se non ci sono li registra
async def get_cached_resource (client: httpx.AsyncClient, semaphore, resource: str, identifier: str,):
    cache_path = _build_cached_resource(resource, identifier)

    cache_path.parent.mkdir(parents=True, exist_ok=True)

    if cache_path.exists():
        logger.info(f"Cache hit: {cache_path}")

        with open(cache_path, "r", encoding="utf-8") as f:
            return json.load(f)

    async with semaphore:
        logger.info(f"Cache miss: {cache_path}")

        url = f"{BASE_URL}/{resource}/{identifier}"

        data = await get_pokemon(client,url)

        with open(cache_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

        return data



