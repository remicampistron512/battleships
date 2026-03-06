import json
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.http import require_GET, require_POST

from .logic import GRID_SIZE, apply_shot, board_remaining_ships, new_state_for_size, next_enemy_target
from .models import GameSettings


@require_GET
def index(request):
    settings = GameSettings.load()
    return render(
        request,
        'game/index.html',
        {
            'ui_config': {
                'grid_size': settings.grid_size,
                'water_color': settings.water_color,
                'grid_line_color': settings.grid_line_color,
                'hit_color': settings.hit_color,
                'miss_color': settings.miss_color,
                'ship_color': settings.ship_color,
            }
        },
    )


@require_POST
def new_game(request):
    settings = GameSettings.load()
    state = new_state_for_size(settings.grid_size)
    request.session['battleships_state'] = state
    return JsonResponse(
        {
            'grid_size': state.get('grid_size', GRID_SIZE),
            'status': state['status'],
            'ui': {
                'water_color': settings.water_color,
                'grid_line_color': settings.grid_line_color,
                'hit_color': settings.hit_color,
                'miss_color': settings.miss_color,
                'ship_color': settings.ship_color,
            },
        }
    )


@require_POST
def fire(request):
    state = request.session.get('battleships_state')
    if not state:
        return JsonResponse({'error': 'No active game. Start a new game first.'}, status=400)

    payload = json.loads(request.body or '{}')
    row = payload.get('row')
    col = payload.get('col')
    if not isinstance(row, int) or not isinstance(col, int):
        return JsonResponse({'error': 'row and col must be integers.'}, status=400)
    state_grid_size = state.get('grid_size', GRID_SIZE)
    if row < 0 or col < 0 or row >= state_grid_size or col >= state_grid_size:
        return JsonResponse({'error': 'Shot is outside the board.'}, status=400)

    player_result = apply_shot(state['enemy_board'], row, col)
    if player_result == 'repeat':
        return JsonResponse({'error': 'Cell was already targeted.'}, status=400)

    state['player_view'][row][col] = 'X' if player_result == 'hit' else 'O'

    enemy_turn = None
    if board_remaining_ships(state['enemy_board']):
        enemy_target = next_enemy_target(state)
        if enemy_target is not None:
            enemy_row, enemy_col = enemy_target
            enemy_result = apply_shot(state['player_board'], enemy_row, enemy_col)
            state['enemy_shots'].append({'row': enemy_row, 'col': enemy_col, 'result': enemy_result})
            enemy_turn = {'row': enemy_row, 'col': enemy_col, 'result': enemy_result}

    if not board_remaining_ships(state['enemy_board']):
        state['status'] = 'player_won'
    elif not board_remaining_ships(state['player_board']):
        state['status'] = 'enemy_won'

    request.session['battleships_state'] = state
    return JsonResponse(
        {
            'player_result': player_result,
            'enemy_turn': enemy_turn,
            'player_view': state['player_view'],
            'player_board': state['player_board'],
            'status': state['status'],
        }
    )
