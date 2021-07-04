from itertools import islice, combinations

from controllers.player_controller import get_player_rank, get_player_score
from models.match_model import Match
from models.round_model import Round


class Tournament:
    def __init__(self, name, place, date, time_control, description, players_list=None,
                 number_of_rounds=4, rounds_list=None, current_round=0):
        if players_list is None:
            players_list = []
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
            self.rounds_list.append(Round(match_list, name=f"Round{self.current_round}"))
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
                if (tmp_list[0], tmp_list[i]) not in possible_combos:
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
            self.rounds_list.append(Round(match_list, name=f"Round{self.current_round}"))

    def sort_players_score(self):
        s = sorted(self.players_list, reverse=True, key=get_player_rank)
        self.players_list = sorted(s, reverse=True, key=get_player_score)
