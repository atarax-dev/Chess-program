from datetime import datetime


class Player:
    def __init__(self, last_name, first_name, birth_date, gender, rank, score=0):

        self.last_name = last_name
        self.first_name = first_name
        self.birth_date = birth_date
        self.gender = gender
        self.rank = rank
        self.score = score

#    def __repr__(self):
#        return self.first_name

    def get_json(self):
        """
Permet d'obtenir les informations du joueur sous forme de dictionnaire
        :return: dict
        """
        return {
            "last_name": self.last_name,
            "first_name": self.first_name,
            "birth_date": datetime.strftime(self.birth_date, "%Y-%m-%d"),
            "gender": self.gender,
            "rank": self.rank,
            "score": self.score
        }
