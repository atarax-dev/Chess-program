from datetime import datetime

from controllers.tournament_controller import create_and_launch_tournament
from models.player_model import Player
from models.tournament_model import Tournament


def show_tournament_details(tournament):
    return tournament.name, tournament.place, tournament.date, tournament.rounds_list, tournament.players_list, \
           tournament.timecontrol, tournament.description, tournament.number_of_rounds


def show_player_details(player):
    return player.last_name, player.first_name, player.birth_date, player.gender


def show_tournament_sorted_results(tournament):
    tournament.sort_players_score()
    for player in tournament.players_list:
        print(player.first_name + " " + str(player.score) + " " + str(player.rank))


def show_tournament_current_rounds_list(tournament):
    print(tournament.current_round)
    print(tournament.rounds_list[tournament.current_round-1].match_list)


def show_menu(menu_list):
    for path_fonction in menu_list:
        for (key, value) in path_fonction.items():
            print(key)
    user_input = int(input("Quel est votre choix? "))
    for (key, value) in menu_list[user_input-1].items():
        return value()


def show_main_menu():
    main_menu_list = [{"[1]. Lancer un tournoi\n": show_tournament_menu},
                      {"[2]. Accéder à la base de données\n": show_database_menu}]
    print("Bienvenue dans le programme de tournois\n")
    show_menu(main_menu_list)


def show_tournament_menu():
    tournament_menu_list = [{"[1]. Créer un nouveau tournoi\n": create_and_launch_tournament},
                            {"[2]. Charger un tournoi inachevé\n": "load_tournament"},
                            # TODO charger tournoi existant dans la db
                            {"[3]. Retour\n": show_main_menu}]
    show_menu(tournament_menu_list)


def show_new_tournament_menu(tournament):
    new_tournament_menu_list = [{"[1]. Ajouter un nouveau joueur\n": "add_player_to_tournament"},
                                {"[2]. Ajouter un joueur existant\n": "add_existing_player_to_tournament"},
                                # TODO ajouter joueur existant dans la db pour le tournoi
                                {"[3]. Retour\n": show_tournament_menu}]

    for path_fonction in new_tournament_menu_list:
        for (key, value) in path_fonction.items():
            print(key)
    user_input = int(input("Quel est votre choix? "))
    if user_input == 1:
        add_player_to_tournament(tournament)
    elif user_input == 2:
        # TODO rappel fonction ajouter joueur existant
        pass
    elif user_input == 3:
        show_tournament_menu()


def create_tournament():
    name = input("Quel est le nom du tournoi? ")
    place = input("Où se joue t'il? ")
    date = datetime.now()
    time_control = input("Quel mode de jeu? (Bullet, Blitz, Rapide) ")
    description = input("Ecrivez ici les remarques du tournoi ")
    return Tournament(name=name, place=place, date=date, time_control=time_control, description=description)


def add_player_to_tournament(tournament):
    last_name = input("Veuillez entrez le nom de famille du joueur ")
    first_name = input("Veuillez entrez le prénom du joueur ")
    birth_date = input("Veuillez entrez la date de naissance du joueur au format jjmmaa ")
    gender = input("Veuillez entrez le genre du joueur M(ale)/F(emale)/O(thers) ")
    rank = int(input("Veuillez entrez le classement du joueur "))
    new_player = Player(last_name, first_name, birth_date, gender, rank)
    tournament.add_player(new_player)
    # TODO fonction save player dans db
    # TODO fonction save tournoi dans db


def show_database_menu():
    database_menu_list = [{"[1]. Créer un nouveau joueur\n": "add_new_player_to_db"},
                          # TODO add joueur db
                          {"[2]. Modifier un joueur\n": "modify_player_in_db"},
                          # TODO mod joueur db
                          {"[3]. Afficher tous les joueurs de la base de données\n": "show_all_players_in_db"},
                          # TODO afficher tous les joueurs en db
                          {"[4]. Afficher tous les tournois\n": "show_all_tournaments_in_db"},
                          # TODO afficher tous les tournois en db
                          {"[5]. Afficher les joueurs d'un tournoi\n": "show_players_in_tournament"},
                          # TODO afficher les joueurs d'un tournoi en db
                          {"[6]. Afficher les rondes d'un tournoi\n": "show_rounds_in_tournament"},
                          # TODO afficher les rondes d'un tournoi en db
                          {"7]. Afficher les matchs d'un tournoi\n": "show_matchs_in_tournament"},
                          # TODO afficher les matchs d'un tournoi en db
                          {"[8]. Retour\n": show_main_menu}]
    show_menu(database_menu_list)
