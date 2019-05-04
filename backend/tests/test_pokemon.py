import unittest, sys

sys.path.append("../")

from app import db, Pokemon


class PokemonTest(unittest.TestCase):
    
    @classmethod
    def setUpClass(self):
        db.create_all()
    
    @classmethod   
    def tearDownClass(self):
        db.drop_all()

    def test_pokemon_create(self):
        print("######  Testing Pokemon Creation ######")
        pokemon = {
            "pokemon": {
                "name": "Test Pokemon",
                "sprite": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/4.png",
                "cardColours": {"fg": "#eeeeee", "bg": "#3e3e3e", "desc": "#111111"},
            }
        }
        db.session.add(
            Pokemon(
                name=pokemon["pokemon"]["name"],
                sprite=pokemon["pokemon"]["sprite"],
                fg=pokemon["pokemon"]["cardColours"]["fg"],
                bg=pokemon["pokemon"]["cardColours"]["bg"],
                desc=pokemon["pokemon"]["cardColours"]["desc"],
            )
        )
        db.session.commit()
        pokemon_data = (
            db.session.query(Pokemon).filter(Pokemon.name == "Test Pokemon").first()
        )
        pokemondata = {
            "pokemon": {
                "name": pokemon_data.name,
                "sprite": pokemon_data.sprite,
                "cardColours": {
                    "fg": pokemon_data.fg,
                    "bg": pokemon_data.bg,
                    "desc": pokemon_data.desc,
                },
            }
        }
        self.assertEqual(pokemon, pokemondata)
        print("######  Testing Pokemon Creation is SUCCESS  ######")

    def test_pokemon_fetch(self):
        print("######  Testing Pokemon Existance  ######")
        pokemon = {
            "pokemon": {
                "id": 1,
                "name": "Test Pokemon",
                "sprite": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/4.png",
                "cardColours": {"fg": "#eeeeee", "bg": "#3e3e3e", "desc": "#111111"},
            }
        }
        pokemon_data = (
            db.session.query(Pokemon).filter(Pokemon.name == "Test Pokemon").first()
        )
        pokemondata = {
            "pokemon": {
                "id": pokemon_data.id,
                "name": pokemon_data.name,
                "sprite": pokemon_data.sprite,
                "cardColours": {
                    "fg": pokemon_data.fg,
                    "bg": pokemon_data.bg,
                    "desc": pokemon_data.desc,
                },
            }
        }
        self.assertEqual(pokemon, pokemondata)
        print("######  Testing Pokemon Existance is SUCCESS  ######")

    def test_pokemon_update(self):
        print("######  Testing Pokemon Updation  ######")
        pokemon = {
            "pokemon": {
                "name": "New Pokemon",
                "sprite": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/1.png",
                "cardColours": {"fg": "#eeeeee", "bg": "#3e3e3e", "desc": "#111111"},
            }
        }
        if(db.session.query(Pokemon).filter(Pokemon.name == "Test Pokemon").first() is not None):
            db.session.add(
                Pokemon(
                    name=pokemon["pokemon"]["name"],
                    sprite=pokemon["pokemon"]["sprite"],
                    fg=pokemon["pokemon"]["cardColours"]["fg"],
                    bg=pokemon["pokemon"]["cardColours"]["bg"],
                    desc=pokemon["pokemon"]["cardColours"]["desc"],
                )
            )
            db.session.commit()
        pokemon_data = (
            db.session.query(Pokemon).filter(Pokemon.name == "New Pokemon").first()
        )
        pokemondata = {
            "pokemon": {
                "name": pokemon_data.name,
                "sprite": pokemon_data.sprite,
                "cardColours": {
                    "fg": pokemon_data.fg,
                    "bg": pokemon_data.bg,
                    "desc": pokemon_data.desc,
                },
            }
        }
        self.assertEqual(pokemon, pokemondata)
        print("######  Testing Pokemon Updation is SUCCESS  ######")

    def test_pokemon_zdelete(self):
        print("######  Testing Pokemon Deletion  ######")
        pokemon = (
            db.session.query(Pokemon).filter(Pokemon.name == "New Pokemon").first()
        )
        db.session.delete(pokemon)
        db.session.commit()
        self.assertIsNone(
            db.session.query(Pokemon).filter(Pokemon.name == "New Pokemon").first()
        )
        print("######  Testing Pokemon Deletion is SUCCESS  ######")

if __name__ == "__main__":
    unittest.main()
