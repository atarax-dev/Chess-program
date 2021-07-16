from datetime import datetime
from operator import attrgetter

from tinydb import TinyDB, Query

from helpers import helpers
from models.player_model import Player
from views.views import show_menu, modify_player_menu_list, ask_new_last_name, ask_new_first_name, ask_new_birth_date, \
    ask_new_gender, ask_new_rank


def load_player_from_db(first_name, last_name):
    """
Crée un objet joueur à partir de la base de données
    :param first_name: str
    :param last_name: str
    :return: instance de joueur
    """
    db = TinyDB("db.json")
    players_table = db.table("players")
    player = Query()
    result = players_table.search(player.last_name == f"{last_name}" and player.first_name == f"{first_name}")
    player = create_player_from_json(result[0])
    return player


def save_player_in_db(player_object):
    """
Sauvegarde un joueur en base de données
    :param player_object: instance de joueur
    """
    data = player_object.get_json()
    db = TinyDB("db.json")
    players_table = db.table("players")
    players_table.insert(data)


def update_player_in_db(player, attribute_to_modify):
    """
Met à jour les informations d'un joueur dans la base de données
    :param player: instance de joueur
    :param attribute_to_modify: attribut à modifier
    """
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
    """
Crée une instance de joueur à partir d'un json
    :param json_player: json
    :return: instance de joueur
    """
    last_name = json_player["last_name"]
    birth_date = datetime.strptime(json_player["birth_date"], "%Y-%m-%d").date()
    first_name = json_player["first_name"]
    gender = json_player["gender"]
    rank = int(json_player["rank"])
    score = json_player["score"]
    return Player(last_name, first_name, birth_date, gender, rank, score)


def sort_players_list(method, players_list):
    """
Trie une liste de joueurs
    :param method: str ("rank" ou "alpha")
    :param players_list: liste d'instances de joueur
    :return: sorted list
    """
    if method == "rank":
        sorted_players_list = sorted(players_list, reverse=True, key=attrgetter("rank"))
        return sorted_players_list
    elif method == "alpha":
        sorted_players_list = sorted(players_list, reverse=False, key=attrgetter("last_name"))
        return sorted_players_list


def run_modify_player_menu(player):
    """
Lance le menu de modification d'un joueur
    :param player: instance de joueur
    """
    user_choice = 0
    while not helpers.is_valid_entry(user_choice, [1, 2, 3, 4, 5, 6]):
        user_choice = show_menu(modify_player_menu_list)
    if user_choice == 1:  # Modifier le nom
        new_last_name = ask_new_last_name()
        player.last_name = new_last_name
        update_player_in_db(player, "last_name")
        helpers.run_database_menu()
    elif user_choice == 2:  # Modifier le prenom
        new_first_name = ask_new_first_name()
        player.first_name = new_first_name
        update_player_in_db(player, "first_name")
        helpers.run_database_menu()
    elif user_choice == 3:  # Modifier la date de naissance
        new_birth_date = ask_new_birth_date()
        player.birth_date = new_birth_date
        update_player_in_db(player, "birth_date")
        helpers.run_database_menu()
    elif user_choice == 4:  # Modifier le genre
        new_gender = ask_new_gender()
        player.gender = new_gender
        update_player_in_db(player, "gender")
        helpers.run_database_menu()
    elif user_choice == 5:  # Modifier le classement
        new_rank = ask_new_rank()
        player.rank = new_rank
        update_player_in_db(player, "rank")
        helpers.run_database_menu()
    elif user_choice == 6:  # Retour
        helpers.run_database_menu()
