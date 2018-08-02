import app.secrets as secrets
import app.models.CalculatedMatch as CMatch
import app.models.Player as Player
import app.controllers.PlayersProcessor as PProcessor
import urllib.request

from app.matchClass import match


def get_matches_from_spreadsheet():
    url = secrets.getspreadsheeturl()
    response = urllib.request.urlopen(url)
    data = response.read()  # a `bytes` object
    text = data.decode('utf-8').split('\r\n')
    text.pop(0)
    return text


def generate_matches(mongo_handler):
    players_data = PProcessor.get_all_players_from_spreadsheet(mongo_handler)
    matches_data = get_matches_from_spreadsheet()
    matches = []
    mongo_handler.db.matches.remove({})
    for row in matches_data:
        raw_data = row.split(',')

        if raw_data[2] > raw_data[3]:
            temp = raw_data[3]
            raw_data[3] = raw_data[2]
            raw_data[2] = temp

        if raw_data[6] > raw_data[7]:
            temp = raw_data[7]
            raw_data[7] = raw_data[6]
            raw_data[6] = temp

        player11 = PProcessor.get_player(raw_data[2], players_data)
        player12 = PProcessor.get_player(raw_data[3], players_data)
        player21 = PProcessor.get_player(raw_data[6], players_data)
        player22 = PProcessor.get_player(raw_data[7], players_data)

        calculated_match = CMatch.CalculatedMatch(
            raw_data[0],
            raw_data[1],
            player11,
            player12,
            player21,
            player22,
            int(raw_data[4]),
            int(raw_data[5]),
            raw_data[8]
        )
        player11.change_rating(calculated_match.rating_change, mongo_handler)
        player12.change_rating(calculated_match.rating_change, mongo_handler)
        player21.change_rating(-calculated_match.rating_change, mongo_handler)
        player22.change_rating(-calculated_match.rating_change, mongo_handler)

        matches.append(calculated_match)
        calculated_match.insert_to_db(mongo_handler)
        calculated_match.update_players(mongo_handler)
    return matches


def get_matches_for_list(mongo_handler):
    data = mongo_handler.db.matches.find()
    list = []
    for match in data:
        list.append(match)
    list.reverse()
    return list
