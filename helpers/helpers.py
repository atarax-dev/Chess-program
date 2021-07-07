from tinydb import TinyDB, Query

from models.player_model import Player


def save_player_in_db(player):
    data = player.get_json()
    db = TinyDB("db.json")
    db.insert(data)


def load_player_from_db(first_name, last_name):
    db = TinyDB("db.json")
    player = Query()
    result = db.search(player.last_name == f"{last_name}" and player.first_name == f"{first_name}")
    last_name = result[0]["last_name"]
    first_name = result[0]["first_name"]
    birth_date = result[0]["birth_date"]
    gender = result[0]["gender"]
    rank = result[0]["rank"]
    score = result[0]["score"]
    return Player(last_name, first_name, birth_date, gender, rank, score)
