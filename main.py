import argparse
from pokemon_etl.extract.extract_all import extract_all
from pokemon_etl.pipeline import run_all
from pokemon_etl.transform.transform_all import transform_all
from pokemon_etl.load.load_all import load_all


def main():
    parser = argparse.ArgumentParser(description="Pokemon ETL CLI")

    parser.add_argument(
        "command",
        choices=["extract", "transform", "load", "all"],
        help="Command to run"
    )

    args = parser.parse_args()

    if args.command == "extract":
        extract_all()
    if args.command == "transform":
        transform_all()
    if args.command == "load":
        load_all()
    if args.command == "all":
        run_all()


if __name__ == "__main__":
    main()
