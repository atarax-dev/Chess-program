from datetime import datetime

from tinydb import TinyDB, Query

from controllers.player_controller import save_player_in_db, create_player_from_json, load_player_from_db, \
    update_player_in_db, sort_players_list
from controllers.round_controller import create_round_from_json
from models.tournament_model import Tournament
from views.views import show_tournament_current_rounds_list, show_tournament_sorted_results, ask_continue_or_quit, \
    show_menu, main_menu_list, tournament_menu_list, ask_tournament_attributes, add_players_menu_list, \
    ask_player_attributes, database_menu_list, ask_for_scores, show_tournaments_from_db, ask_for_choice, \
    show_players_from_db, show_players, show_rounds, modify_player_menu_list, ask_new_first_name, ask_new_last_name, \
    ask_new_birth_date, ask_new_gender, ask_new_rank, show_players_menu_list, show_players_in_players_list


def launch_tournament(tournament):
    while tournament.current_round <= tournament.number_of_rounds:
        tournament.generate_swiss_pairs()
        update_tournament_in_db(tournament)
        show_tournament_current_rounds_list(tournament)
        enter_scores(tournament)
        show_tournament_sorted_results(tournament)
        continue_or_quit()
    for player in tournament.players_list:
        player.score = 0
        update_player_in_db(player)


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
            update_tournament_in_db(tournament)
            if versus != tournament.rounds_list[i].match_list[3]:
                continue_or_quit()
        tournament.rounds_list[i].end_date = datetime.now()
    tournament.current_round += 1
    update_tournament_in_db(tournament)


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
        save_tournament_in_db(tournament1)
        while len(tournament1.players_list) < 8:
            print(f"Il manque {8 - len(tournament1.players_list)} joueurs")
            run_add_players_menu(tournament1)
            update_tournament_in_db(tournament1)
        launch_tournament(tournament1)
        run_main_menu()
    elif user_choice == 2:
        db = TinyDB("db.json")
        raw_tournaments_table = db.table("tournaments")
        tournaments_table = []
        for tournament in raw_tournaments_table:
            tournaments_table.append(tournament)
        show_tournaments_from_db()
        choice = ask_for_choice()
        menu_range = get_range_list(tournaments_table)
        while choice not in menu_range:
            ask_for_choice()
        tournament = load_tournament_from_db(tournaments_table[choice-1]["name"], tournaments_table[choice-1]["place"])
        while len(tournament.players_list) < 8:
            print(f"Il manque {8 - len(tournament.players_list)} joueurs")
            run_add_players_menu(tournament)
            update_tournament_in_db(tournament)
        launch_tournament(tournament)
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
        update_tournament_in_db(tournament)
    elif user_choice == 2:
        show_players_from_db()
        db = TinyDB("db.json")
        raw_players_table = db.table("players")
        players_table = []
        for player in raw_players_table:
            players_table.append(player)
        choice = ask_for_choice()
        menu_range = get_range_list(players_table)
        while choice not in menu_range:
            ask_for_choice()
        player = load_player_from_db(players_table[choice - 1]["first_name"], players_table[choice - 1]["last_name"])
        tournament.players_list.append(player)
    elif user_choice == 3:
        run_main_menu()


def get_range_list(menu_list):
    menu_range = []
    i = 1
    for ranged in range(len(menu_list) + 1):
        menu_range.append(i)
        i += 1
    return menu_range


