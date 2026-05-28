from dataclasses import dataclass

@dataclass
class Pokemon:
    name: str
    types: list
    abilities: list
    cry: str
    forms: list
    height: float
    id: int
    moves: list
    species: str
    sprites: dict
    stats: dict
    weight: float

    def presentati(self):
        print(f"ciao sono {self.name.capitalize()} peso {self.weight}, sono alto {self.height}, il mio codice pensionistico è {self.id}, sono della casata degli {self.species}")

    def __str__(self):
        return f"""
    name: {self.name}
    types: {self.types}
    abilities: {self.abilities}
    forms: {self.forms}
    height: {self.height}
    id: {self.id}
    moves: {self.moves}
    species: {self.species}
    sprites: {self.sprites}
    stats: {self.stats}
    weight: {self.weight}
    """

if __name__ == "__main__":

    pokemon_test = Pokemon(
        name = "bulbasaur",
        types = ["poison", "weed"],
        abilities = ["brucare", "fumare"],
        cry = "a lot",
        forms = ["base"],
        height = 7.0,
        id = 1,
        moves = ["a lot", "foglie_lame", "assorbi_ginocchio"],
        species = "bulbasaur",
        sprites = {"base":"coca cola", "back":"fanta"},
        stats = {"attack":3, "defence": 5, "hp":67},
        weight = 69.0, # nice
    )

    pokemon_test.presentati()

    print("i can learn:")
    for x in pokemon_test.moves:
        print(x)