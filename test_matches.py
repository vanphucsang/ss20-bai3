import unittest
from main import determine_winner

class TestTournamentLogic(unittest.TestCase):
    
    def test_determine_winner_team_a_wins(self):
        match = {
            "match_id": "M01",
            "team_a": "T1",
            "team_b": "GenG",
            "score_a": 2,
            "score_b": 0,
            "status": "Completed"
        }
        self.assertEqual(determine_winner(match), "T1")

    def test_determine_winner_draw(self):
        match = {
            "match_id": "M02",
            "team_a": "JDG",
            "team_b": "BLG",
            "score_a": 1,
            "score_b": 1,
            "status": "Completed"
        }
        self.assertEqual(determine_winner(match), "Draw")

    def test_determine_winner_pending(self):
        match = {
            "match_id": "M03",
            "team_a": "G2",
            "team_b": "FNC",
            "score_a": 0,
            "score_b": 0,
            "status": "Pending"
        }
        self.assertEqual(determine_winner(match), "Not Started")
        
    def test_determine_winner_missing_key(self):
        match = {
            "match_id": "M04",
            "team_a": "WBG",
            "status": "Completed"
        }
        self.assertEqual(determine_winner(match), "Data Error")

if __name__ == '__main__':
    unittest.main()