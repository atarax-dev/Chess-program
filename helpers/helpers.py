from tinydb import TinyDB

from controllers.player_controller import save_player_in_db, load_player_from_db, run_modify_player_menu, \
    create_player_from_json, sort_players_list
from controllers.tournament_controller import save_tournament_in_db, run_add_players_menu, update_tournament_in_db, \
    launch_tournament, load_tournament_from_db
from views.views import ask_continue_or_quit, show_menu, main_menu_list, tournament_menu_list, \
    ask_tournament_attributes, show_tournaments_from_db, ask_for_choice, database_menu_list, ask_player_attributes, \
    show_players_from_db, show_rounds, show_players_menu_list, show_players_in_players_list


def continue_or_quit():
    """
Permet de continuer l'action en cours ou de retourner au menu principal
    """
    user_choice = 0
    while not is_valid_entry(user_choice, ["o", "n"]):
        user_choice = ask_continue_or_quit()
    if user_choice == "o":
        pass
    elif user_choice == "n":
        run_main_menu()


def run_main_menu():
    """
Lance le menu principal
    """
    user_choice = 0
    while not is_valid_entry(user_choice, [1, 2]):
        user_choice = show_menu(main_menu_list)
    if user_choice == 1:  # Lancer ou reprendre un tournoi
        run_tournament_menu()
    elif user_choice == 2:  # Accéder à la base de données
        run_database_menu()


def run_tournament_menu():
    """
Lance le menu de création ou reprise d'un tournoi
    """
    user_choice = 0
    while not is_valid_entry(user_choice, [1, 2, 3]):
        user_choice = show_menu(tournament_menu_list)
    if user_choice == 1:  # Créer un nouveau tournoi
        tournament1 = ask_tournament_attributes()
        save_tournament_in_db(tournament1)
        while len(tournament1.players_list) < 8:
            print(f"Il manque {8 - len(tournament1.players_list)} joueurs")
            run_add_players_menu(tournament1)
            update_tournament_in_db(tournament1)
        launch_tournament(tournament1)
        run_main_menu()
    elif user_choice == 2:  # Charger un tournoi inachevé
        db = TinyDB("db.json")
        raw_tournaments_table = db.table("tournaments")
        tournaments_table = []
        for tournament in raw_tournaments_table:
            tournaments_table.append(tournament)
        show_tournaments_from_db()
        choice = ask_for_choice()
        menu_range = get_range_list(tournaments_table)
        while choice not in menu_range:
            choice = ask_for_choice()
        tournament = load_tournament_from_db(tournaments_table[choice-1]["name"], tournaments_table[choice-1]["place"])
        while len(tournament.players_list) < 8:
            print(f"Il manque {8 - len(tournament.players_list)} joueurs")
            run_add_players_menu(tournament)
            update_tournament_in_db(tournament)
        launch_tournament(tournament)
        run_main_menu()
    elif user_choice == 3:  # Retour
        run_main_menu()


def get_range_list(menu_list):
    """
Permet d'obtenir une liste des indices entiers de la liste du menu à partir de 1
    :param menu_list: liste d'un menu
    :return: liste contenant plusieurs int
    """
    menu_range = []
    i = 1
    for ranged in range(len(menu_list) + 1):
        menu_range.append(i)
        i += 1
    return menu_range


def run_database_menu():
    """
Lance le menu de la base de données
    """
    user_choice = 0
    while not is_valid_entry(user_choice, [1, 2, 3, 4, 5, 6, 7, 8]):
        user_choice = show_menu(database_menu_list)
    if user_choice == 1:  # Créer un nouveau joueur
        player = ask_player_attributes()
        save_player_in_db(player)
        run_database_menu()
    elif user_choice == 2:  # Modifier un joueur
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
    elif user_choice == 3:  # Afficher tous les joueurs de la base de données
        db = TinyDB("db.json")
        players_table = db.table("players")
        players_list = []
        for json_player in players_table:
            player = create_player_from_json(json_player)
            players_list.append(player)
        run_show_players_menu(players_list)
        continue_or_quit()
        run_database_menu()
    elif user_choice == 4:  # Afficher tous les tournois de la base de données
        show_tournaments_from_db()
        continue_or_quit()
        run_database_menu()
    elif user_choice == 5:  # Afficher les joueurs d'un tournoi
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
        run_show_players_menu(tournament.players_list)
        continue_or_quit()
        run_database_menu()
    elif user_choice == 6:  # Afficher les rondes d'un tournoi
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
    elif user_choice == 7:  # Afficher les matchs d'un tournoi
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
    elif user_choice == 8:  # Retour
        run_main_menu()


def run_show_players_menu(players_list):
    """
Lance le menu d'affichage des joueurs par ordre alphabétique ou par classement
    """
    choice = show_menu(show_players_menu_list)
    if choice == 1:  # Afficher par ordre alphabetique
        sorted_players_list = sort_players_list("alpha", players_list)
        show_players_in_players_list(sorted_players_list)
        continue_or_quit()
        run_show_players_menu(players_list)
    elif choice == 2:  # Afficher par classement
        sorted_players_list = sort_players_list("rank", players_list)
        show_players_in_players_list(sorted_players_list)
        continue_or_quit()
        run_show_players_menu(players_list)
    elif choice == 3:  # Retour
        run_database_menu()


def is_valid_entry(user_input, valid_choice_list):
    """
Détermine si l'entrée utilisateur est valide
    :param user_input: int
    :param valid_choice_list: listes d'entiers pour un choix valide
    :return: bool
    """
    if user_input in valid_choice_list:
        return True
    else:
        return False
