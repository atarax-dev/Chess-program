from datetime import datetime

from controllers.player_controller import get_player_rank, get_player_score
from models.player_model import Player
from models.tournament_model import Tournament


def create_tournament():
    name = "Le tournoi des cracks"
    place = "Genève"
    date = datetime.now()
    players_list = [
        Player("Dupont", "JM", datetime(1990, 6, 12), "M", 2000),
        Player("Bueno", "Pepito", datetime(1993, 8, 24), "M", 1800),
        Player("Nabialek", "Anthony", datetime(1993, 3, 25), "M", 2500),
        Player("De Bon", "Emile", datetime(2003, 10, 17), "M", 1000),
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


def sort_players_score(tournament):
    s = sorted(tournament.players_list, reverse=True, key=get_player_rank)
    sorted_players = sorted(s, reverse=True, key=get_player_score)
    return sorted_players


def sort_players_rank(tournament):
    sorted_players = sorted(tournament.players_list, reverse=True, key=get_player_rank)
    return sorted_players
