from config.settings import CLEAN_DIR, RAW_DIR
import polars as pl
from pokemon_etl.transform.pokemon import read_raw_json

#TYPES.PAERQUET
def transform_types():
    type_list = read_raw_json("type")

    type_df = pl.DataFrame(type_list)
    type_lf = type_df.lazy()

    type_lf_clean = type_lf.select([
        pl.col("id").cast(pl.Int32).alias("type_id"),
        pl.col("name").cast(pl.Utf8).alias("type_name"),
    ])

    file_path = CLEAN_DIR / "types.parquet"
    df_types = type_lf_clean.collect()
    df_types.write_parquet(file_path)
#---------------------------------------------------------------------------------------

def transform_type_damage_relations():

    type_list = read_raw_json("type")

    type_df = pl.DataFrame(type_list)
    type_lf = type_df.lazy()


    # DOUBLE_DAMAGE_TO
    type_lf_select = type_lf.select([
        pl.col("name").cast(pl.Utf8).alias("type_name"),
        pl.col("damage_relations").struct.field("double_damage_to")
    ])

    type_lf_explode = type_lf_select.explode("double_damage_to")

    type_new_select = type_lf_explode.select([
        pl.col("type_name").cast(pl.Utf8).alias("attacking_type"),
        pl.col("double_damage_to").struct.field("name").cast(pl.Utf8).alias("defending_type"),
    ])

    type_new_column = type_new_select.with_columns(
        pl.lit(2.0).cast(pl.Float32).alias("multiplier"),
    )
    type_double_damage =  type_new_column.filter(pl.col("defending_type").is_not_null())
  #-------------------------------------------------------------------------------------

   #HALF_DAMAGE_TO
    type_lf_select = type_lf.select([
        pl.col("name").cast(pl.Utf8).alias("type_name"),
        pl.col("damage_relations").struct.field("half_damage_to")
    ])

    type_lf_explode = type_lf_select.explode("half_damage_to")

    type_new_select = type_lf_explode.select([
        pl.col("type_name").cast(pl.Utf8).alias("attacking_type"),
        pl.col("half_damage_to").struct.field("name").cast(pl.Utf8).alias("defending_type"),
    ])

    type_new_column = type_new_select.with_columns(
        pl.lit(0.5).cast(pl.Float32).alias("multiplier"),
    )
    type_half_damage = type_new_column.filter(pl.col("defending_type").is_not_null())
  #-------------------------------------------------------------------------------------

   #NO_DAMAGE_TO
    type_lf_select = type_lf.select([
        pl.col("name").cast(pl.Utf8).alias("type_name"),
        pl.col("damage_relations").struct.field("no_damage_to")
    ])

    type_lf_explode = type_lf_select.explode("no_damage_to")

    type_new_select = type_lf_explode.select([
        pl.col("type_name").cast(pl.Utf8).alias("attacking_type"),
        pl.col("no_damage_to").struct.field("name").cast(pl.Utf8).alias("defending_type"),
    ])

    type_new_column = type_new_select.with_columns(
        pl.lit(0.0).cast(pl.Float32).alias("multiplier"),
    )
    type_no_damage = type_new_column.filter(pl.col("defending_type").is_not_null())
  #-------------------------------------------------------------------------------------

    #Unisco i 3 LazyFrame
    lf_type_damage_relations = pl.concat([
        type_double_damage,
        type_half_damage,
        type_no_damage,
    ])

    #Salvo in parquet
    file_path = CLEAN_DIR / "type_damage_relations.parquet"
    df_type_damage_relations = lf_type_damage_relations.collect()
    df_type_damage_relations.write_parquet(file_path)


transform_types()
transform_type_damage_relations()