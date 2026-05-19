from config.settings import CLEAN_DIR, RAW_DIR
import polars as pl
from pokemon_etl.transform.pokemon import read_raw_json

#SPECIES.PAERQUET
def transform_species():
    species_list = read_raw_json("pokemon-species")

    species_df = pl.DataFrame(species_list)
    species_lf = species_df.lazy()

    species_lf_clean = species_lf.select([
        pl.col("id").cast(pl.Int32).alias("pokemon_id"),
        pl.col("generation").struct.field("url").str.split("/").list.get(-2).cast(pl.Int32).alias("generation_id"),
        pl.col("capture_rate").cast(pl.Int32).alias("capture_rate"),
        pl.col("is_legendary").cast(pl.Boolean).alias("is_legendary"),
        pl.col("is_mythical").cast(pl.Boolean).alias("is_mythical"),
    ])

    df_species = species_lf_clean.collect()
    file_path = CLEAN_DIR / "species.parquet"
    df_species.write_parquet(file_path)