import requests
from src.const import pokemon_url
from src.pokemon import Pokemon

def extract_names() -> list:
    """extracts every pokemon name in existence"""
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

def get_pokemon_data(pokemon_name: str)->Pokemon | None:
    """given a pokemon name returns a pokemon object"""
    #takes data for one pokemon
    url = f"https://pokeapi.co/api/v2/pokemon/{pokemon_name.lower()}"
    response = requests.get(url)
    data = response.json()

    if response.status_code == 200:
        pokemon = Pokemon(
            name = data["name"],
            types = [element["type"]["name"] for element in data["types"]],
            abilities = [element["ability"]["name"] for element in data["abilities"]],
            cry = data["cries"]["latest"],
            forms = [form["name"] for form in data["forms"]],
            height= data["height"],
            id = data["id"],
            moves=[element["move"]["name"] for element in data["moves"]],
            species=data["species"]["name"],
            sprites=data["sprites"],
            stats= {element["stat"]["name"]: element["base_stat"] for element in data["stats"]},
            weight=data["weight"],
        )
        return pokemon
    else:
        return None


if __name__ == "__main__":

    bulbasaur = get_pokemon_data("bulbasaur")

    print(bulbasaur)







