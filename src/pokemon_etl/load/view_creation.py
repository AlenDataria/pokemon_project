import duckdb
import pyarrow
from duckdb_loader import  conn

#Creazione vw_pokemon_full
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

#Creazione vw_stats_pivot
conn.execute(f"""
    CREATE OR REPLACE VIEW vw_pokemon_stats_pivot AS
    SELECT
        pokemon_id,
        MAX(
            CASE
                WHEN stat_name = 'hp'
                THEN base_stat
            END
        ) AS hp,
         MAX(
            CASE
                WHEN stat_name = 'attack'
                THEN base_stat
            END
        ) AS attack,
         MAX(
            CASE
                WHEN stat_name = 'defense'
                THEN base_stat
            END
        ) AS defense,
         MAX(
            CASE
                WHEN stat_name = 'special-attack'
                THEN base_stat
            END
        ) AS special_attack,
         MAX(
            CASE
                WHEN stat_name = 'special-defense'
                THEN base_stat
            END
        ) AS special_defense,
         MAX(
            CASE
                WHEN stat_name = 'speed'
                THEN base_stat
            END
        ) AS speed
    FROM pokemon_stats
    GROUP BY pokemon_id
""")

#Creazione vw_type_matchups
conn.execute(f"""
    CREATE OR REPLACE VIEW vw_type_matchups AS
    SELECT * FROM type_damage_relations
""")

