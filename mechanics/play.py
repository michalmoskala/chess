from game import Game
from utils import Position

DEBUG = True


def get_manual_move(own_game:Game, is_white): #  this function is awful i know dont at me
    all = own_game.get_all_legal_moves_for_player(is_white)
    c = input()

    if c == "list":
        for p in own_game.pieces:
            owner = "White " if p.is_white else "Black "
            print(owner + str(p))
        c = input()

    if c == "redo":
        for p in own_game.pieces:
            print(f'pieces.append({p.__class__.__name__}(Position("{chr(p.position.x)}", {p.position.y}), {p.is_white}, {p.initial_position}))')
        c = input()

    c = c.capitalize()
    a = c[0]
    b = int(c[1])

    move = Position(a, b)
    actions = []
    for k, v in all.items():
        if move in v['attacks']:
            actions.append(k)
        if move in v['moves']:
            actions.append(k)
    if len(actions) == 1:
        return actions[0].position, c
    c = input("Be more specific")
    c = c.upper()
    return c[0:2], c[2:5]


def play(white_move=get_manual_move, black_move=get_manual_move):
    game = Game(special=False, pieces=None)

    while True:
        complete = False
        while not complete:
            try:
                start, end = white_move(game.make_new_game(), True)
                game.act(start, end, True)
                complete = True
            except Exception as e:
                print(e)
                raise e
                start, end = get_manual_move(game.make_new_game(), True)
                game.act(start, end, True)
                complete = True

        complete = False
        while not complete:
            try:
                start, end = black_move(game.make_new_game(), False)
                game.act(start, end, False)
                complete = True
            except Exception as e:
                print(e)
                start, end = get_manual_move(game.make_new_game(), False)
                game.act(start, end, False)
                complete = True
