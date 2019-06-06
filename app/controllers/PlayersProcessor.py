import urllib.request

import app.secrets as secrets

import app.models.CalculatedMatch as CMatch
import app.models.Player as Player


def get_all_players_from_spreadsheet(mongo_handler, matches):
    starting_rating = 1000
    mongo_handler.db.players.remove({})

    players_list = []
    players_columns = [2, 3, 6, 7]

    for row in matches:
        raw_data = row.split(',')
        for column in players_columns:
            if players_list.count(raw_data[column]) == 0:
                players_list.append(raw_data[column])

    players_object_list = []
    for player in players_list:
        player_object = Player.Player(players_object_list.__len__(), player)
        player_object.insert_to_db(mongo_handler)
        players_object_list.append(player_object)

    return players_object_list


def get_player(name, players_object_list):
    for index in range(players_object_list.__len__()):
        if players_object_list[index].name == name:
            return players_object_list[index]

    return 0


def sort_players_by_rating(mongo_handler):
    data = mongo_handler.db.players.find().sort("present_rating", 1)
    list = []
    for player in data:
        list.append(player)
    list.reverse()

    return list
