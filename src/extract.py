import requests
from src.const import pokemon_url

def extract_names() -> list:

    search_path = pokemon_url
    data = []
    i = 0
    while True:
        response = requests.get(search_path)
        raw_data = response.json()
        next_url = raw_data["next"]
        pokemon_list = raw_data["results"]
        data_mom = [element["name"] for element in pokemon_list]
        data.append(data_mom)
        if next_url is None:
            print("finished")
            break
        search_path = next_url
        i += 1
        print(f"{i} round done")

    return data

def get_pokemon_data(pokemon_name: str):
 url = f"https://pokeapi.co/api/v2/pokemon/{pokemon_name.lower()}"
 response = requests.get(url)

 if response.status_code == 200:
     return response.json()
 else:
     return None


if __name__ == "__main__":
    from src.save import save_json
    from src.const import RAW_DATA_DIR

    data = get_pokemon_data("bulbasaur")

    save_json(data, path = RAW_DATA_DIR/"test_bulba.json")
    print("mia madre")





