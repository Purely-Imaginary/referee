import urllib.request

import app.secrets as secrets

import app.models.CalculatedMatch as CMatch
import app.models.Player as Player


def get_all_players_from_spreadsheet():
    url = secrets.getspreadsheeturl()
    response = urllib.request.urlopen(url)
    data = response.read()  # a `bytes` object
    text = data.decode('utf-8').split('\r\n')
    text.pop(0)

    players_list = []
    players_columns = [2, 3, 6, 7]

    for row in text:
        raw_data = row.split(',')
        for column in players_columns:
            if players_list.count(raw_data[column]) == 0:
                players_list.append(raw_data[column])

    players_object_list = []
    for player in players_list:
        players_object_list.append(Player.Player(players_object_list.__len__(), player))

    return players_object_list


def get_player(name, players_object_list):
    for index in range(players_object_list.__len__()):
        if players_object_list[index].name == name:
            return players_object_list[index]

    return 0


def sort_players_by_rating(players):
    return sorted(players, key=lambda player: player.present_rating, reverse=True)
