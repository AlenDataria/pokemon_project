import duckdb
import pyarrow
from config.settings import DATA_DIR, CLEAN_DIR

#Creazione database DuckDB
conn = duckdb.connect(DATA_DIR/"mart.duckdb")

#CREAZIONE TABELLA DUCKDB POKEMON
#path del parquet
path = CLEAN_DIR / "pokemon.parquet"

#Creazione tabella
conn.execute(f"""
    CREATE OR REPLACE TABLE pokemon AS
    SELECT * FROM read_parquet('{path}');
""")
#-----------------------------------------------------------------------------------------

#CREAZIONE TABELLA DUCKDB POKEMON_ABILITIES
#path del parquet
path = CLEAN_DIR / "pokemon_abilities.parquet"

#Creazione tabella
conn.execute(f"""
    CREATE OR REPLACE TABLE pokemon_abilities AS
    SELECT * FROM read_parquet('{path}');
""")
#----------------------------------------------------------------------------------------

#CREAZIONE TABELLA DUCKDB POKEMON_STATS
#path del parquet
path = CLEAN_DIR / "pokemon_stats.parquet"

#Creazione tabella
conn.execute(f"""
    CREATE OR REPLACE TABLE pokemon_stats AS
    SELECT * FROM read_parquet('{path}');
""")
#----------------------------------------------------------------------------------------

#CREAZIONE TABELLA DUCKDB POKEMON_TYPES
#path del parquet
path = CLEAN_DIR / "pokemon_types.parquet"

#Creazione tabella
conn.execute(f"""
    CREATE OR REPLACE TABLE pokemon_types AS
    SELECT * FROM read_parquet('{path}');
""")
#----------------------------------------------------------------------------------------

#CREAZIONE TABELLA DUCKDB SPECIES
#path del parquet
path = CLEAN_DIR / "species.parquet"

#Creazione tabella
conn.execute(f"""
    CREATE OR REPLACE TABLE species AS
    SELECT * FROM read_parquet('{path}');
""")
#----------------------------------------------------------------------------------------

#CREAZIONE TABELLA DUCKDB TYPE_DAMAGE_RELATIONS
#path del parquet
path = CLEAN_DIR / "type_damage_relations.parquet"

#Creazione tabella
conn.execute(f"""
    CREATE OR REPLACE TABLE type_damage_relations AS
    SELECT * FROM read_parquet('{path}');
""")
#----------------------------------------------------------------------------------------

#CREAZIONE TABELLA DUCKDB TYPES
#path del parquet
path = CLEAN_DIR / "types.parquet"

#Creazione tabella
conn.execute(f"""
    CREATE OR REPLACE TABLE types AS
    SELECT * FROM read_parquet('{path}');
""")
#---------------------------------------------------------------------------------------


















