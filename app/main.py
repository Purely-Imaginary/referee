from flask import Flask, render_template, make_response, redirect, url_for, request, session
from flask_pymongo import PyMongo
from app.elo import main as elo
import app.controllers.MatchesProcessor as MProcessor
import app.controllers.PlayersProcessor as PProcessor
import app.secrets as secrets

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
    returnData = elo()
    return returnData


@app.route("/hi/<name>")
def hi(name=None):
    response = make_response(redirect(url_for('cookie')))
    response.set_cookie('username', name)
    debug = mongo.db.matches.insert({'name': name})
    # return render_template('hi.html', name=name)
    return response


@app.route("/league")
@app.route("/league/<league_id>")
def league(league_id=''):
    MProcessor.generate_matches(mongo)
    table = MProcessor.generate_table(mongo, league_id)
    return render_template('league.html', table=table['scoreboard'], teams=table['detailed'])


@app.route("/getRank")
def generate_ranking():
    MProcessor.generate_matches(mongo)
    sorted_players = PProcessor.sort_players_by_rating(mongo)
    matches = MProcessor.get_matches_for_list(mongo)

    return render_template('ranking.html', data=matches, players=sorted_players)


if __name__ == "__main__":
    # Only for debugging while developing
    app.run(host='0.0.0.0', debug=True, port=5025)
