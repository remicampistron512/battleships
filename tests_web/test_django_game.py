import os
import sys

PROJECT_ROOT = os.path.join(os.path.dirname(__file__), '..', 'django_battleships')
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_battleships.settings')

import django

django.setup()

from django.test import Client


def test_new_game_and_fire_cycle():
    client = Client()

    response = client.post('/api/new-game/')
    assert response.status_code == 200
    payload = response.json()
    assert payload['grid_size'] == 10

    fire_response = client.post(
        '/api/fire/',
        data='{"row": 0, "col": 0}',
        content_type='application/json',
    )
    assert fire_response.status_code == 200
    fire_payload = fire_response.json()
    assert fire_payload['player_result'] in {'hit', 'miss'}
    assert fire_payload['status'] in {'active', 'player_won', 'enemy_won'}
    assert len(fire_payload['player_view']) == 10
