import math
import Utilities


def minimax(state: Utilities.GameState, depth, is_max, threshold):
    if depth == threshold:
        return state.predict_score(), None
    if is_max:
        best_score, max_child = -math.inf, None
        child_states = state.get_next_states(1)
        for child in child_states:
            score, _ = minimax(child, depth + 1, False, threshold)
            if best_score < score:
                max_child, best_score = child, score
        return best_score, max_child

    else:
        best_score, min_child = math.inf, None
        child_states = state.get_next_states(0)
        for child in child_states:
            score, _ = minimax(child, depth + 1, True, threshold)
            if best_score > score:
                min_child, best_score = child, score
        return best_score, min_child


def alphabeta_pruning(state: Utilities.GameState, depth, is_max, threshold, alpha, beta):
    if depth == threshold:
        return state.predict_score(), None
    if is_max:
        best_score, max_child = -math.inf, None
        child_states = state.get_next_states(1)
        for child in child_states:
            score, _ = minimax(child, depth + 1, False, threshold)
            if best_score < score:
                max_child, best_score = child, score
            alpha = max(alpha, best_score)
            if alpha > beta:
                break
        return best_score, max_child

    else:
        best_score, min_child = math.inf, None
        child_states = state.get_next_states(0)
        for child in child_states:
            score, _ = minimax(child, depth + 1, True, threshold)
            if best_score > score:
                min_child, best_score = child, score
            beta = min(beta, best_score)
            if alpha > beta:
                break
        return best_score, min_child
