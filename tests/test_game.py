import unittest

from app import create_app
from game import apply_move, check_winner, computer_move, is_draw, new_game


class GameLogicTests(unittest.TestCase):
    def test_detects_winner(self):
        board = ["X", "X", "X", "", "O", "", "", "", "O"]
        result = check_winner(board)
        self.assertEqual(result.winner, "X")
        self.assertEqual(result.line, (0, 1, 2))

    def test_detects_draw(self):
        board = ["X", "O", "X", "X", "O", "O", "O", "X", "X"]
        self.assertTrue(is_draw(board))

    def test_apply_move_rejects_taken_square(self):
        state = new_game("multiplayer")
        state["board"][0] = "X"
        self.assertFalse(apply_move(state, 0, "O"))
        self.assertEqual(state["message"], "That square is already taken.")

    def test_computer_takes_winning_move(self):
        board = ["O", "O", "", "X", "X", "", "", "", ""]
        self.assertEqual(computer_move(board, "O"), 2)

    def test_computer_blocks_human_win(self):
        board = ["X", "X", "", "O", "", "", "", "", ""]
        self.assertEqual(computer_move(board, "O"), 2)

    def test_apply_move_records_winning_line(self):
        state = new_game("multiplayer")
        state["board"] = ["X", "X", "", "O", "O", "", "", "", ""]
        state["current_player"] = "X"

        self.assertTrue(apply_move(state, 2, "X"))
        self.assertEqual(state["winner"], "X")
        self.assertEqual(state["winner_line"], [0, 1, 2])


class RouteTests(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.app.config.update(TESTING=True, SECRET_KEY="test-secret")
        self.client = self.app.test_client()

    def test_mode_selection_starts_game(self):
        response = self.client.post("/mode", data={"mode": "computer"}, follow_redirects=False)
        self.assertEqual(response.status_code, 302)
        self.assertIn("/game", response.headers["Location"])

    def test_cannot_play_without_selecting_mode(self):
        response = self.client.get("/game")
        self.assertEqual(response.status_code, 302)
        self.assertIn("/mode", response.headers["Location"])


if __name__ == "__main__":
    unittest.main()
