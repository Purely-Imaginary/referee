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


def generate_matches(matches_data, players_data):
    matches = []
    for row in matches_data:
        raw_data = row.split(',')

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
        player11.change_rating(calculated_match.rating_change)
        player12.change_rating(calculated_match.rating_change)
        player21.change_rating(-calculated_match.rating_change)
        player22.change_rating(-calculated_match.rating_change)

        matches.append(calculated_match)
    return matches
