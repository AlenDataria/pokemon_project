from pokemon_etl.load.duckdb_loader import conn

def test_heaviest_pokemon_by_type():
    result = conn.execute(f'''
        SELECT type_name, pokemon_name, weight_hg
        FROM vw_pokemon_full
        QUALIFY ROW_NUMBER() OVER (
        PARTITION BY type_name
        ORDER BY weight_hg DESC
    ) = 1;
    ''').fetchall()
    assert len(result) > 0

def test_average_stat_total_by_generatio():
    result = conn.execute(f'''
        SELECT
            vpf.generation_id,
            AVG(vsp.stat_total) AS avg_stat_total
        FROM vw_pokemon_full vpf
        LEFT JOIN vw_stats_pivot vsp
        ON vpf.pokemon_id = vsp.pokemon_id
        GROUP BY vpf.generation_id
        ORDER BY avg_stat_total DESC;
    ''').fetchall()
    assert len(result) > 0

def test_strongest_attacking_type():
    result = conn.execute(f'''
        SELECT attacking_type, COUNT(*) AS num_super_effective
        FROM vw_type_matchups WHERE multiplier = 2
        GROUP BY attacking_type ORDER BY 2 DESC
    ''').fetchall()
    assert len(result) > 0