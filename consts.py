import chess

# ---------- Constants and Parameters ---------- #
PIECE_SCORES = [
    (chess.PAWN, 100),
    (chess.KNIGHT, 275), 
    (chess.BISHOP, 325), 
    (chess.ROOK, 500), 
    (chess.QUEEN, 900)
]

CENTER_SQUARES = [chess.E4, chess.D4, chess.E5, chess.D5]

EXPLORATION_VALUE = 1.4
N_SIMULATIONS = 1000