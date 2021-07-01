class Player:
    def __init__(self, last_name, first_name, birth_date, gender, rank, tournament_position=0, score=0):

        self.last_name = last_name
        self.first_name = first_name
        self.birth_date = birth_date
        self.gender = gender
        self.rank = rank
        self.score = score
        self.tournament_position = tournament_position

    def __repr__(self):
        return self.first_name

    def get_json(self):
        return {
            "last_name": self.last_name,
            "first_name": self.first_name,
            "birth_date": self.birth_date,
            "gender": self.gender,
            "rank": self.rank
        }

    def set_rank(self, new_rank):
        self.rank = new_rank
