from flask import Flask,request,json,jsonify
from flask_sqlalchemy import SQLAlchemy
import os

app=Flask(__name__)
basedir=os.path.abspath(os.path.dirname(__file__))

app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///'+os.path.join(basedir,'db.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICAIONS']=False

db=SQLAlchemy(app)

class Pokemon(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(500),unique=True)
    sprite=db.Column(db.String,unique=True)
    fg=db.Column(db.String)
    bg=db.Column(db.String)
    desc=db.Column(db.String)

    def __init__(self,name,sprite,fg,bg,desc):
        self.name=name
        self.sprite=sprite
        self.fg=fg
        self.bg=bg
        self.desc=desc

@app.route('/api/pokemon',methods=['POST'])
def create_pokemon():
    name=request.json['name']
    sprite=request.json['sprite']
    fg=request.json['fg']
    bg=request.json['bg']
    desc=request.json['desc']
    pokemondata=Pokemon(name,sprite,fg,bg,desc)
    db.session.add(pokemondata)
    db.session.commit()
    return get_pokemon(id),201

@app.route("/api/pokemon/<int:id>")
def get_pokemon(id) : 
    result = pokemon.query.filter(Pokemon.id == id).first()
    data={}
    data['pokemon'] = {}
    data['pokemon']['id']=result.id
    data['pokemon']['name']=result.name
    data['pokemon']['sprite']=result.sprite
    data['pokemon']['cardColours']={}
    data['pokemon']['cardColours']['fg']=result.fg
    data['pokemon']['cardColours']['bg']=result.bg
    data['pokemon']['cardColours']['desc']=result.desc
    return jsonify(data)

if __name__ == '__main__':
    app.run(host='localhost',port=8006,debug=True)