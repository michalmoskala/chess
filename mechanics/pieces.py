from abc import ABC
from utils import *


class Piece(ABC):
    def __init__(self, position, is_white, initial_position=True):
        self.position = position
        self.is_white = is_white
        self.value = None
        self.initial_position = initial_position

    def find_legal_actions(self, other_pieces):
        raise NotImplemented

    def find_legal_attacks(self, other_pieces):
        raise NotImplemented

    def is_opposite(self, other):
        if self.is_white != other.is_white:
            return True
        return False

    def __str__(self):
        return str(self.__class__.__name__) + " " + str(self.position)

    def get_details(self):
        return str(self.__class__.__name__), str(self.position), self.value

    def go_or_attack(self, other_pieces, moves, attacks, i, j, protections):
        move = self.position.recreate(i, j)
        if check_if_position_is_free(other_pieces, move):
            moves.append(move)
            protections.append(move)
        else:
            protections.append(move)
            enemy = find_piece_by_position(other_pieces, move)
            if enemy:
                if self.is_opposite(enemy):
                    attacks.append(move)
            return True

    def attack(self, other_pieces, i, j, attacks):
        for k in range(1, 8):
            move = self.position.recreate(i*k, j*k)
            if not check_if_position_is_free(other_pieces, move):
                enemy = find_piece_by_position(other_pieces, move)
                if enemy:
                    if self.is_opposite(enemy):
                        attacks.append(move)

    def copy(self):
        if str(self.__class__.__name__) == "Queen":
            return Queen(self.position.recreate(0, 0), self.is_white, self.initial_position)
        if str(self.__class__.__name__) == "King":
            return King(self.position.recreate(0, 0), self.is_white, self.initial_position)
        if str(self.__class__.__name__) == "Pawn":
            return Pawn(self.position.recreate(0, 0), self.is_white, self.initial_position)
        if str(self.__class__.__name__) == "Rook":
            return Rook(self.position.recreate(0, 0), self.is_white, self.initial_position)
        if str(self.__class__.__name__) == "Knight":
            return Knight(self.position.recreate(0, 0), self.is_white, self.initial_position)
        if str(self.__class__.__name__) == "Bishop":
            return Bishop(self.position.recreate(0, 0), self.is_white, self.initial_position)


class Pawn(Piece):
    def __init__(self, position, is_white, initial=True):
        super().__init__(position, is_white, initial)
        self.value = 1

    def find_legal_actions(self, other_pieces):
        if self.is_white:
            jump = 1
        else:
            jump = -1

        moves = []

        move = self.position.recreate(0, jump)
        if check_if_position_is_free(other_pieces, move):
            moves.append(move)
            move = self.position.recreate(0, jump * 2)
            if check_if_position_is_free(other_pieces, move) and self.initial_position:
                moves.append(move)

        attacks = []
        protections = []

        attack = self.position.recreate(1, jump)
        piece = find_piece_by_position(other_pieces, attack)

        if piece:
            if self.is_opposite(piece):
                attacks.append(attack)
        protections.append(attack)

        attack = self.position.recreate(-1, jump)
        piece = find_piece_by_position(other_pieces, attack)
        if piece:
            if self.is_opposite(piece):
                attacks.append(attack)
        protections.append(attack)

        return {"moves": moves, "attacks": attacks, "protections": protections}


class Rook(Piece):
    def __init__(self, position, is_white, initial=True):
        super().__init__(position, is_white, initial)
        self.value = 5

    def find_legal_actions(self, other_pieces):
        moves = []
        attacks = []
        protections = []
        for i in range(1, 8):
            if self.go_or_attack(other_pieces, moves, attacks, i, 0, protections):
                break
        for i in range(-1, -8, -1):
            if self.go_or_attack(other_pieces, moves, attacks, i, 0, protections):
                break
        for i in range(1, 8):
            if self.go_or_attack(other_pieces, moves, attacks, 0, i, protections):
                break
        for i in range(-1, -8, -1):
            if self.go_or_attack(other_pieces, moves, attacks, 0, i, protections):
                break

        return {"moves": moves, "attacks": attacks, "protections": protections}


class Bishop(Piece):
    def __init__(self, position, is_white, initial=True):
        super().__init__(position, is_white, initial)
        self.value = 3

    def find_legal_actions(self, other_pieces):
        moves = []
        attacks = []
        protections = []
        for i in range(1, 8):
            if self.go_or_attack(other_pieces, moves, attacks, i, i, protections):
                break
        for i in range(1, 8):
            if self.go_or_attack(other_pieces, moves, attacks, i, -i, protections):
                break
        for i in range(1, 8):
            if self.go_or_attack(other_pieces, moves, attacks, -i, i, protections):
                break
        for i in range(1, 8):
            if self.go_or_attack(other_pieces, moves, attacks, -i, -i, protections):
                break

        return {"moves": moves, "attacks": attacks, "protections": protections}


class Queen(Piece):
    def __init__(self, position, is_white, initial=True):
        super().__init__(position, is_white, initial)
        self.value = 8

    def find_legal_actions(self, other_pieces):
        b = Bishop(self.position.recreate(0, 0), self.is_white).find_legal_actions(other_pieces)
        r = Rook(self.position.recreate(0, 0), self.is_white).find_legal_actions(other_pieces)
        return {"moves": b["moves"] + r["moves"], "attacks": b["attacks"] + r["attacks"], "protections": b['protections']+r['protections']}


class King(Piece):
    def __init__(self, position, is_white, initial=True):
        super().__init__(position, is_white, initial)
        self.value = 100

    def find_legal_actions(self, other_pieces):
        moves = []
        attacks = []
        protections = []
        for i in range(-1, 2):
            for j in range(-1, 2):
                if i != 0 or j != 0:
                    self.go_or_attack(other_pieces, moves, attacks, i, j, protections)
        row = 1 if self.is_white else 8

        rr = find_piece_by_position(other_pieces, Position("H", row))
        if self.initial_position and rr:
            if rr.initial_position and not find_piece_by_position(other_pieces, Position("G", row)) and not find_piece_by_position(other_pieces, Position("F", row)):
                moves.append(Position("G", row))

        lr = find_piece_by_position(other_pieces, Position("A", row))
        if self.initial_position and lr:
            if lr.initial_position and not find_piece_by_position(other_pieces, Position("D", row)) and not find_piece_by_position(other_pieces, Position("B", row)) and not find_piece_by_position(other_pieces, Position("C", row)):
                moves.append(Position("C", row))

        return {"moves": moves, "attacks": attacks, "protections": protections}


class Knight(Piece):
    def __init__(self, position, is_white, initial=True):
        super().__init__(position, is_white, initial)
        self.value = 3

    def find_legal_actions(self, other_pieces):
        moves = []
        attacks = []
        protections = []
        self.go_or_attack(other_pieces, moves, attacks, 2, -1, protections)
        self.go_or_attack(other_pieces, moves, attacks, 2, 1, protections)

        self.go_or_attack(other_pieces, moves, attacks, -2, 1, protections)
        self.go_or_attack(other_pieces, moves, attacks, -2, -1, protections)

        self.go_or_attack(other_pieces, moves, attacks, 1, -2, protections)
        self.go_or_attack(other_pieces, moves, attacks, 1, 2, protections)

        self.go_or_attack(other_pieces, moves, attacks, -1, 2, protections)
        self.go_or_attack(other_pieces, moves, attacks, -1, -2, protections)

        return {"moves": moves, "attacks": attacks, "protections": protections}
