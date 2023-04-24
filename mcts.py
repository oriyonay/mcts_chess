import math
import random
from tqdm.auto import trange

from consts import *
from evaluate import evaluate_position
from utils import sigmoid

class Node:
    def __init__(self, state, parent=None, move=None):
        self.state = state
        self.parent = parent
        self.children = []
        self.visits = 1 # to avoid division by zero
        self.score = 0
        self.move = move

    def add_child(self, state, move):
        child = Node(state, self, move)
        self.children.append(child)
        return child

    def update(self, score):
        if score == '1/2-1/2':
            value = 0.5
        elif self.state.turn:
            # the engine's turn, so the engine won if the score is not a draw
            value = 1 if score == '0-1' else 0
        else:
            # the user's turn, so the user won if the score is not a draw
            value = 1 if score == '1-0' else 0

        self.score += value
        self.visits += 1


    def select_child(self, exploration_value):
        return max(self.children, key=lambda child: child.get_ucb(exploration_value))

    def fully_expanded(self):
        legal_moves = list(self.state.legal_moves)
        return len(self.children) == len(legal_moves)

    def get_ucb(self, exploration_value):
        evaluation = sigmoid(evaluate_position(self.state) / 100)
        if self.visits == 0:
            return evaluation
        else:
            return self.score / self.visits + exploration_value * math.sqrt(
                math.log(self.parent.visits) / self.visits
            ) + evaluation

class MonteCarloTreeSearch:
    def __init__(self, exploration_value=1.4):
        self.exploration_value = exploration_value

    def get_move(self, state, simulations_number):
        root = Node(state)

        for _ in trange(simulations_number):
            node = root
            state_copy = state.copy()

            # selection
            while node.fully_expanded() and node.children:
                node = node.select_child(self.exploration_value)
                state_copy.push(node.move)

            # expansion
            if not node.fully_expanded():
                legal_moves = list(state_copy.legal_moves)
                random.shuffle(legal_moves)
                for move in legal_moves:
                    if move not in [child.move for child in node.children]:
                        state_copy.push(move)
                        node.add_child(state_copy, move)
                        break

            # simulation
            while not state_copy.is_game_over():
                state_copy.push(random.choice(list(state_copy.legal_moves)))

            # backpropagation
            while node:
                result = state_copy.result()
                if result == '1/2-1/2':
                    score = 0.5
                elif result == '1-0' and not state_copy.turn:
                    score = 1
                elif result == '0-1' and state_copy.turn:
                    score = 1
                else:
                    score = 0

                node.update(score)
                node = node.parent

        # best move
        best_child = max(root.children, key=lambda child: child.score / child.visits)
        return best_child.move