from flask import Flask, request, json, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
import os

# Initializing App
app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))

# Database
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(
    basedir, "db.sqlite"
)
app.config["SQLALCHEMY_TRACK_MODIFICAIONS"] = False

# Initializing Database
db = SQLAlchemy(app)

# Pokemon Class
class Pokemon(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(500), unique=True, nullable=False)
    sprite = db.Column(db.String, unique=True, nullable=False)
    fg = db.Column(db.String, nullable=False)
    bg = db.Column(db.String, nullable=False)
    desc = db.Column(db.String, nullable=False)

    def __init__(self, name, sprite, fg, bg, desc):
        self.name = name
        self.sprite = sprite
        self.fg = fg
        self.bg = bg
        self.desc = desc


# Handling 404 Error
@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404


# POST Method
@app.route("/api/pokemon", methods=["POST"])
def create_pokemon():
    # Taking Input
    pokemon = request.get_json()
    # Checking Conditions
    if len(pokemon["pokemon"]["name"]) <= 0:
        return "Name is Required"
    elif len(pokemon["pokemon"]["name"]) > 50:
        return "Name should be inbetween 1 and 50"
    else:
        name = pokemon["pokemon"]["name"]
    if len(pokemon["pokemon"]["sprite"]) <= 0:
        return "Sprite is Required"
    elif len(pokemon["pokemon"]["sprite"]) > 200:
        return "Sprite should be inbetween 1 and 200"
    else:
        sprite = pokemon["pokemon"]["sprite"]
    fg = pokemon["pokemon"]["cardColours"]["fg"]
    bg = pokemon["pokemon"]["cardColours"]["bg"]
    desc = pokemon["pokemon"]["cardColours"]["desc"]
    pokemondata = Pokemon(name, sprite, fg, bg, desc)
    # Adding new Pokemon
    db.session.add(pokemondata)
    db.session.commit()
    # Getting the Pokemon Details
    pokemon = Pokemon.query.filter(Pokemon.name == name).first()
    pokemondata = {
        "pokemon": {
            "id": pokemon.id,
            "name": pokemon.name,
            "sprite": pokemon.sprite,
            "cardColours": {"fg": pokemon.fg, "bg": pokemon.bg, "desc": pokemon.desc},
        }
    }
    return jsonify(pokemondata)


# GET Method
@app.route("/api/pokemon/<int:id>", methods=["GET"])
def get_pokemon(id):
    # Checking Conditions
    if not id:
        return ("Pokemon ID must be provided"),404
    pokemon = Pokemon.query.get(id)
    if pokemon == None:
        return ("No Pokemon found with that ID"),404
    # Getting the Pokemon Details
    else:
        pokemondata = {
            "pokemon": {
                "id": pokemon.id,
                "name": pokemon.name,
                "sprite": pokemon.sprite,
                "cardColours": {
                    "fg": pokemon.fg,
                    "bg": pokemon.bg,
                    "desc": pokemon.desc,
                },
            }
        }
        return jsonify(pokemondata)


# PATCH Method
@app.route("/api/pokemon/<int:id>", methods=["PATCH"])
def patch_pokemon(id):
    # Checking Conditions
    pokemon = Pokemon.query.get(id)
    if pokemon == None:
        return ("No Pokemon found with that ID to Update"),404
    else:
        # Updating the Pokemon Details
        pokemon_data = request.json["pokemon"]
        if "name" in pokemon_data:
            if len(pokemon_data["name"]) <= 0:
                return ("Name is Required"),404
            elif len(pokemon_data["name"]) > 50:
                return( "Name should be inbetween 1 and 50"),404
            else:
                pokemon.name = pokemon_data["name"]
        if "sprite" in pokemon_data:
            if len(pokemon_data["sprite"]) <= 0:
                return "Sprite is Required"
            elif len(pokemon_data["sprite"]) > 200:
                return "Sprite should be inbetween 1 and 200"
            else:
                pokemon.sprite = pokemon_data["sprite"]
        if "cardColours" in pokemon_data:
            cardColours_data = request.json["pokemon"]["cardColours"]
            if "fg" in cardColours_data:
                pokemon.fg = pokemon_data["cardColours"]["fg"]
            if "bg" in cardColours_data:
                pokemon.bg = pokemon_data["cardColours"]["bg"]
            if "desc" in cardColours_data:
                pokemon.desc = pokemon_data["cardColours"]["desc"]
        db.session.commit()
        # Getting the  updated Pokemon Details
        pokemon = Pokemon.query.filter(Pokemon.id == id).first()
        pokemondata = {
            "pokemon": {
                "id": pokemon.id,
                "name": pokemon.name,
                "sprite": pokemon.sprite,
                "cardColours": {
                    "fg": pokemon.fg,
                    "bg": pokemon.bg,
                    "desc": pokemon.desc,
                },
            }
        }
        return jsonify(pokemondata)


# DELETE Method
@app.route("/api/pokemon/<int:id>", methods=["DELETE"])
def delete_pokemon(id):
    # Checking Conditions
    pokemon = Pokemon.query.get(id)
    if pokemon == None:
        return ("No Pokemon found with that ID to Delete"),404
    else:
        pokemon = Pokemon.query.filter(Pokemon.id == id).first()
        pokemondata = {
            "pokemon": {
                "id": pokemon.id,
                "name": pokemon.name,
                "sprite": pokemon.sprite,
                "cardColours": {
                    "fg": pokemon.fg,
                    "bg": pokemon.bg,
                    "desc": pokemon.desc,
                },
            }
        }
        # Deleting the Pokemon Details
        db.session.delete(pokemon)
        db.session.commit()
        # Getting the deleted Pokemon Details
        return jsonify(pokemondata)


# Running Server
if __name__ == "__main__":
    db.create_all()
    app.run(host="localhost", port=8006, debug=True)
