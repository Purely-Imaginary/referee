from app.matchClass import match
import urllib.request

players = {}
matches = []


def getPlayerElo(name):
    if name not in players:
        players[name] = 1000
    return players[name]


def processMatch(match):
    player11elo = getPlayerElo(match.player11)
    player12elo = getPlayerElo(match.player12)
    player21elo = getPlayerElo(match.player21)
    player22elo = getPlayerElo(match.player22)

    calculatedMatch = match.calculate(player11elo, player12elo, player21elo, player22elo)
    players[match.player11] += calculatedMatch['ratingChange']
    players[match.player12] += calculatedMatch['ratingChange']
    players[match.player21] -= calculatedMatch['ratingChange']
    players[match.player22] -= calculatedMatch['ratingChange']

    # print(match.date + " " + match.time + ": " + str(ratingChange))
    # print(calculatedMatch)
    matches.append(calculatedMatch)


def importmatch(string):
    data = string.split(',')
    if data[0] == 'Date':
        return
    newMatch = match(
        data[0],
        data[1],
        data[2],
        data[3],
        data[6],
        data[7],
        int(data[4]),
        int(data[5]),
        data[8]
    )
    i = 0
    return newMatch


def main():
    skipFirst = True
    url = 'https://spreadsheets.google.com/feeds/download/spreadsheets/Export?key=1ZcanOKj8IMd4AEynruOyp0D5HIY05wUqEjg4P2Z6ang&hl&exportFormat=csv'
    response = urllib.request.urlopen(url)
    data = response.read()  # a `bytes` object
    text = data.decode('utf-8').split('\r\n')

    for row in text:
        if skipFirst:
            skipFirst = False
        else:
            processMatch(importmatch(row))

    playersSorted = [(k, players[k]) for k in sorted(players, key=players.get, reverse=True)]

    returnData = ""
    for name, elo in playersSorted:
        returnData += "{:25}".format(name) + ":" + "{:10.2f}<br>".format(elo)
    return returnData
