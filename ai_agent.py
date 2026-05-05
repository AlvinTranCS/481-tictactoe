import random
from game_logic import get_active_boards, get_valid_moves

def get_safe_moves(board_array, active_boards):
    safe_moves_count = 0
    for move in get_valid_moves(board_array, active_boards):
        new_board = list(board_array)
        new_board[move] = 1
        new_active = get_active_boards(new_board)
        if sum(new_active) > 0:
            safe_moves_count += 1
    return safe_moves_count

def get_dynamic_depth(active_boards):
    num_active = sum(active_boards)
    if num_active == 3:
        return 4
    elif num_active == 2:
        return 5
    else:
        return 7

def negamax(board_array, depth, alpha, beta, color=1):
    active_boards = get_active_boards(board_array)
    num_active = sum(active_boards)
    
    if num_active == 0:
        return 1000 + depth
        
    if depth == 0:
        safe_moves = get_safe_moves(board_array, active_boards)
        if safe_moves % 2 != 0:
            return 10 + safe_moves
        else:
            return -10 - safe_moves
            
    best_value = float('-inf')
    moves = get_valid_moves(board_array, active_boards)
    
    if not moves:
        return 0
        
    for move in moves:
        new_board = list(board_array)
        new_board[move] = 1
        
        val = -negamax(new_board, depth - 1, -beta, -alpha, -color)
        
        if val > best_value:
            best_value = val
        
        if best_value > alpha:
            alpha = best_value
            
        if alpha >= beta:
            break
            
    return best_value

def get_best_move(board_array):
    active_boards = get_active_boards(board_array)
    depth = get_dynamic_depth(active_boards)
    
    best_value = float('-inf')
    best_move = None
    alpha = float('-inf')
    beta = float('inf')
    
    moves = get_valid_moves(board_array, active_boards)
    if not moves:
        return None
        
    random.shuffle(moves)
    
    for move in moves:
        new_board = list(board_array)
        new_board[move] = 1
        
        val = -negamax(new_board, depth - 1, -beta, -alpha)
        
        if val > best_value:
            best_value = val
            best_move = move
            
        if best_value > alpha:
            alpha = best_value
            
    return best_move

def get_ai_move(board_array, difficulty):
    moves = get_valid_moves(board_array, get_active_boards(board_array))
    if not moves:
        return None
        
    if difficulty == "Easy":
        return random.choice(moves)
    elif difficulty == "Medium":
        if random.random() < 0.5:
            return random.choice(moves)
        else:
            return get_best_move(board_array)
    else:
        return get_best_move(board_array)
