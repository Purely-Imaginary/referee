from flask import Flask
from app.elo import main as elo
app = Flask(__name__)


@app.route("/")
def hello():
    i=0
    returnData = elo()
    return returnData


if __name__ == "__main__":
    # Only for debugging while developing
    app.run(host='0.0.0.0', debug=True, port=5025)
