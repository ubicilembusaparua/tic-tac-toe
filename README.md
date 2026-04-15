# Tic-Tac-Toe

A Flask-based tic-tac-toe web game with two play modes:

- Local multiplayer on one device
- Play against a simple computer opponent

## Features

- Clean browser-based game board
- Animated tile reveal
- Highlighted winning line when the game is finished
- Responsive layout for desktop and mobile

## Requirements

- Python 3.13+
- Flask 3.x

## Setup

Install dependencies:

```bash
C:/Users/ASUS/AppData/Local/Programs/Python/Python313/python.exe -m pip install -r requirements.txt
```

## Run

Start the app with:

```bash
C:/Users/ASUS/AppData/Local/Programs/Python/Python313/python.exe app.py
```

Or run it with Flask:

```bash
set FLASK_APP=app
set SECRET_KEY=your-secret-key
flask run
```

## Tests

Run the test suite with:

```bash
C:/Users/ASUS/AppData/Local/Programs/Python/Python313/python.exe -m unittest discover -s tests
```

## Notes

- Set `SECRET_KEY` in your environment before deploying.
- The repository is intended for local play and simple single-session game state.