def run_database_menu():
    user_choice = 0
    while not is_valid_entry(user_choice, [1, 2, 3, 4, 5, 6, 7, 8]):
        user_choice = show_menu(database_menu_list)
    if user_choice == 1:
        player = ask_player_attributes()
        save_player_in_db(player)
        run_database_menu()
    elif user_choice == 2:
        show_players_from_db()
        db = TinyDB("db.json")
        raw_players_table = db.table("players")
        players_table = []
        for player in raw_players_table:
            players_table.append(player)
        choice = ask_for_choice()
        menu_range = get_range_list(players_table)
        while choice not in menu_range:
            ask_for_choice()
        player = load_player_from_db(players_table[choice - 1]["first_name"], players_table[choice - 1]["last_name"])
        run_modify_player_menu(player)
    elif user_choice == 3:
        run_show_players_menu()
        continue_or_quit()
        run_database_menu()
    elif user_choice == 4:
        show_tournaments_from_db()
        continue_or_quit()
        run_database_menu()
    elif user_choice == 5:
        db = TinyDB("db.json")
        raw_tournaments_table = db.table("tournaments")
        tournaments_table = []
        for tournament in raw_tournaments_table:
            tournaments_table.append(tournament)
        show_tournaments_from_db()
        choice = ask_for_choice()
        menu_range = get_range_list(tournaments_table)
        while choice not in menu_range:
            ask_for_choice()
        tournament = load_tournament_from_db(tournaments_table[choice - 1]["name"],
                                             tournaments_table[choice - 1]["place"])
        show_players(tournament.players_list)
        continue_or_quit()
        run_database_menu()
    elif user_choice == 6:
        db = TinyDB("db.json")
        raw_tournaments_table = db.table("tournaments")
        tournaments_table = []
        for tournament in raw_tournaments_table:
            tournaments_table.append(tournament)
        show_tournaments_from_db()
        choice = ask_for_choice()
        menu_range = get_range_list(tournaments_table)
        while choice not in menu_range:
            ask_for_choice()
        tournament = load_tournament_from_db(tournaments_table[choice - 1]["name"],
                                             tournaments_table[choice - 1]["place"])
        show_rounds(tournament.rounds_list)
        continue_or_quit()
        run_database_menu()
    elif user_choice == 7:
        db = TinyDB("db.json")
        raw_tournaments_table = db.table("tournaments")
        tournaments_table = []
        for tournament in raw_tournaments_table:
            tournaments_table.append(tournament)
        show_tournaments_from_db()
        choice = ask_for_choice()
        menu_range = get_range_list(tournaments_table)
        while choice not in menu_range:
            ask_for_choice()
        tournament = load_tournament_from_db(tournaments_table[choice - 1]["name"],
                                             tournaments_table[choice - 1]["place"])
        show_rounds(tournament.rounds_list)
        continue_or_quit()
        run_database_menu()
    elif user_choice == 8:
        run_main_menu()


def run_modify_player_menu(player):
    user_choice = 0
    while not is_valid_entry(user_choice, [1, 2, 3, 4, 5, 6]):
        user_choice = show_menu(modify_player_menu_list)
    if user_choice == 1:
        new_last_name = ask_new_last_name()
        player.last_name = new_last_name
        update_player_in_db(player, "last_name")
        run_database_menu()
    elif user_choice == 2:
        new_first_name = ask_new_first_name()
        player.first_name = new_first_name
        update_player_in_db(player, "first_name")
        run_database_menu()
    elif user_choice == 3:
        new_birth_date = ask_new_birth_date()
        player.birth_date = new_birth_date
        update_player_in_db(player, "birth_date")
        run_database_menu()
    elif user_choice == 4:
        new_gender = ask_new_gender()
        player.gender = new_gender
        update_player_in_db(player, "gender")
        run_database_menu()
    elif user_choice == 5:
        new_rank = ask_new_rank()
        player.rank = new_rank
        update_player_in_db(player, "rank")
        run_database_menu()
    elif user_choice == 6:
        run_database_menu()


def run_show_players_menu():
    choice = show_menu(show_players_menu_list)
    db = TinyDB("db.json")
    players_table = db.table("players")
    players_list = []
    for player in players_table:
        players_list.append(player)
    if choice == 1:
        sorted_players_list = sort_players_list("alpha", players_list)
        show_players_in_players_list(sorted_players_list)
        continue_or_quit()
        run_show_players_menu()
    elif choice == 2:
        sorted_players_list = sort_players_list("rank", players_list)
        show_players_in_players_list(sorted_players_list)
        continue_or_quit()
        run_show_players_menu()
    elif choice == 3:
        run_database_menu()


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
    return Tournament(name, place, date, time_control, description, players_list,
                      number_of_rounds, rounds_list, current_round)
