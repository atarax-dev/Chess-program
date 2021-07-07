from datetime import datetime
from itertools import islice, combinations
from operator import attrgetter

from models.match_model import Match
from models.player_model import Player
from models.round_model import Round


class Tournament:
    def __init__(self, name, place, date, time_control, description, players_list=None,
                 number_of_rounds=4, rounds_list=None, current_round=0):
        if players_list is None:
            players_list = [
                Player("Dupont", "JM", datetime(1990, 6, 12), "M", 2000),
                Player("Bueno", "Pepito", datetime(1993, 8, 24), "M", 1800),
                Player("Nabialek", "Anthony", datetime(1993, 3, 25), "M", 2500),
                Player("De Troie", "Emile", datetime(2003, 10, 17), "M", 1000),
                Player("Cagole", "Cindy", datetime(1989, 5, 7), "F", 600),
                Player("Pahouf", "Laetitia", datetime(1991, 5, 3), "F", 1200),
                Player("Tukonai", "Ines", datetime(1977, 4, 1), "F", 1550),
                Player("Layeuve", "Francoise", datetime(1958, 6, 13), "F", 1950)]
        if rounds_list is None:
            rounds_list = []
        self.current_round = current_round
        self.name = name
        self.place = place
        self.date = date
        self.rounds_list = rounds_list
        self.players_list = players_list
        self.time_control = time_control
        self.description = description
        self.number_of_rounds = number_of_rounds

    def add_player(self, player):
        self.players_list.append(player)

    def add_round(self, roundn):
        self.rounds_list.append(roundn)

    def get_possible_combos(self):
        tmp_list = self.players_list
        possible_combos = list(combinations(tmp_list, 2))
        reversed_tuples = []
        for (i, j) in possible_combos:
            reversed_tuples.append((j, i))
        possible_combos.extend(reversed_tuples)
        return possible_combos

    def generate_swiss_pairs(self):
        self.sort_players_score()
        if self.current_round == 0:
            match_tuple_list = zip(self.players_list, islice(self.players_list, 4, 8))
            match_list = []
            for (player1, player2) in match_tuple_list:
                match_list.append(Match(player1, player2))

            self.current_round += 1
            self.add_round(Round(match_list, name=f"Round{self.current_round}"))
        else:
            possible_combos = self.get_possible_combos()
            for played_round in self.rounds_list:
                for match in played_round.match_list:
                    possible_combos.remove((match.player1, match.player2))
                    possible_combos.remove((match.player2, match.player1))
            tmp_list = list(self.players_list)
            match_list = []
            while len(tmp_list) >= 2:
                i = 1
                while (tmp_list[0], tmp_list[i]) not in possible_combos:
                    try:
                        i += 1
                    except IndexError:
                        i = 1
                pair = (tmp_list[0], tmp_list[i])
                match = Match(pair[0], pair[1])
                reversed_pair = (tmp_list[i], tmp_list[0])
                tmp_list.remove(tmp_list[i])
                tmp_list.remove(tmp_list[0])
                match_list.append(match)
                try:
                    possible_combos.remove(pair)
                    possible_combos.remove(reversed_pair)
                except ValueError:
                    pass
            self.add_round(Round(match_list, name=f"Round{self.current_round}"))
            # TODO fonction save tournoi dans db

    def sort_players_score(self):
        s = sorted(self.players_list, reverse=True, key=attrgetter("rank"))
        self.players_list = sorted(s, reverse=True, key=attrgetter("score"))

    def get_json(self):
        return {
            "name": self.name,
            "place": self.place,
            "date": self.date,
            "time_control": self.time_control,
            "players_list": self.players_list,
            "number_of_rounds": self.number_of_rounds,
            "rounds_list": self.rounds_list,
            "description": self.description,
            "current_round": self.current_round
        }

    def get_tournament_details(self):
        return self.name, self.place, self.date, self.rounds_list, self.players_list, \
               self.time_control, self.description, self.number_of_rounds
