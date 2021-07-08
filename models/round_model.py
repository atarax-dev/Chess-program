from helpers.helpers import convert_datetime_to_str, convert_str_to_datetime


class Round:
    def __init__(self, match_list, name, begin_date, end_date=None):

        self.end_date = end_date
        self.begin_date = begin_date
        self.name = name
        self.match_list = match_list

    def get_json(self):
        json_match_list = []
        for match in self.match_list:
            json_match = match.get_json()
            json_match_list.append(json_match)
        if self.end_date is None:
            end_date = None
        else:
            end_date = convert_str_to_datetime(self.end_date)

        return {
            "match_list": json_match_list,
            "name": self.name,
            "begin_date": convert_datetime_to_str(self.begin_date),
            "end_date": end_date
        }
