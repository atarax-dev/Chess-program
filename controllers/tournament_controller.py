from controllers.round_controller import enter_scores
from views import views


def launch_tournament(tournament):
    while len(tournament.players_list) < 8:
        print(f"Il manque {8 - len(tournament.players_list)} joueurs")
        views.show_new_tournament_menu(tournament)
    while tournament.current_round <= tournament.number_of_rounds:
        tournament.generate_swiss_pairs()
        views.show_tournament_current_rounds_list(tournament)
        enter_scores(tournament)
        views.show_tournament_sorted_results(tournament)


def create_and_launch_tournament():
    tournament1 = views.create_tournament()
    launch_tournament(tournament1)

