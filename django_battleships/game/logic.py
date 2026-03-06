import random

GRID_SIZE = 10
SHIP_LENGTHS = (5, 4, 3, 3, 2)


def empty_grid():
    return [['~' for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]


def place_ships():
    grid = empty_grid()
    for length in SHIP_LENGTHS:
        placed = False
        while not placed:
            horizontal = random.choice((True, False))
            if horizontal:
                row = random.randint(0, GRID_SIZE - 1)
                col = random.randint(0, GRID_SIZE - length)
                cells = [(row, col + offset) for offset in range(length)]
            else:
                row = random.randint(0, GRID_SIZE - length)
                col = random.randint(0, GRID_SIZE - 1)
                cells = [(row + offset, col) for offset in range(length)]

            if all(grid[r][c] == '~' for r, c in cells):
                for r, c in cells:
                    grid[r][c] = 'S'
                placed = True
    return grid


def new_state():
    return {
        'player_board': place_ships(),
        'enemy_board': place_ships(),
        'player_view': empty_grid(),
        'enemy_shots': [],
        'status': 'active',
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
    attempted = {(entry['row'], entry['col']) for entry in state['enemy_shots']}
    candidates = [
        (r, c)
        for r in range(GRID_SIZE)
        for c in range(GRID_SIZE)
        if (r, c) not in attempted
    ]
    return random.choice(candidates) if candidates else None
