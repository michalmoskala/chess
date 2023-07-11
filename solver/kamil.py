import random


def get_auto_move(own_game, is_white):
    move_scores = []
    legal_actions = own_game.get_all_legal_moves_for_player(is_white, check_for_checks=True)
    for piece, actions in legal_actions.items():
        for move in actions["moves"]:
            value = random.randint(0, 100)
            move_scores.append((piece.position, move, value))

        for attack in actions["attacks"]:
            value = random.randint(0, 100) + 100
            move_scores.append((piece.position, attack, value))

    move_scores.sort(key=lambda x: x[2], reverse=True)
    return move_scores[0][0], move_scores[0][1]
