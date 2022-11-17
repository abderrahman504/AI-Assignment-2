import math
from Utilities import GameState
from Tree import TreeNode


def minimax(state: GameState, depth, is_max, threshold, root: TreeNode):
    if depth == threshold:
        return state.predict_score(), None
    if is_max:
        best_score, max_child = -math.inf, None
        child_states = state.get_next_states(1)
        for child in child_states:
            child_node = TreeNode()
            root.add_child(child_node)
            score, _ = minimax(child, depth + 1, False, threshold, child_node)
            child_node.set_score(score)
            if best_score < score:
                max_child, best_score = child, score
        root.set_score(best_score)
        return best_score, max_child

    else:
        best_score, min_child = math.inf, None
        child_states = state.get_next_states(0)
        for child in child_states:
            child_node = TreeNode()
            root.add_child(child_node)
            score, _ = minimax(child, depth + 1, True, threshold, child_node)
            child_node.set_score(score)
            if best_score > score:
                min_child, best_score = child, score
        root.set_score(best_score)
        return best_score, min_child


def alphabeta_pruning(state: GameState, depth, is_max, threshold, alpha, beta, root: TreeNode):
    if depth == threshold:
        return state.predict_score(), None
    if is_max:
        best_score, max_child = -math.inf, None
        child_states = state.get_next_states(1)
        for child in child_states:
            child_node = TreeNode()
            root.add_child(child_node)
            score, _ = alphabeta_pruning(child, depth + 1, False, threshold, alpha, beta, child_node)
            child_node.set_score(score)
            if best_score < score:
                max_child, best_score = child, score
            alpha = max(alpha, best_score)
            if alpha >= beta:
                break
        root.set_score(best_score)
        return best_score, max_child

    else:
        best_score, min_child = math.inf, None
        child_states = state.get_next_states(0)
        for child in child_states:
            child_node = TreeNode()
            root.add_child(child_node)
            score, _ = alphabeta_pruning(child, depth + 1, True, threshold, alpha, beta, child_node)
            child_node.set_score(score)
            if best_score > score:
                min_child, best_score = child, score
            beta = min(beta, best_score)
            if alpha >= beta:
                break
        root.set_score(best_score)
        return best_score, min_child
