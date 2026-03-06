import random

GRID_SIZE = 10
SHIP_LENGTHS = (5, 4, 3, 3, 2)


def ship_lengths_for_grid(grid_size):
    if grid_size < GRID_SIZE:
        return tuple(length for length in SHIP_LENGTHS if length <= grid_size)
    return SHIP_LENGTHS


def empty_grid(grid_size):
    return [['~' for _ in range(grid_size)] for _ in range(grid_size)]


def place_ships(grid_size):
    grid = empty_grid(grid_size)
    for length in ship_lengths_for_grid(grid_size):
        placed = False
        while not placed:
            horizontal = random.choice((True, False))
            if horizontal:
                row = random.randint(0, grid_size - 1)
                col = random.randint(0, grid_size - length)
                cells = [(row, col + offset) for offset in range(length)]
            else:
                row = random.randint(0, grid_size - length)
                col = random.randint(0, grid_size - 1)
                cells = [(row + offset, col) for offset in range(length)]

            if all(grid[r][c] == '~' for r, c in cells):
                for r, c in cells:
                    grid[r][c] = 'S'
                placed = True
    return grid


def new_state():
    return new_state_for_size(GRID_SIZE)


def new_state_for_size(grid_size):
    return {
        'player_board': place_ships(grid_size),
        'enemy_board': place_ships(grid_size),
        'player_view': empty_grid(grid_size),
        'enemy_shots': [],
        'status': 'active',
        'grid_size': grid_size,
    }


def board_remaining_ships(board):
    return any(cell == 'S' for row in board for cell in row)


def apply_shot(board, target_row, target_col):
    current = board[target_row][target_col]
    if current == 'S':
        board[target_row][target_col] = 'X'
        return 'hit'
    if current == '~':
        board[target_row][target_col] = 'O'
        return 'miss'
    return 'repeat'


def next_enemy_target(state):
    grid_size = state.get('grid_size', GRID_SIZE)
    attempted = {(entry['row'], entry['col']) for entry in state['enemy_shots']}
    candidates = [
        (r, c)
        for r in range(grid_size)
        for c in range(grid_size)
        if (r, c) not in attempted
    ]
    return random.choice(candidates) if candidates else None
