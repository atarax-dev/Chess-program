from helpers.helpers import convert_datetime_to_str


class Player:
    def __init__(self, last_name, first_name, birth_date, gender, rank, score=0):

        self.last_name = last_name
        self.first_name = first_name
        self.birth_date = birth_date
        self.gender = gender
        self.rank = rank
        self.score = score

    def __repr__(self):
        return self.first_name

    def get_json(self):
        return {
            "last_name": self.last_name,
            "first_name": self.first_name,
            "birth_date": convert_datetime_to_str(self.birth_date),
            "gender": self.gender,
            "rank": self.rank,
            "score": self.score
        }

    def set_rank(self, new_rank):
        self.rank = new_rank

    def get_player_details(self):
        return self.last_name, self.first_name, self.birth_date, self.gender
