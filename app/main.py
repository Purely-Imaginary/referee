from flask import Flask, render_template, make_response, redirect, url_for, request, session
from app.elo import main as elo
import app.secrets as secrets

app = Flask(__name__)

app.secret_key = secrets.getsecretkey()


@app.route("/")
def hello():
    i=3
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
    # return render_template('hi.html', name=name)
    return response


@app.route("/setcookie")
def cookie():
    username = request.cookies.get('username')
    response = make_response(render_template('hi.html', name=username, session=session['data2']))
    response.set_cookie('testing cookie', 'cookie tested!')
    return response


if __name__ == "__main__":
    # Only for debugging while developing
    app.run(host='0.0.0.0', debug=True, port=5025)
