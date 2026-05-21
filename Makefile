extract:
	python -m pokemon_etl extract

transform:
	python -m pokemon_etl transform

load:
	python -m pokemon_etl load

all:
	python -m pokemon_etl all

clean:
	rm -rf data/raw/*
	rm -rf data/clean/*
	rm -f data/mart.duckdb

test:
	PYTHONPATH=. uv run pytest