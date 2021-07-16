from datetime import datetime

from tinydb import TinyDB, Query

from controllers.player_controller import save_player_in_db, create_player_from_json, load_player_from_db, \
    update_player_in_db
from controllers.round_controller import create_round_from_json
from helpers import helpers
from models.tournament_model import Tournament
from views.views import show_tournament_current_rounds_list, show_tournament_sorted_results, show_menu, \
    add_players_menu_list, ask_player_attributes, ask_for_scores, ask_for_choice, show_players_from_db


def launch_tournament(tournament):
    """
Lance ou reprend le tournoi tant qu'il n'est pas terminé
    :param tournament: instance de tournoi
    """
    while tournament.current_round <= tournament.number_of_rounds:
        if tournament.current_round == 0 and len(tournament.rounds_list) == 0:
            tournament.generate_swiss_pairs()
        if not len(tournament.rounds_list) >= tournament.current_round:
            tournament.generate_swiss_pairs()
        update_tournament_in_db(tournament)
        show_tournament_current_rounds_list(tournament)
        helpers.continue_or_quit()
        enter_scores(tournament)
        show_tournament_sorted_results(tournament)
        helpers.continue_or_quit()
    if tournament.current_round == 5:
        for player in tournament.players_list:
            player.score = 0
            update_player_in_db(player, "first_name")


def enter_scores(tournament):
    """
Permet de mettre à jour le score des joueurs après avoir entré le résultat d'un match
    :param tournament: instance de tournoi
    """
    i = tournament.current_round - 1
    if str(tournament.date.date()) != str(datetime.now().date()) \
            and not (str(datetime.now().date()) in tournament.date_list):
        tournament.date_list.append(str(datetime.now().date()))
    for versus in tournament.rounds_list[i].match_list:
        if versus.result1 == 0 and versus.result2 == 0:
            result = 0
            while not helpers.is_valid_entry(result, ["1", "2", "n"]):
                result = ask_for_scores(versus)
            if result == "1":
                versus.player1.score += 1
                versus.result1 = 1
                versus.result2 = 0
            elif result == "2":
                versus.player2.score += 1
                versus.result1 = 0
                versus.result2 = 1
            elif result == "n":
                versus.player1.score += 0.5
                versus.result1 = 0.5
                versus.player2.score += 0.5
                versus.result2 = 0.5
            update_tournament_in_db(tournament)
            if versus != tournament.rounds_list[i].match_list[3]:
                helpers.continue_or_quit()
        tournament.rounds_list[i].end_date = datetime.now()
    tournament.current_round += 1
    update_tournament_in_db(tournament)


def run_add_players_menu(tournament):
    """
Lance le menu d'ajout des joueurs au tournoi
    :param tournament: instance de tournoi
    """
    user_choice = 0
    while not helpers.is_valid_entry(user_choice, [1, 2, 3]):
        user_choice = show_menu(add_players_menu_list)
    if user_choice == 1:  # Ajouter un nouveau joueur
        new_player = ask_player_attributes()
        tournament.add_player(new_player)
        save_player_in_db(new_player)
        update_tournament_in_db(tournament)
    elif user_choice == 2:  # Ajouter un joueur existant
        show_players_from_db()
        db = TinyDB("db.json")
        raw_players_table = db.table("players")
        players_table = []
        for player in raw_players_table:
            players_table.append(player)
        choice = ask_for_choice()
        menu_range = helpers.get_range_list(players_table)
        while choice not in menu_range:
            ask_for_choice()
        player = load_player_from_db(players_table[choice - 1]["first_name"], players_table[choice - 1]["last_name"])
        tournament.players_list.append(player)
    elif user_choice == 3:  # Retour
        helpers.run_main_menu()


def load_tournament_from_db(name, place):
    """
Crée un objet tournoi à partir de la base de données
    :param name: str
    :param place: str
    :return: instance de tournoi
    """
    db = TinyDB("db.json")
    tournaments_table = db.table("tournaments")
    tournament = Query()
    result = tournaments_table.search(tournament.name == f"{name}" and tournament.place == f"{place}")
    tournament = create_tournament_from_json(result[0])
    return tournament


def save_tournament_in_db(tournament_object):
    """
Sauvegarde un tournoi en base de données
    :param tournament_object: instance de tournoi
    """
    data = tournament_object.get_json()
    db = TinyDB("db.json")
    tournaments_table = db.table("tournaments")
    tournaments_table.insert(data)


def update_tournament_in_db(tournament):
    """
Met à jour les informations d'un tournoi dans la base de données
    :param tournament: instance de tournoi
    """
    db = TinyDB("db.json")
    tournaments_table = db.table("tournaments")
    tournament_entry = Query()
    result = tournaments_table.search((tournament_entry.name == f"{tournament.name}"
                                       and tournament_entry.place == f"{tournament.place}"))
    json_tournament = tournament.get_json()

    update_list = [({"name": json_tournament["name"]}, tournament_entry.name == str(result[0]["name"])
                    and tournament_entry.place == str(result[0]["place"])),
                   ({"place": json_tournament["place"]}, tournament_entry.name == str(result[0]["name"])
                    and tournament_entry.place == str(result[0]["place"])),
                   ({"date": json_tournament["date"]}, tournament_entry.name == str(result[0]["name"])
                    and tournament_entry.place == str(result[0]["place"])),
                   ({"time_control": json_tournament["time_control"]}, tournament_entry.name == str(result[0]["name"])
                    and tournament_entry.place == str(result[0]["place"])),
                   ({"description": json_tournament["description"]}, tournament_entry.name == str(result[0]["name"])
                    and tournament_entry.place == str(result[0]["place"])),
                   ({"players_list": json_tournament["players_list"]}, tournament_entry.name == str(result[0]["name"])
                    and tournament_entry.place == str(result[0]["place"])),
                   ({"number_of_rounds": json_tournament["number_of_rounds"]},
                    tournament_entry.name == str(result[0]["name"])
                    and tournament_entry.place == str(result[0]["place"])),
                   ({"rounds_list": json_tournament["rounds_list"]}, tournament_entry.name == str(result[0]["name"])
                    and tournament_entry.place == str(result[0]["place"])),
                   ({"current_round": json_tournament["current_round"]},
                    tournament_entry.name == str(result[0]["name"])
                    and tournament_entry.place == str(result[0]["place"])),
                   ({"date_list": json_tournament["date_list"]}, tournament_entry.name == str(result[0]["name"])
                    and tournament_entry.place == str(result[0]["place"]))]

    tournaments_table.update_multiple(update_list)


def create_tournament_from_json(json_tournament):
    """
Crée une instance de tournoi à partir d'un json
    :param json_tournament: json
    :return: instance de tournoi
    """
    name = json_tournament["name"]
    place = json_tournament["place"]
    date = datetime.strptime(json_tournament["date"], "%Y-%m-%d %H:%M:%S")
    time_control = json_tournament["time_control"]
    json_players_list = json_tournament["players_list"]
    players_list = []
    for json_player in json_players_list:
        player = create_player_from_json(json_player)
        players_list.append(player)
    json_rounds_list = json_tournament["rounds_list"]
    rounds_list = []
    for json_round in json_rounds_list:
        generated_round = create_round_from_json(json_round)
        rounds_list.append(generated_round)
    number_of_rounds = json_tournament["number_of_rounds"]
    description = json_tournament["description"]
    current_round = json_tournament["current_round"]
    date_list = json_tournament["date_list"]
    return Tournament(name, place, date, time_control, description, players_list,
                      number_of_rounds, rounds_list, date_list, current_round)
