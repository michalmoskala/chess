from pieces import Pawn, Rook, Queen, King, Knight, Bishop, Piece
from utils import Position, find_piece_by_position, find_king


class Game:
    def __init__(self, pieces, special=False):
        if not pieces:
            pieces = []
            if special:  # you can use this to start from a specific position
                pieces.append(Queen(Position("A", 8), False, False))
                pieces.append(Pawn(Position("A", 3), False, False))
                pieces.append(Pawn(Position("G", 7), False, True))
                pieces.append(Pawn(Position("H", 7), False, True))

                pieces.append(Bishop(Position("C", 8), False, False))

                pieces.append(Rook(Position("C", 7), True, False))
                pieces.append(Rook(Position("A", 2), True, False))

                pieces.append(King(Position("E", 5), True, False))
                pieces.append(King(Position("E", 8), False, False))
            else:
                for i in range(8):
                    pieces.append(Pawn(Position("A", 2).recreate(i, 0), True))
                    pieces.append(Pawn(Position("A", 7).recreate(i, 0), False))

                pieces.append(Rook(Position("A", 1), True))
                pieces.append(Rook(Position("H", 1), True))
                pieces.append(Rook(Position("A", 8), False))
                pieces.append(Rook(Position("H", 8), False))

                pieces.append(Knight(Position("B", 1), True))
                pieces.append(Knight(Position("G", 1), True))
                pieces.append(Knight(Position("B", 8), False))
                pieces.append(Knight(Position("G", 8), False))

                pieces.append(Bishop(Position("C", 1), True))
                pieces.append(Bishop(Position("F", 1), True))
                pieces.append(Bishop(Position("C", 8), False))
                pieces.append(Bishop(Position("F", 8), False))

                pieces.append(Queen(Position("D", 1), True))
                pieces.append(Queen(Position("D", 8), False))

                pieces.append(King(Position("E", 1), True))
                pieces.append(King(Position("E", 8), False))

        self.pieces = pieces

    def get_all_legal_moves_for_player(self, is_white: bool, check_for_checks=False):
        all_moves = {}
        for piece in self.pieces:
            if piece.is_white == is_white:
                moves = piece.find_legal_actions(self.pieces)
                if check_for_checks:
                    moves = self.only_leave_king_safe_rules(moves, piece, is_white)
                if moves['attacks'] or moves['moves'] or moves['protections']:
                    all_moves[piece] = moves
        return all_moves

    def get_num_of_queens(self):
        num = 0
        for p in self.pieces:
            if str(p.__class__.__name__) == "Queen":
                num += 1
        return num

    def to_pos(self, loc):
        if type(loc) == str:
            return Position(loc[0], int(loc[1]))
        else:
            return loc

    def act(self, piece_location, destination, is_white, do_print=True):
        start = self.to_pos(piece_location)
        end = self.to_pos(destination)

        piece: Piece = find_piece_by_position(self.pieces, start)
        actions = piece.find_legal_actions(self.pieces)

        if not piece:
            raise Exception("Origin contains no Pieces")
        if piece.is_white != is_white:
            raise Exception("Origin contains no Pieces of yours")
        if end not in actions['moves'] and end not in actions['attacks']:
            raise Exception("Illegal move")

        text = f"{'White' if is_white else 'Black'} {str(piece)} {destination}"

        if end in actions['moves']:
            if str(piece.__class__.__name__) == "King" and piece.initial_position and end.x in (67, 71):
                if end.x == 71:
                    row = "H"
                    rook_end = "F"
                elif end.x == 67:
                    row = "A"
                    rook_end = "D"
                else:
                    print("DHSALDHAJS")
                    exit(312)
                rook = find_piece_by_position(self.pieces, Position(row, piece.position.y))
                if not rook:
                    print("CO KURWA - TO NIE POWINNO SIĘ WYDARZYĆ")
                text += " castles with "
                text += str(rook)
                rook.position = Position(rook_end, rook.position.y)
                rook.initial_position = False
        elif end in actions['attacks']:
            killed = find_piece_by_position(self.pieces, end)
            text += " attacks " + str(killed)
            self.pieces.remove(killed)

            if str(killed.__class__.__name__) == "King" and do_print:
                exit(5)
        else:
            print("CO KURWA - DEBUG THIS to powinno być złapane w wyjątku z illegal move")

        piece.position = end
        piece.initial_position = False
        if str(piece.__class__.__name__) == "Pawn" and end.y in (1, 8):
            self.pieces.append(Queen(piece.position, is_white, False))
            self.pieces.remove(piece)
            text += " and promotes to Queen"
        if do_print:
            print(text)

    def make_new_game(self):
        pieces2 = []
        for p in self.pieces:
            pieces2.append(p.copy())
        return Game(pieces2)

    def only_leave_king_safe_rules(self, moves, piece, is_white):
        new_moves = {"attacks": [], "moves": []}
        for move in moves['moves']:
            new_game = self.make_new_game()
            new_game.act(piece.position, move, is_white, do_print=False)
            king_position = find_king(new_game.pieces, is_white)
            responses = new_game.get_all_legal_moves_for_player(not is_white, check_for_checks=False)
            illegal = True
            for _, actions in responses.items():
                if king_position in actions['attacks']:
                    illegal = True
                    break
                illegal = False
            if not illegal:
                new_moves['moves'].append(move)

        for move in moves['attacks']:
            new_game = self.make_new_game()
            new_game.act(piece.position, move, is_white, do_print=False)
            king_position = find_king(new_game.pieces, is_white)
            responses = new_game.get_all_legal_moves_for_player(not is_white, check_for_checks=False)
            illegal = True
            for _, actions in responses.items():
                if king_position in actions['attacks']:
                    illegal = True
                    break
                illegal = False
            if not illegal:
                new_moves['attacks'].append(move)
        new_moves['protections'] = moves['protections']

        return new_moves

