from unittest import TestCase
from app import app, check_valid_word
from flask import session, make_response, jsonify
from boggle import Boggle

app.config['TESTING'] = True
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']


class FlaskTests(TestCase):

    # TODO -- write tests for every view function / feature!
    def test_display_board(self):
        with app.test_client() as client:
            res = client.get('/')
            html = res.get_data(as_text=True)
            self.assertEqual(res.status_code, 200)
            self.assertIn('<table>', html)

    def test_start_game_count(self):
        with app.test_client() as client:
            with client.session_transaction() as change_session:
                change_session['count'] = 10
            res = client.get('/')
            self.assertEqual(res.status_code, 200)
            self.assertEqual(session['count'], 11)

    def test_displayinput_guess(self):
        with app.test_client() as client:
            res = client.get('/')
            html = res.get_data(as_text=True)
            self.assertIn('<input type="text" id="guess">', html)

    def test_check_valid_word(self):
        with app.test_client() as client:
            res = client.get("/verifyword/jddh")
            self.assertEqual(res.status_code, 200)
            html = res.get_data(as_text=True)
            self.assertIn('{\n  "result": "not-a-word"\n}\n', html)

    def test_score_submit(self):
        with app.test_client() as client:
            res = client.get("/score/12")
            self.assertEqual(res.status_code, 302)
            self.assertEqual(res.location, '/')
