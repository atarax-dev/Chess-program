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


def show_main_menu():
    print("Bienvenue dans le programme de tournois\n"
          "[1]. Lancer un tournoi\n"
          "[2]. Accéder à la base de données\n")


def show_tournament_menu():
    print("[1]. Créer un nouveau tournoi\n"
          "[2]. Charger un tournoi inachevé\n"
          "[3]. Retour\n")


def show_database_menu():
    print("[1]. Ajouter un nouveau joueur\n"
          "[2]. Modifier un joueur\n"
          "[3]. Afficher tous les joueurs de la base de données\n"
          "[4]. Afficher tous les tournois\n"
          "[5]. Afficher les joueurs d'un tournoi\n"
          "[6]. Afficher les rondes d'un tournoi\n"
          "[7]. Afficher les matchs d'un tournoi\n"
          "[8]. Retour\n")



