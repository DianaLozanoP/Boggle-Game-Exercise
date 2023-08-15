
from boggle import Boggle
from flask import Flask, request, redirect, jsonify, make_response, render_template, session
boggle_game = Boggle()

app = Flask(__name__)
app.config['SECRET_KEY'] = 'Checorocks'


scores = [0]


@app.route("/")
def display_board():
    board = boggle_game.make_board()
    h_score = max(scores)
    session['board'] = board
    session['count'] = session.get('count', 0) + 1
    return render_template("generateboard.html", board=board, h_score=h_score)


@app.route('/verifyword/<word>', methods=['GET'])
def check_valid_word(word):
    # Retrieve the words from boggle
    words = boggle_game.words
    valid_word = False
    # Run a loop to check if the word is inside the dictionary
    for w in words:
        if word == w:
            valid_word = True
        else:
            response = make_response(
                jsonify({"result": "not-a-word"}))
    # if the word is inside dictionary, check if it is valid for the current board
    if valid_word == True:
        # create a response in JSON
        response = make_response(
            jsonify({"result": boggle_game.check_valid_word(session['board'], word)}))
    return response


@app.route('/score/<score>', methods=["GET"])
def track_scores(score):
    integer_score = int(score)
    scores.append(integer_score)
    return redirect("/")
