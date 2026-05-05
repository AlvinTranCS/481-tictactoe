def check_board_dead(board_slice):
    """
    Checks if a 9-element list (representing a 3x3 board) has a 3-in-a-row.
    board_slice is a list of 9 elements (0 for empty, 1 for 'X').
    """
    lines = [
        (0, 1, 2), (3, 4, 5), (6, 7, 8),  # Rows
        (0, 3, 6), (1, 4, 7), (2, 5, 8),  # Columns
        (0, 4, 8), (2, 4, 6)              # Diagonals
    ]
    for line in lines:
        if board_slice[line[0]] == 1 and board_slice[line[1]] == 1 and board_slice[line[2]] == 1:
            return True
    return False

def get_active_boards(board_array):
    """
    Returns a list of 3 booleans indicating which of the 3 boards are still active.
    board_array is a 1D list of 27 elements.
    """
    return [
        not check_board_dead(board_array[0:9]),
        not check_board_dead(board_array[9:18]),
        not check_board_dead(board_array[18:27])
    ]

def get_valid_moves(board_array, active_boards):
    """
    Returns a list of valid 1D indices (0-26) to play on.
    A move is valid if the spot is empty and the board it belongs to is active.
    """
    moves = []
    for i in range(27):
        board_idx = i // 9
        if active_boards[board_idx] and board_array[i] == 0:
            moves.append(i)
    return moves

def is_game_over(board_array):
    """
    The game is over when all 3 boards are dead (i.e., have a 3-in-a-row).
    """
    active_boards = get_active_boards(board_array)
    return sum(active_boards) == 0
