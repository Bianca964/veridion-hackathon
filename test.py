import unittest
import requests_mock

from hack import play_game


class TestGame(unittest.TestCase):
    @requests_mock.Mocker()
    def test_play_game(self, mock):
        # Simulăm răspunsurile serverului
        mock.get("http://127.0.0.1:5000/get-word", json={"word": "rock", "round": 1})
        mock.get("http://127.0.0.1:5000/status", json={"status": "ongoing"})
        mock.post("http://127.0.0.1:5000/submit-word", json={"message": "Word submitted!"})

        play_game(player_id=1)  # Ar trebui să ruleze fără erori

if __name__ == "__main__":
    unittest.main()
