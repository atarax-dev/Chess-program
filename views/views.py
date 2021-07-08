from datetime import datetime

from tinydb import TinyDB

from models.player_model import Player
from models.tournament_model import Tournament


main_menu_list = ["[1]. Lancer ou reprendre un tournoi\n",
                  "[2]. Accéder à la base de données\n"]


tournament_menu_list = ["[1]. Créer un nouveau tournoi\n",
                        "[2]. Charger un tournoi inachevé\n",
                        "[3]. Retour\n"]

add_players_menu_list = ["[1]. Ajouter un nouveau joueur\n",
                         "[2]. Ajouter un joueur existant\n",
                         "[3]. Retour\n"]

database_menu_list = ["[1]. Créer un nouveau joueur\n",
                      "[2]. Modifier un joueur\n",
                      "[3]. Afficher tous les joueurs de la base de données\n",
                      "[4]. Afficher tous les tournois\n",
                      "[5]. Afficher les joueurs d'un tournoi\n",
                      "[6]. Afficher les rondes d'un tournoi\n",
                      "7]. Afficher les matchs d'un tournoi\n",
                      "[8]. Retour\n"]


def show_menu(menu_list):
    for path in menu_list:
        print(path)
    try:
        user_input = int(input("Quel est votre choix? "))
        return user_input
    except ValueError:
        show_menu(menu_list)


def show_tournament_sorted_results(tournament):
    tournament.sort_players_score()
    for player in tournament.players_list:
        print(player.first_name + " " + str(player.score) + " " + str(player.rank))


def show_tournament_current_rounds_list(tournament):
    print(tournament.current_round)
    print(tournament.rounds_list[tournament.current_round-1].match_list)


def ask_tournament_attributes():
    name = input("Quel est le nom du tournoi? ")
    place = input("Où se joue t'il? ")
    date = datetime.now()
    time_control = input("Quel mode de jeu? (Bullet, Blitz, Rapide) ")
    description = input("Ecrivez ici les remarques du tournoi ")
    return Tournament(name=name, place=place, date=date, time_control=time_control, description=description)


def ask_player_attributes():
    last_name = input("Veuillez entrez le nom de famille du joueur ")
    first_name = input("Veuillez entrez le prénom du joueur ")
    birth_date = input("Veuillez entrez la date de naissance du joueur au format jjmmaa ")
    gender = input("Veuillez entrez le genre du joueur M(ale)/F(emale)/O(thers) ")
    rank = int(input("Veuillez entrez le classement du joueur "))
    return Player(last_name, first_name, birth_date, gender, rank)


def ask_for_scores(versus):
    result = str(input(f"Veuillez entrez le résultat du match {versus} (1/2/N) ")).lower()
    return result


def ask_continue_or_quit():
    answer = input("Voulez-vous continuer? O/N ").lower()
    return answer


def show_players_from_db():
    players = TinyDB("db.json")
    for player in players:
        print(player)
