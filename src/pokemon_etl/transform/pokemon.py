import json
from config.settings import CLEAN_DIR, RAW_DIR
import polars as pl


#Funzione che legge e inserisce i file json raw in una lista di dizionari per dataframe
def read_raw_json (rw_folder):
    folder = RAW_DIR / rw_folder

    #Leggo i file presenti in /raw/pokemon, e li inserisco in una lista
    lista_json = []

    for raw_file in folder.glob("*.json"):
        with open(raw_file, "r", encoding="utf-8") as f:
            lista_json.append(json.load(f))
    return lista_json




#Funzione che prende la lista di pokemon li trasforma in parquet
#POKEMON.PARQUET
def transform_pokemon():

    #Chiamiamo la funzione che genera la lista
    pokemon_list = read_raw_json("pokemon")
    #Trasformo la lista di file json in un dataframe
    poke_df = pl.DataFrame(pokemon_list)

    #Comincio le trasformazioni in LazyFrame
    poke_lf = poke_df.lazy()
    poke_lf_clean = poke_lf.select([
        pl.col("id").cast(pl.Int32).alias("pokemon_id"),
        pl.col("name").cast(pl.Utf8),
        pl.col("height").cast(pl.Int32).alias("height_dm"),
        pl.col("weight").cast(pl.Int32).alias("weight_hg"),
        pl.col("base_experience").cast(pl.Int32),
        pl.col("is_default").cast(pl.Boolean)
    ])

    #Salvo in formato parquet in /data/clean
    file_path= CLEAN_DIR / "pokemon.parquet" #creo dove salvare

    df_pokemon = poke_lf_clean.collect() #Trasforma il lazyframe in dataframe
    df_pokemon.write_parquet(file_path) #Salvo in parquet
#---------------------------------------------------------------------------------------

#POKEMON_STATS.PARQUET
def transform_pokemon_stats():
    pokemon_list = read_raw_json("pokemon")

    poke_df_stats = pl.DataFrame(pokemon_list)
    poke_lf_stats = poke_df_stats.lazy()

    #seleziono le colonne che mi servono
    poke_lf_stats_clean_select = (poke_lf_stats.select([
        pl.col("id").cast(pl.Int32).alias("pokemon_id"),
        pl.col("stats")
    ]))
    #con .explode() stats non è più contenuto in liste ma in righe
    poke_lf_stats_clean_explode = poke_lf_stats_clean_select.explode("stats")

    #con .struct.field() estraggo gli stats che mi interessano
    poke_lf_stats_clean = poke_lf_stats_clean_explode.select(
        pl.col("pokemon_id").cast(pl.Int32),
        pl.col("stats").struct.field("base_stat").cast(pl.Int32).alias("base_stat"),
        pl.col("stats").struct.field("effort").cast(pl.Int32).alias("effort"),
        pl.col("stats").struct.field("stat").struct.field("name").cast(pl.Utf8).alias("stat_name")
    )

    #salvo in formato parquet
    file_path = CLEAN_DIR / "pokemon_stats.parquet"
    df_pokemon_stats = poke_lf_stats_clean.collect()
    df_pokemon_stats.write_parquet(file_path)
#----------------------------------------------------------------------------------------


#POKEMON_TYPES.PARQUET
def transform_pokemon_types():
    pokemon_list = read_raw_json("pokemon")

    poke_df_types = pl.DataFrame(pokemon_list)
    poke_lf_types = poke_df_types.lazy()

    poke_lf_types_select = poke_lf_types.select([
        pl.col("id"),
        pl.col("types"),
    ])

    poke_lf_types_explode = poke_lf_types_select.explode("types")

    poke_lf_type_clean = poke_lf_types_explode.select([
        pl.col("id").cast(pl.Int32).alias("pokemon_id"),
        pl.col("types").struct.field("slot").cast(pl.Int32).alias("slot"),
        pl.col("types").struct.field("type").struct.field("name").cast(pl.Utf8).alias("type_name"),
        pl.col("types").struct.field("type").struct.field("url").cast(pl.Utf8).alias("type_url"),
    ])


    file_path = CLEAN_DIR / "pokemon_types.parquet"
    df_pokemon_types = poke_lf_type_clean.collect()
    df_pokemon_types.write_parquet(file_path)
#-----------------------------------------------------------------------------------------

#POKEMON_ABILITY.PARQUET
def transform_pokemon_abilities():
    pokemon_list = read_raw_json("pokemon")

    poke_df_abilities = pl.DataFrame(pokemon_list)
    poke_lf_abilities = poke_df_abilities.lazy()

    poke_lf_abilities_select = poke_lf_abilities.select([
        pl.col("id"),
        pl.col("abilities")
    ])

    poke_lf_abilities_explode = poke_lf_abilities_select.explode("abilities")

    poke_lf_abilities_clean = poke_lf_abilities_explode.select([
        pl.col("id").cast(pl.Int32).alias("pokemon_id"),
        pl.col("abilities").struct.field("ability").struct.field("name").cast(pl.Utf8).alias("ability_name"),
        pl.col("abilities").struct.field("is_hidden").cast(pl.Boolean).alias("is_hidden"),
        pl.col("abilities").struct.field("ability").struct.field("url").cast(pl.Utf8).alias("ability_url"),
    ])

    file_path = CLEAN_DIR / "pokemon_abilities.parquet"
    df_pokemon_abilities = poke_lf_abilities_clean.collect()
    df_pokemon_abilities.write_parquet(file_path)



transform_pokemon()
transform_pokemon_stats()
transform_pokemon_types()
transform_pokemon_abilities()



