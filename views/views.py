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
                      "[7]. Afficher les matchs d'un tournoi\n",
                      "[8]. Retour\n"]

modify_player_menu_list = ["[1]. Modifier le nom\n",
                           "[2]. Modifier le prenom\n",
                           "[3]. Modifier la date de naissance\n",
                           "[4]. Modifier le genre\n",
                           "[5]. Modifier le classement\n",
                           "[6]. Retour\n"]

show_players_menu_list = ["[1]. Afficher par ordre alphabetique\n",
                          "[2]. Afficher par classement\n",
                          "[3]. Retour\n"]


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
    print("Round " + str(tournament.current_round))
    print(tournament.rounds_list[tournament.current_round-1].match_list)


def ask_tournament_attributes():
    name = input("Quel est le nom du tournoi? ")
    place = input("Où se joue t'il? ")
    while not place.isalpha():
        place = input("Où se joue t'il? ")
        print("Vous ne devez entrer que des lettres")
    date0 = datetime.now().strftime("%Y-%m-%d %H:%M")
    date = datetime.strptime(date0, "%Y-%m-%d %H:%M")
    time_control = input("Quel mode de jeu? (Bullet [1], Blitz [2], Rapide[3])  ")
    while time_control not in ["1", "2", "3"]:
        time_control = input("Quel mode de jeu? (Bullet [1], Blitz [2], Rapide[3])  ")
        print("Vous devez entrer 1, 2 ou 3")
    description = input("Ecrivez ici les remarques du tournoi ")
    return Tournament(name=name, place=place, date=date, time_control=time_control, description=description)


def ask_player_attributes():
    last_name = input("Veuillez entrez le nom de famille du joueur ")
    first_name = input("Veuillez entrez le prénom du joueur ")
    birth_date = input("Veuillez entrez la date de naissance du joueur au format AAAAMMJJ ")
    valid_birth_date = False
    while not valid_birth_date:
        try:
            birth_date = f"{birth_date[:4]}-{birth_date[4:6]}-{birth_date[6:8]}"
            birth_date = datetime.strptime(birth_date, "%Y-%m-%d").date()
            valid_birth_date = True
        except ValueError:
            birth_date = input("Veuillez entrez la date de naissance du joueur au format AAAAMMJJ ")
            print("Entrez la date au format AAAAMMJJ")
    gender = input("Veuillez entrez le genre du joueur M(ale)/F(emale)/O(thers) ").lower()
    while gender not in ["m", "f", "o"]:
        gender = input("Veuillez entrez le genre du joueur M(ale)/F(emale)/O(thers) ").lower()
        print("Vous devez entrer M, F ou O")
    rank = input("Veuillez entrez le classement du joueur ")
    valid_rank = False
    while not valid_rank:
        try:
            rank = int(rank)
            valid_rank = True
        except ValueError:
            rank = input("Veuillez entrez le classement du joueur ")
            print("Vous devez entrer un entier")
    return Player(last_name, first_name, birth_date, gender, rank)


def ask_for_scores(versus):
    result = str(input(f"Veuillez entrez le résultat du match {versus} (1/2/N) ")).lower()
    return result


def ask_continue_or_quit():
    answer = input("Voulez-vous continuer? O/N ").lower()
    return answer


def show_players_in_players_list(players_list):
    i = 1
    for player in players_list:
        print(f"[{i}]." + player.last_name + " " + player.first_name + " " + datetime.strftime(player.birth_date,
                                                                                               "%Y-%m-%d")
              + " " + player.gender + " " + str(player.rank))
        i += 1


def show_players_from_db():
    db = TinyDB("db.json")
    players_table = db.table("players")
    i = 1
    for player in players_table:
        print(f"[{i}.]" + player["first_name"] + " " + player["last_name"] + " " + str(player["birth_date"])
              + " " + player["gender"] + " " + str(player["rank"]))
        i += 1


def show_tournaments_from_db():
    db = TinyDB("db.json")
    tournaments_table = db.table("tournaments")
    i = 1
    for tournament in tournaments_table:
        print(f"[{i}]." + tournament["name"] + " " + tournament["place"] + " " + tournament["date"]
              + " " + tournament["time_control"])
        print(tournament["description"])
        for player in tournament["players_list"]:
            print(player["last_name"] + " " + player["first_name"] + " " + player["birth_date"]
                  + " " + player["gender"] + " " + str(player["rank"]) + " " + str(player["score"]))
        i += 1

        if tournament["current_round"] == 5:
            print("Tournoi achevé")
        else:
            print("Tournoi en cours")


def show_players(players_list):
    for player in players_list:
        print(f"{player.first_name} {player.last_name} {player.birth_date} {player.gender} {player.rank}")


def ask_for_choice():
    try:
        choice = input("Quel est votre choix? ")
        choice = int(choice)
        return choice
    except ValueError:
        ask_for_choice()
        print("Veuillez entrer un chiffre valide")


def show_rounds(rounds_list):
    for played_round in rounds_list:
        print(f"{played_round.name}")
        for match in played_round.match_list:
            print(f"{match.player1}:{match.result1} vs {match.player2}:{match.result2}")


def ask_new_last_name():
    new_last_name = input("Quel est le nouveau nom? ")
    return new_last_name


def ask_new_first_name():
    new_first_name = input("Quel est le nouveau prenom? ")
    return new_first_name


def ask_new_birth_date():
    new_birth_date = input("Entrez la nouvelle date de naissance du joueur au format AAAAMMJJ ")
    try:
        new_birth_date = f"{new_birth_date[:4]}-{new_birth_date[4:6]}-{new_birth_date[6:8]}"
        new_birth_date = datetime.strptime(new_birth_date, "%Y-%m-%d")
        return new_birth_date
    except ValueError:
        ask_new_birth_date()
        print("Entrez la date au format AAAAMMJJ")


def ask_new_gender():
    new_gender = input("Veuillez entrez le nouveau genre du joueur M(ale)/F(emale)/O(thers) ")
    try:
        new_gender = new_gender.lower()
    except ValueError:
        ask_new_gender()
    if new_gender not in ["m", "f", "o"]:
        ask_new_gender()
        print("Vous devez entrer M, F ou O")
    return new_gender


def ask_new_rank():
    new_rank = input("Veuillez entrez le classement du joueur ")
    try:
        new_rank = int(new_rank)
        return new_rank
    except ValueError:
        ask_new_rank()
        print("Vous devez entrer un entier")

