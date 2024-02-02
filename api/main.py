#
# to run use command: flask run -h 0.0.0.0 -p port
#

import flask
from flask_httpauth import HTTPTokenAuth

app = flask.Flask(__name__)

with open('tokens.tok', 'r') as file:
    allowed_tokens_str = file.read()
allowed_tokens = allowed_tokens_str.split('\n')

token_auth = HTTPTokenAuth(scheme="Bearer")

@app.route("/Auth")
@token_auth.login_required
def Auth():
    return flask.jsonify({"Status":"OK"})

@app.route("/Predict/<id>")
@token_auth.login_required
def Predict(id):
    print(flask.request.get_json()["dates"])
    
    #predicting weather
    return flask.jsonify({
        "Status":"OK",
        "Data": id
        })


@token_auth.verify_token
def verify_token(token):
    if token not in allowed_tokens:
        return None
    return True




# for some reason it does not work
# if __name__ == '__main__':
#     app.run(host="0.0.0.0", port=8642, debug=True)
