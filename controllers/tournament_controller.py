from datetime import datetime

from tinydb import TinyDB, Query

from controllers.player_controller import save_player_in_db, create_player_from_json
from controllers.round_controller import create_round_from_json
from helpers.helpers import convert_str_to_datetime
from models.tournament_model import Tournament
from views.views import show_tournament_current_rounds_list, show_tournament_sorted_results, ask_continue_or_quit, \
    show_menu, main_menu_list, tournament_menu_list, ask_tournament_attributes, add_players_menu_list, \
    ask_player_attributes, database_menu_list, ask_for_scores


def launch_tournament(tournament):
    while tournament.current_round <= tournament.number_of_rounds:
        tournament.generate_swiss_pairs()
        show_tournament_current_rounds_list(tournament)
        enter_scores(tournament)
        show_tournament_sorted_results(tournament)
        continue_or_quit()


def enter_scores(tournament):
    i = tournament.current_round - 1
    for versus in tournament.rounds_list[i].match_list:
        if versus.result1 == 0 and versus.result2 == 0:
            result = 0
            while not is_valid_entry(result, ["1", "2", "n"]):
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
            if versus != tournament.rounds_list[i].match_list[3]:
                continue_or_quit()
        tournament.rounds_list[i].end_date = datetime.now()
        tournament.current_round += 1
        # TODO fonction save tournoi dans db


def continue_or_quit():
    user_choice = 0
    while not is_valid_entry(user_choice, ["o", "n"]):
        user_choice = ask_continue_or_quit()
    if user_choice == "o":
        pass
    elif user_choice == "n":
        run_main_menu()


def run_main_menu():
    user_choice = 0
    while not is_valid_entry(user_choice, [1, 2]):
        user_choice = show_menu(main_menu_list)
    if user_choice == 1:
        run_tournament_menu()
    elif user_choice == 2:
        run_database_menu()


def run_tournament_menu():
    user_choice = 0
    while not is_valid_entry(user_choice, [1, 2, 3]):
        user_choice = show_menu(tournament_menu_list)
    if user_choice == 1:
        tournament1 = ask_tournament_attributes()
        while len(tournament1.players_list) < 8:
            print(f"Il manque {8 - len(tournament1.players_list)} joueurs")
            run_add_players_menu(tournament1)
        launch_tournament(tournament1)
        run_main_menu()
    elif user_choice == 2:
        # TODO afficher tous les tournois
        # TODO input choix
        # TODO fonction charger tournoi inachevé
        pass
    elif user_choice == 3:
        run_main_menu()


def run_add_players_menu(tournament):
    user_choice = 0
    while not is_valid_entry(user_choice, [1, 2, 3]):
        user_choice = show_menu(add_players_menu_list)
    if user_choice == 1:
        new_player = ask_player_attributes()
        tournament.add_player(new_player)
        save_player_in_db(new_player)
        # TODO fonction save tournoi dans db
    elif user_choice == 2:
        # TODO afficher la liste des joueurs en db
        # TODO demander quel joueur
        # TODO chercher ce joueur et l'ajouter au tournoi
        pass
    elif user_choice == 3:
        run_main_menu()


def run_database_menu():
    user_choice = 0
    while not is_valid_entry(user_choice, [1, 2, 3, 4, 5, 6, 7, 8]):
        user_choice = show_menu(database_menu_list)
    if user_choice == 1:
        player = ask_player_attributes()
        save_player_in_db(player)
    elif user_choice == 2:
        # TODO mod joueur db
        pass
    elif user_choice == 3:
        # TODO afficher tous les joueurs en db
        pass
    elif user_choice == 4:
        # TODO afficher tous les tournois en db
        pass
    elif user_choice == 5:
        # TODO afficher les joueurs d'un tournoi en db
        pass
    elif user_choice == 6:
        # TODO afficher les rondes d'un tournoi en db
        pass
    elif user_choice == 7:
        # TODO afficher les matchs d'un tournoi en db
        pass
    elif user_choice == 8:
        run_main_menu()


def is_valid_entry(user_input, valid_choice_list):
    if user_input in valid_choice_list:
        return True
    else:
        return False


def load_tournament_from_db(name, place):
    db = TinyDB("db.json")
    tournaments_table = db.table("tournaments")
    tournament = Query()
    result = tournaments_table.search(tournament.name == f"{name}" and tournament.place == f"{place}")
    tournament = create_tournament_from_json(result[0])
    return tournament


def save_tournament_in_db(tournament_object):
    data = tournament_object.get_json()
    db = TinyDB("db.json")
    tournaments_table = db.table("tournaments")
    tournaments_table.insert(data)


def update_tournament_in_db(tournament):
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
                   ({"current_round": json_tournament["current_round"]}, tournament_entry.name == str(result[0]["name"])
                    and tournament_entry.place == str(result[0]["place"]))]

    tournaments_table.update_multiple(update_list)


def create_tournament_from_json(json_tournament):
    name = json_tournament["name"]
    place = json_tournament["place"]
    date = convert_str_to_datetime(json_tournament["date"])
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
    return Tournament(name, place, date, time_control, description, players_list,
                      number_of_rounds, rounds_list, current_round)
