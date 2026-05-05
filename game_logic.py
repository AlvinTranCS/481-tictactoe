def check_board_dead(board_slice):
    lines = [
        (0, 1, 2), (3, 4, 5), (6, 7, 8),
        (0, 3, 6), (1, 4, 7), (2, 5, 8),
        (0, 4, 8), (2, 4, 6)
    ]
    for line in lines:
        if board_slice[line[0]] == 1 and board_slice[line[1]] == 1 and board_slice[line[2]] == 1:
            return True
    return False

def get_active_boards(board_array):
    return [
        not check_board_dead(board_array[0:9]),
        not check_board_dead(board_array[9:18]),
        not check_board_dead(board_array[18:27])
    ]

def get_valid_moves(board_array, active_boards):
    moves = []
    for i in range(27):
        board_idx = i // 9
        if active_boards[board_idx] and board_array[i] == 0:
            moves.append(i)
    return moves

def is_game_over(board_array):
    active_boards = get_active_boards(board_array)
    return sum(active_boards) == 0
