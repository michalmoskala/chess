from mechanics.play import play
from solver.kamil import get_auto_move as kamil_move

if __name__ == '__main__':
    play(white_move=kamil_move)
