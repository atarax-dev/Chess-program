class Tournament:
    def __init__(self, name, place, date, players_list, time_control, description,
                 number_of_rounds=4, rounds_list=None):
        if rounds_list is None:
            rounds_list = []
        self.name = name
        self.place = place
        self.date = date
        self.rounds_list = rounds_list
        self.players_list = players_list
        self.time_control = time_control
        self.description = description
        self.number_of_rounds = number_of_rounds
