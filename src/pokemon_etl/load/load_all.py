import duckdb
from config.settings import CLEAN_DIR, DATA_DIR
import logging

logger = logging.getLogger(__name__)

def load_all():

    logger.info("Starting load phase")

    conn = duckdb.connect(DATA_DIR / "mart.duckdb")
    path = CLEAN_DIR / "pokemon.parquet"

    # Creazione tabella pokemon
    logger.info("Loading pokemon table")
    conn.execute(f"""
        CREATE OR REPLACE TABLE pokemon AS
        SELECT * FROM read_parquet('{path}');
    """)
    # -----------------------------------------------------------------------------------------

    # CREAZIONE TABELLA DUCKDB POKEMON_ABILITIES
    # path del parquet
    path = CLEAN_DIR / "pokemon_abilities.parquet"

    # Creazione tabella
    logger.info("Loading pokemon_abilities table")
    conn.execute(f"""
        CREATE OR REPLACE TABLE pokemon_abilities AS
        SELECT * FROM read_parquet('{path}');
    """)
    # ----------------------------------------------------------------------------------------

    # CREAZIONE TABELLA DUCKDB POKEMON_STATS
    # path del parquet
    path = CLEAN_DIR / "pokemon_stats.parquet"

    # Creazione tabella
    logger.info("Loading pokemon_stats table")
    conn.execute(f"""
        CREATE OR REPLACE TABLE pokemon_stats AS
        SELECT * FROM read_parquet('{path}');
    """)
    # ----------------------------------------------------------------------------------------

    # CREAZIONE TABELLA DUCKDB POKEMON_TYPES
    # path del parquet
    path = CLEAN_DIR / "pokemon_types.parquet"

    # Creazione tabella
    logger.info("Loading pokemon_types table")
    conn.execute(f"""
        CREATE OR REPLACE TABLE pokemon_types AS
        SELECT * FROM read_parquet('{path}');
    """)
    # ----------------------------------------------------------------------------------------

    # CREAZIONE TABELLA DUCKDB SPECIES
    # path del parquet
    path = CLEAN_DIR / "species.parquet"

    # Creazione tabella
    logger.info("Loading species table")
    conn.execute(f"""
        CREATE OR REPLACE TABLE species AS
        SELECT * FROM read_parquet('{path}');
    """)
    # ----------------------------------------------------------------------------------------

    # CREAZIONE TABELLA DUCKDB TYPE_DAMAGE_RELATIONS
    # path del parquet
    path = CLEAN_DIR / "type_damage_relations.parquet"

    # Creazione tabella
    logger.info("Loading type_damage_relations table")
    conn.execute(f"""
        CREATE OR REPLACE TABLE type_damage_relations AS
        SELECT * FROM read_parquet('{path}');
    """)
    # ----------------------------------------------------------------------------------------

    # CREAZIONE TABELLA DUCKDB TYPES
    # path del parquet
    path = CLEAN_DIR / "types.parquet"

    # Creazione tabella
    logger.info("Loading types table")
    conn.execute(f"""
        CREATE OR REPLACE TABLE types AS
        SELECT * FROM read_parquet('{path}');
    """)
   #-------------------------------------------------------------------------------------
    #CREAZIONE VIEW
    # Creazione vw_pokemon_full
    logger.info("Creating vw_pokemon_full")
    conn.execute("""
        CREATE OR REPLACE VIEW vw_pokemon_full AS
        SELECT
            p.pokemon_id,
            p.name AS pokemon_name,
            p.height_dm,
            p.weight_hg,
            p.base_experience,
            pt.type_name,
            s.generation_id,
            s.capture_rate,
            s.is_legendary,
            s.is_mythical
        FROM pokemon p
        LEFT JOIN pokemon_types pt
            ON p.pokemon_id = pt.pokemon_id
        LEFT JOIN species s
            ON p.pokemon_id = s.pokemon_id
    """)

    # Creazione vw_stats_pivot
    logger.info("Creating vw_stats_pivot")
    conn.execute(f"""
    CREATE OR REPLACE VIEW vw_stats_pivot AS
    SELECT
        *,
        hp + attack + defense + special_attack + special_defense + speed AS stat_total
    FROM (
        SELECT
            pokemon_id,
            MAX(CASE WHEN stat_name = 'hp' THEN base_stat END) AS hp,
            MAX(CASE WHEN stat_name = 'attack' THEN base_stat END) AS attack,
            MAX(CASE WHEN stat_name = 'defense' THEN base_stat END) AS defense,
            MAX(CASE WHEN stat_name = 'special-attack' THEN base_stat END) AS special_attack,
            MAX(CASE WHEN stat_name = 'special-defense' THEN base_stat END) AS special_defense,
            MAX(CASE WHEN stat_name = 'speed' THEN base_stat END) AS speed
        FROM pokemon_stats
        GROUP BY pokemon_id
    )
""")

    # Creazione vw_type_matchups
    logger.info("Creating vw_type_matchups")
    conn.execute(f"""
        CREATE OR REPLACE VIEW vw_type_matchups AS
        SELECT * FROM type_damage_relations
    """)

    logger.info("Load phase completed")

    conn.close()