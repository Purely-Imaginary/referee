import time

from flask import Flask, render_template, make_response, redirect, url_for, request, session
from flask_pymongo import PyMongo
import controllers.MatchesProcessor as MProcessor
import controllers.PlayersProcessor as PProcessor
import models.Player as Player
import controllers.TableProcessor as TProcessor
import secrets as secrets
import pprint

app = Flask(__name__)

app.secret_key = secrets.getsecretkey()

# sudo service mongod start
app.config["MONGO_URI"] = "mongodb://localhost:27017/referee"
mongo = PyMongo(app)


@app.route("/")
def hello():
    session['data2'] = 'sessions data'
    app.logger.debug('A value for debugging')
    app.logger.warning('A warning occurred (%d apples)', 42)
    app.logger.error('An error occurred')
    return render_template('hi.html')


@app.route("/hi/<name>")
def hi(name=None):
    response = make_response(redirect(url_for('cookie')))
    response.set_cookie('username', name)
    debug = mongo.db.matches.insert({'name': name})
    # return render_template('hi.html', name=name)
    return response


@app.route("/league")
@app.route("/league/<league_id>")
@app.route("/league/<league_id>/<generate>")
def league(league_id='', generate=True):
    if generate != 'false':
        MProcessor.generate_matches(mongo)

    table = MProcessor.generate_table(mongo, league_id)
    matches = MProcessor.get_matches_for_league(mongo, league_id, True)
    table = TProcessor.replace_names_with_teams(table)
    return render_template('league.html', table=table['scoreboard'], teams=table['detailed'], last_matches=matches,
                           league_id=league_id)


@app.route("/recalc")
def recalc():
    MProcessor.generate_matches(mongo)
    generate_ranking()


@app.route("/getRank")
@app.route("/getRank/<generate>")
def generate_ranking(generate=True):
    start_time = time.time()
    if generate != 'false':
        MProcessor.generate_matches(mongo)
    sorted_players = PProcessor.sort_players_by_rating(mongo)
    matches = MProcessor.get_matches_for_list(mongo)
    duration = round(time.time() - start_time, 4)
    app.logger.debug('Ready in ' + str(duration) + 's')

    return render_template('ranking.html', data=matches, players=sorted_players)


@app.route("/getPlayer/<player_id>")
def get_player(player_id):
    player_data = Player.Player.get_player_data(player_id, mongo)

    return render_template('playerStats.html', player_data=player_data)


@app.route("/print", methods=['GET', 'POST'])
def print_data():
    data = pprint.pformat(request.form)
    app.logger.debug(data)

    return data


if __name__ == "__main__":
    # Only for debugging while developing
    app.run(host='0.0.0.0', debug=True, port=5025)
