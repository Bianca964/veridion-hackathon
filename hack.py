import unittest
import requests_mock

import requests
from time import sleep
import random


#host = ""
host = "http://127.0.0.1:5000"
post_url = f"{host}/submit-word"
get_url = f"{host}/get-word"
status_url = f"{host}/status"

NUM_ROUNDS = 5


def what_beats(word):
    sleep(random.randint(1, 3))
    return random.randint(1, 60)

def play_game(player_id):

    for round_id in range(1, NUM_ROUNDS+1):
        round_num = -1
        while round_num != round_id:
            response = requests.get(get_url)
            print(response.json())
            sys_word = response.json()['word']
            round_num = response.json()['round']

            sleep(1)

        if round_id > 1:
            status = requests.get(status_url)
            print(status.json())

        choosen_word = what_beats(sys_word)
        data = {"player_id": player_id, "word_id": choosen_word, "round_id": round_id}
        response = requests.post(post_url, json=data)
        print(response.json())




# test
class TestGame(unittest.TestCase):
    @requests_mock.Mocker()
    def test_play_game(self, mock):
        # Lista de runde simulate
        round_responses = [
            {"word": "rock", "round": 1},
            {"word": "paper", "round": 2},
            {"word": "scissors", "round": 3},
            {"word": "lizard", "round": 4},
            {"word": "spock", "round": 5}
        ]

        def get_word_callback(request, context):
            """Simulează schimbarea rundelor."""
            return round_responses.pop(0) if round_responses else {"word": "rock", "round": 5}

        mock.get(get_url, json=get_word_callback)  # Simulează schimbarea rundelor
        mock.get(status_url, json={"status": "ongoing"})
        mock.post(post_url, json={"message": "Word submitted!"})

        play_game(player_id=1)  # Ar trebui să ruleze fără a intra în buclă infinită

if __name__ == "__main__":
    unittest.main()