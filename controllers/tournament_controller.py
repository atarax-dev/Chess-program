from datetime import datetime

from controllers.round_controller import enter_scores
from models.player_model import Player
from models.tournament_model import Tournament
from views.views import show_tournament_current_rounds_list, show_tournament_sorted_results


def create_tournament():
    name = "Le tournoi des cracks"
    place = "Genève"
    date = datetime.now()
    players_list = [
        Player("Dupont", "JM", datetime(1990, 6, 12), "M", 2000),
        Player("Bueno", "Pepito", datetime(1993, 8, 24), "M", 1800),
        Player("Nabialek", "Anthony", datetime(1993, 3, 25), "M", 2500),
        Player("De Troie", "Emile", datetime(2003, 10, 17), "M", 1000),
        Player("Cagole", "Cindy", datetime(1989, 5, 7), "F", 600),
        Player("Pahouf", "Laetitia", datetime(1991, 5, 3), "F", 1200),
        Player("Tukonai", "Ines", datetime(1977, 4, 1), "F", 1550),
        Player("Layeuve", "Francoise", datetime(1958, 6, 13), "F", 1950)
    ]
    rounds_list = []
    time_control = "Rapide"
    description = "Remarques"
    return Tournament(name=name, place=place, date=date, rounds_list=rounds_list, players_list=players_list,
                      time_control=time_control, description=description)


def launch_tournament(tournament):
    while tournament.current_round <= tournament.number_of_rounds:
        tournament.generate_swiss_pairs()
        show_tournament_current_rounds_list(tournament)
        enter_scores(tournament)
        show_tournament_sorted_results(tournament)
