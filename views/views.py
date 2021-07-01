from controllers.tournament_controller import sort_players_score


def show_tournament_details(self):
    return self.name, self.place, self.date, self.rounds_list, self.players_list, \
           self.timecontrol, self.description, self.number_of_rounds


def show_player_details(self):
    return self.last_name, self.first_name, self.birth_date, self.gender


def show_tournament_sorted_results(self):
    sorted_players = sort_players_score(self)
    for player in sorted_players:
        print(player.first_name + " " + str(player.score) + " " + str(player.rank))
