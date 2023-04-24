from consts import *
from mcts import MonteCarloTreeSearch

if __name__ == '__main__':
    # create the Monte Carlo Tree Search object
    mcts = MonteCarloTreeSearch(exploration_value=EXPLORATION_VALUE)

    # initialize the board
    board = chess.Board()

    # main loop
    while not board.is_game_over():
        # display the board
        print(board)

        if board.turn == chess.WHITE:
            # get the user's move
            user_move = input('Enter your move (in algebraic notation): ')
            try:
                board.push_san(user_move)
            except ValueError:
                print('Invalid move. Please try again.')
                continue

        else:
            # use MCTS to suggest a move for the engine
            engine_move = mcts.get_move(board, simulations_number=N_SIMULATIONS)

            # display the engine's move
            print(f'Engine: {engine_move.uci()}')

            # apply the engine's move to the board
            board.push(engine_move)

    # display the final result
    print(board.result())
