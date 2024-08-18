import random
from typing import Tuple
from ..othello.gamestate import GameState
from ..othello.board import Board
from .minimax import minimax_move

# Voce pode criar funcoes auxiliares neste arquivo
# e tambem modulos auxiliares neste pacote.
#
# Nao esqueca de renomear 'your_agent' com o nome
# do seu agente.


def make_move(state) -> Tuple[int, int]:
    """
    Returns a move for the given game state
    :param state: state to make the move
    :return: (int, int) tuple with x, y coordinates of the move (remember: 0 is the first row/column)
    """

    # o codigo abaixo apenas retorna um movimento aleatorio valido para
    # a primeira jogada 
    # Remova-o e coloque uma chamada para o minimax_move (que vc implementara' no modulo minimax).
    # A chamada a minimax_move deve receber sua funcao evaluate como parametro.

    free_spaces = state.board.num_pieces('.')
    if free_spaces < 10:
        return minimax_move(state, 5, evaluate_custom)
    if free_spaces < 20:
        return minimax_move(state, 4, evaluate_custom)
    return minimax_move(state, 3, evaluate_custom)

def coin_parity(state, player):
    player_coins = state.board.num_pieces(player)
    opponent_coins = state.board.num_pieces(Board.opponent(player))
    return 100 * (player_coins - opponent_coins) / player_coins + opponent_coins

EVAL_MASK = [
    [100, -30, 6, 2, 2, 6, -30, 100],
    [-30, -50, 1, 1, 1, 1, -50, -30],
    [  6,   1, 1, 1, 1, 1,   1,   6],
    [  2,   1, 1, 3, 3, 1,   1,   2],
    [  2,   1, 1, 3, 3, 1,   1,   2],
    [  6,   1, 1, 1, 1, 1,   1,   6],
    [-30, -50, 1, 1, 1, 1, -50, -30],
    [100, -30, 6, 2, 2, 6, -30, 100]
]

def static_weights (state, player):
    board = str(state.get_board()).split("\n")
    state_total = 0
    
    for mask_row, board_row in zip(EVAL_MASK, board):
        for mask_cell, board_cell in zip(mask_row, board_row):
            # Adds the value if player controls that cell
            if board_cell == player:
                state_total += mask_cell
            # Or subtracts it if it's the opponent who controls it
            elif board_cell == Board.opponent(player):
                state_total -= mask_cell
    return state_total


def actual_mobility(state, player):
    player_moves = len(state.legal_moves())
    opponent_moves = len(state.board.legal_moves(Board.opponent(player)))
    return 100 * (player_moves - opponent_moves) / player_moves + opponent_moves

    
# Counts the amount of free cells around a give piece
def count_potential(board, row, collumn):
    def eval_cell(board, row, collumn):
        cell = board[row][collumn]
        return 1 if cell == "." else 0
    cell_value = 0
    if row > 0:
        # Top right
        if collumn > 0:
            cell_value += eval_cell(board, row-1, collumn-1)
        # Top left
        if collumn < 7:
            cell_value += eval_cell(board, row-1, collumn+1)
        # Top middle
        cell_value += eval_cell(board, row-1, collumn)
        
    if row < 7 :
        # Bottom right
        if collumn > 0:
            cell_value += eval_cell(board, row+1, collumn-1)
        # Bottom left
        if collumn < 7:
            cell_value += eval_cell(board, row+1, collumn+1)
        # Bottom middle
        cell_value += eval_cell(board, row+1, collumn)
        
    # Middle left
    if collumn > 0:
        cell_value += eval_cell(board, row, collumn-1)
        
    # Middle right
    if collumn < 7:
        cell_value += eval_cell(board, row, collumn+1)
    
    return cell_value
    
def potential_mobility(state, player):
    player_potential = 0
    opponent_potential = 0
    opponent = Board.opponent(player)
    
    board = str(state.get_board()).split("\n")
    
    for i in range(8):
        for j in range(8):
            # yes, potential mobility is reversed
            if board[i][j] == player:
                opponent_potential += count_potential(board, i, j)
            elif board[i][j] == opponent:
                player_potential += count_potential(board, i, j)
    return 100 * (player_potential - opponent_potential) / (player_potential + opponent_potential)

def stability(state, player):
    player_stability = 0
    opponent_stability = 0
    opponent = Board.opponent(player)
    
    board = str(state.get_board()).split("\n")
    
    for i in range(8):
        for j in range(8):
            if board[i][j] == player:
                open_flanks = count_potential(board, i, j)
                if (open_flanks == 0):
                    player_stability += 1
            elif board[i][j] == opponent:
                open_flanks = count_potential(board, i, j)
                if (open_flanks == 0):
                    opponent_stability += 1
    if (player_stability + opponent_stability) == 0:
        return 0
    return 100 * (player_stability - opponent_stability) / (player_stability + opponent_stability)


def potential_corners(state, player):
    state_value = 0
    if (state.is_legal_move((0,0))):
        state_value += 25
    if (state.is_legal_move((7,7))):
        state_value += 25
    if (state.is_legal_move((0,7))):
        state_value += 25
    if (state.is_legal_move((7,0))):
        state_value += 25
    
    return state_value

def evaluate_custom(state, player:str) -> float:
    """
    Evaluates an othello state from the point of view of the given player. 
    If the state is terminal, returns its utility. 
    If non-terminal, returns an estimate of its value based on your custom heuristic
    :param state: state to evaluate (instance of GameState)
    :param player: player to evaluate the state for (B or W)
    """
    
    if (state.is_terminal()):
        return float("inf") * 1 if (state.winner == player) else -1
    static_value_contrib = 0
    potential_mobility_contrib = 0
    parity_contrib = 0
    actual_mobility_contrib = 0
    corners_contrib = 0
    
    # Play on principles during earlygame, think on lategame
    free_spaces = state.board.num_pieces('.')
    if (free_spaces) < 10:
        parity_contrib = coin_parity(state, player)
        corners_contrib = potential_corners(state, player)
        actual_mobility_contrib = actual_mobility(state, player)
        stability_contrib = stability(state, player)
    elif (free_spaces) < 30:
        actual_mobility_contrib = actual_mobility(state, player)
        static_value_contrib = 0.45 * static_weights(state, player)
        potential_mobility_contrib = potential_mobility(state, player)
        corners_contrib = potential_corners(state, player)
        stability_contrib = stability(state, player)
    else:
        static_value_contrib =  static_weights(state, player)
        potential_mobility_contrib = potential_mobility(state, player)
        corners_contrib = potential_corners(state, player)
        stability_contrib = 0.5 * stability(state, player)
        
        
    return static_value_contrib + parity_contrib + actual_mobility_contrib + potential_mobility_contrib + corners_contrib + stability_contrib
