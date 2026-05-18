import argparse

from pokemon_etl.extract.ingest import run_extract


def main():
    parser = argparse.ArgumentParser(description="Pokemon ETL CLI")

    parser.add_argument(
        "command",
        choices=["extract"],
        help="Command to run"
    )

    args = parser.parse_args()

    if args.command == "extract":
        run_extract()


if __name__ == "__main__":
    main()