# Battleships

This repository now includes a web implementation of Battleships using:

- **Django** for the backend API
- **AngularJS** for the frontend behavior
- **HTML Canvas** for all board rendering and visual styling

## Run locally

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python django_battleships/manage.py migrate
python django_battleships/manage.py runserver
```

Open `http://127.0.0.1:8000/`.

## API endpoints

- `POST /api/new-game/` starts a new game in session state.
- `POST /api/fire/` with JSON `{ "row": <int>, "col": <int> }` fires at enemy grid.
