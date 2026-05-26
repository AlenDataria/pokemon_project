from dataclasses import dataclass

@dataclass
class Pokemon:
    name: str
    types: list
    abilities: list
    cries: list
    forms: list
    height: float
    id: int
    moves: list
    species: str
    sprites: list
    stats: dict
    weight: float

    def presentati(self):
        print(f"ciao sono {self.name.capitalize()} peso {self.weight}, sono alto {self.height}, il mio codice pensionistico è {self.id}, sono della casata degli {self.species}")

if __name__ == "__main__":

    pokemon_test = Pokemon(
        name = "bulbasaur",
        types = ["poison", "weed"],
        abilities = ["brucare", "fumare"],
        cries = ["a lot"],
        forms = ["base"],
        height = 7.0,
        id = 1,
        moves = ["a lot", "foglie_lame", "assorbi_ginocchio"],
        species = "bulbasaur",
        sprites = ["coca cola", "fanta"],
        stats = {"attack":3, "defence": 5, "hp":67},
        weight = 69.0, # nice
    )

    pokemon_test.presentati()

    print("i can learn:")
    for x in pokemon_test.moves:
        print(x)