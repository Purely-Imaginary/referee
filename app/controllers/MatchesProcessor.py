import app.secrets as secrets
import app.models.CalculatedMatch as CMatch
import app.models.Player as Player
import app.controllers.PlayersProcessor as PProcessor
import urllib.request


def get_matches_from_spreadsheet():
    url = secrets.getspreadsheeturl()
    response = urllib.request.urlopen(url)
    data = response.read()  # a `bytes` object
    text = data.decode('utf-8').split('\r\n')
    text.pop(0)
    return text


def generate_matches(mongo_handler):
    matches_data = get_matches_from_spreadsheet()
    players_data = PProcessor.get_all_players_from_spreadsheet(mongo_handler, matches_data)
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


def get_matches_for_league(mongo_handler, leagueId, reverse=False):
    data = mongo_handler.db.matches.find({'league': leagueId})
    list = []
    for match in data:
        list.append(match)

    if reverse:
        list.reverse()
    return list


def generate_table(mongo_handler, league_id=''):
    matches_list = get_matches_for_league(mongo_handler, league_id)
    teams = {}
    for match in matches_list:
        name1 = match['team1']['player1']['name'] + " - " + match['team1']['player2']['name']
        name2 = match['team2']['player1']['name'] + " - " + match['team2']['player2']['name']
        if name1 not in teams:
            teams[name1] = {}

        if name2 not in teams:
            teams[name2] = {}

        if name2 not in teams[name1]:
            teams[name1][name2] = {
                'team1goals': match['team1']['score'],
                'team2goals': match['team2']['score'],
            }
        else:
            teams[name1][name2]['team1goals'] += match['team1']['score']
            teams[name1][name2]['team2goals'] += match['team2']['score']

        if name1 not in teams[name2]:
            teams[name2][name1] = {
                'team1goals': match['team2']['score'],
                'team2goals': match['team1']['score'],
            }
        else:
            teams[name2][name1]['team1goals'] += match['team2']['score']
            teams[name2][name1]['team2goals'] += match['team1']['score']

    scoreboard = {}

    for team1 in teams:
        wins = 0
        losses = 0
        points = 0
        goals_scored = 0
        goals_lost = 0

        for team2 in teams[team1]:
            goals_scored += teams[team1][team2]['team1goals']
            goals_lost += teams[team1][team2]['team2goals']
            if teams[team1][team2]['team1goals'] > teams[team1][team2]['team2goals']:
                wins += 1
                points += 3
            else:
                losses += 1

        scoreboard[team1] = {
            'wins': wins,
            'losses': losses,
            'points': points,
            'goals_lost': goals_lost,
            'goals_scored': goals_scored,
        }
    sorted_scoreboard = sorted(scoreboard.items(),
                               key=lambda x: (x[1]['points'], x[1]['goals_scored'] - x[1]['goals_lost']), reverse=True)

    score_table = {}

    for name1 in teams:
        for name2 in teams:
            if name1 not in score_table:
                score_table[name1] = {}
                score_table[name1][name2] = {}

            if name2 not in score_table[name1]:
                score_table[name1][name2] = {}

            if name2 in teams[name1]:
                score_table[name1][name2] = str(teams[name1][name2]['team1goals']) + ":" + str(
                    teams[name1][name2]['team2goals'])
            elif name2 == name1:
                score_table[name1][name2] = "X"
            else:
                score_table[name1][name2] = "---"

    return {'scoreboard': sorted_scoreboard, 'detailed': score_table}


def get_league_matches(mongo_handler, league_id):
    return None
