from datetime import datetime

from controllers.match_controller import create_match_from_json
from models.round_model import Round


def create_round_from_json(json_round):
    json_match_list = json_round["match_list"]
    match_list = []
    for json_match in json_match_list:
        match = create_match_from_json(json_match)
        match_list.append(match)
    name = json_round["name"]
    begin_date = json_round["begin_date"]
    if json_round["end_date"] != 0:
        end_date = datetime.strptime(json_round["end_date"], "%Y-%m-%d %H:%M")
    else:
        end_date = json_round["end_date"]
    return Round(match_list, name, begin_date, end_date)
