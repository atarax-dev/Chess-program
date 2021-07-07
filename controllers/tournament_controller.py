from datetime import datetime

from helpers.helpers import save_player_in_db
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
        result = ask_for_scores(versus)
        if result == "1":
            versus.player1.score += 1
            versus.result1 = 1
            versus.result2 = 0
        elif result == "2":
            versus.player2.score += 1
            versus.result1 = 0
            versus.result2 = 1
        elif result == "N":
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
    answer = ask_continue_or_quit()
    if answer.lower() == "o":
        pass
    elif answer.lower() == "n":
        run_main_menu()


def run_main_menu():
    user_choice = show_menu(main_menu_list)
    if user_choice == 1:
        run_tournament_menu()
    elif user_choice == 2:
        run_database_menu()


def run_tournament_menu():
    user_choice = show_menu(tournament_menu_list)
    if user_choice == 1:
        tournament1 = ask_tournament_attributes()
        while len(tournament1.players_list) < 8:
            print(f"Il manque {8 - len(tournament1.players_list)} joueurs")
            run_add_players_menu(tournament1)
        launch_tournament(tournament1)
        run_main_menu()
    elif user_choice == 2:
        # TODO fonction charger tournoi inachevé
        pass
    elif user_choice == 3:
        run_main_menu()


def run_add_players_menu(tournament):
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
