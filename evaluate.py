'''
Position evaluation
'''

from consts import *

def evaluate_position(board):
    """
    Evaluates the given board position and returns a score.
    """
    score = 0

    # material score
    for piece_type, value in PIECE_SCORES:
        score += len(board.pieces(piece_type, chess.WHITE)) * value
        score -= len(board.pieces(piece_type, chess.BLACK)) * value

    # positional score
    for square, piece in board.piece_map().items():
        if piece.color == chess.WHITE:
            # bonus for controlling the center of the board
            if square in CENTER_SQUARES:
                score += 10
        else:
            if square in CENTER_SQUARES:
                score -= 10

    return score