from __future__ import annotations

from flask import Flask, flash, redirect, render_template, request, session, url_for

from game import apply_move, computer_move, new_game

SESSION_GAME_KEY = "tic_tac_toe_game"
SESSION_MODE_KEY = "tic_tac_toe_mode"


def create_app() -> Flask:
    app = Flask(__name__)
    app.config["SECRET_KEY"] = "dev-tic-tac-toe-secret"

    def load_game() -> dict | None:
        mode = session.get(SESSION_MODE_KEY)
        game = session.get(SESSION_GAME_KEY)
        if not mode or not isinstance(game, dict):
            return None
        return game

    def save_game(game: dict) -> None:
        session[SESSION_GAME_KEY] = game
        session[SESSION_MODE_KEY] = game["mode"]

    @app.get("/")
    def index():
        return redirect(url_for("choose_mode"))

    @app.route("/mode", methods=["GET", "POST"])
    def choose_mode():
        if request.method == "POST":
            mode = request.form.get("mode", "multiplayer")
            if mode not in {"multiplayer", "computer"}:
                mode = "multiplayer"
            game = new_game(mode)
            save_game(game)
            return redirect(url_for("game_board"))
        return render_template("index.html")

    @app.get("/game")
    def game_board():
        game = load_game()
        if game is None:
            return redirect(url_for("choose_mode"))
        return render_template("game.html", game=game, mode=game["mode"])

    @app.post("/move")
    def make_move():
        game = load_game()
        if game is None:
            return redirect(url_for("choose_mode"))
        square = request.form.get("square", "")
        try:
            index = int(square)
        except ValueError:
            flash("Choose a valid square.", "error")
            return redirect(url_for("game_board"))

        player = game["current_player"]
        if not apply_move(game, index, player):
            flash(game["message"], "error")
            save_game(game)
            return redirect(url_for("game_board"))

        if game["mode"] == "computer" and not game["winner"] and not game["draw"]:
            ai_index = computer_move(game["board"], "O")
            if ai_index is not None:
                apply_move(game, ai_index, "O")

        save_game(game)
        return redirect(url_for("game_board"))

    @app.post("/reset")
    def reset_game():
        mode = session.get(SESSION_MODE_KEY)
        if mode not in {"multiplayer", "computer"}:
            return redirect(url_for("choose_mode"))
        game = new_game(mode)
        save_game(game)
        flash("Game reset.", "info")
        return redirect(url_for("game_board"))

    return app


app = create_app()


if __name__ == "__main__":
    app.run(debug=True)
