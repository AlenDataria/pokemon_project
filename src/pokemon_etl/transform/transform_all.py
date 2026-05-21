from pokemon_etl.transform.pokemon import transform_pokemon
from pokemon_etl.transform.pokemon import transform_pokemon_abilities
from pokemon_etl.transform.pokemon import transform_pokemon_stats
from pokemon_etl.transform.pokemon import transform_pokemon_types
from pokemon_etl.transform.species import transform_species
from pokemon_etl.transform.pokemon_types import transform_types
from pokemon_etl.transform.pokemon_types import transform_type_damage_relations
import logging

logger = logging.getLogger(__name__)

def transform_all():
    logger.info("Starting transform phase")

    logger.info("Transforming pokemon")
    transform_pokemon()

    logger.info("Transforming pokemon abilities")
    transform_pokemon_abilities()

    logger.info("Transforming pokemon stats")
    transform_pokemon_stats()

    logger.info("Transforming pokemon types")
    transform_pokemon_types()

    logger.info("Transforming species")
    transform_types()

    logger.info("Transforming species damage relations")
    transform_type_damage_relations()

    logger.info("Transforming species stats")
    transform_species()

    logger.info("Transform phase completed")