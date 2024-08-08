import random
from typing import Optional, Tuple, Callable

def minimax(state, root_player: str, max_depth: int, alpha: float, beta: float, eval_func: Callable) -> Tuple[Optional[Tuple[int, int]], float]:
    if state.is_terminal() or max_depth == 0:
        return None, eval_func(state, root_player)

    best_move = None
    if state.player == root_player:
        value = float('-inf')
        for move in state.legal_moves():
            next_state = state.next_state(move)
            _, new_value = minimax(next_state, root_player, max_depth - 1, alpha, beta, eval_func)
            if new_value > value:
                best_move = move
                value = new_value
            alpha = max(alpha, value)
            if alpha >= beta:
                break
        return best_move, value
    else:
        value = float('+inf')
        for move in state.legal_moves():
            next_state = state.next_state(move)
            _, new_value = minimax(next_state, root_player, max_depth - 1, alpha, beta, eval_func)
            if new_value < value:
                value = new_value
                best_move = move
            beta = min(beta, value)
            if beta <= alpha:
                break
        return best_move, value

def minimax_move(state, max_depth:int, eval_func:Callable) -> Tuple[int, int]:
    """
    Returns a move computed by the minimax algorithm with alpha-beta pruning for the given game state.
    :param state: state to make the move (instance of GameState)
    :param max_depth: maximum depth of search (-1 = unlimited)
    :param eval_func: the function to evaluate a terminal or leaf state (when search is interrupted at max_depth)
                    This function should take a GameState object and a string identifying the player,
                    and should return a float value representing the utility of the state for the player.
    :return: (int, int) tuple with x, y coordinates of the move (remember: 0 is the first row/column)
    """
    move, value = minimax(state, "B" if state.player == "W" else "W", max_depth, float('-inf'), float('+inf'), eval_func)
    if move is None:
        return 0, 0
    return move
