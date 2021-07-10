from datetime import datetime
from operator import attrgetter

from tinydb import TinyDB, Query

from models.player_model import Player


def load_player_from_db(first_name, last_name):
    db = TinyDB("db.json")
    players_table = db.table("players")
    player = Query()
    result = players_table.search(player.last_name == f"{last_name}" and player.first_name == f"{first_name}")
    player = create_player_from_json(result[0])
    return player


def save_player_in_db(player_object):
    data = player_object.get_json()
    db = TinyDB("db.json")
    players_table = db.table("players")
    players_table.insert(data)


def update_player_in_db(player, attribute_to_modify):
    db = TinyDB("db.json")
    players_table = db.table("players")
    user = Query()
    result = []
    if attribute_to_modify == "first_name":
        result = players_table.search(user.birth_date == f"{player.birth_date}"
                                      and user.last_name == f"{player.last_name}")
    elif attribute_to_modify == "last_name":
        result = players_table.search(user.first_name == f"{player.first_name}"
                                      and user.birth_date == f"{player.birth_date}")
    elif attribute_to_modify == "birth_date":
        result = players_table.search(user.first_name == f"{player.birth_date}"
                                      and user.last_name == f"{player.last_name}")
    elif attribute_to_modify == "gender":
        result = players_table.search(user.first_name == f"{player.birth_date}"
                                      and user.last_name == f"{player.last_name}")
    elif attribute_to_modify == "rank":
        result = players_table.search(user.first_name == f"{player.birth_date}"
                                      and user.last_name == f"{player.last_name}")

    update_list = [({"last_name": f"{player.last_name}"}, user.last_name == str(result[0]["last_name"])
                    and user.first_name == str(result[0]["first_name"])),
                   ({"first_name": f"{player.first_name}"}, user.last_name == str(result[0]["last_name"])
                    and user.first_name == str(result[0]["first_name"])),
                   ({"birth_date": datetime.strftime(player.birth_date, "%Y-%m-%d")},
                    user.last_name == str(result[0]["last_name"]) and user.first_name == str(result[0]["first_name"])),
                   ({"gender": f"{player.gender}"}, user.last_name == str(result[0]["last_name"])
                    and user.first_name == str(result[0]["first_name"])),
                   ({"rank": int(player.rank)}, user.last_name == str(result[0]["last_name"])
                    and user.first_name == str(result[0]["first_name"])),
                   ({"score": int(player.score)}, user.last_name == str(result[0]["last_name"])
                    and user.first_name == str(result[0]["first_name"]))]

    players_table.update_multiple(update_list)


def create_player_from_json(json_player):
    last_name = json_player["last_name"]
    birth_date = datetime.strptime(json_player["birth_date"], "%Y-%m-%d").date()
    first_name = json_player["first_name"]
    gender = json_player["gender"]
    rank = int(json_player["rank"])
    score = json_player["score"]
    return Player(last_name, first_name, birth_date, gender, rank, score)


def sort_players_list(method, json_players_list):
    players_list = []
    for json_player in json_players_list:
        player = create_player_from_json(json_player)
        players_list.append(player)
    if method == "rank":
        sorted_players_list = sorted(players_list, reverse=True, key=attrgetter("rank"))
        return sorted_players_list
    elif method == "alpha":
        sorted_players_list = sorted(players_list, reverse=False, key=attrgetter("last_name"))
        return sorted_players_list
