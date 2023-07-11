def find_piece_by_position(pieces, position):
    for piece in pieces:
        if piece.position == position:
            return piece
    return None


def check_if_position_is_free(pieces, position):
    for piece in pieces:
        if piece.position == position or position.is_out_of_bounds():
            return False
    return True


def find_king(pieces, is_white):
    for piece in pieces:
        if str(piece.__class__.__name__) == "King" and piece.is_white == is_white:
            return piece.position


class Position:
    def __init__(self, x, y):
        try:
            self.x = ord(x)
        except TypeError:
            self.x = x
        self.y = y

    def __str__(self):
        return f"{chr(self.x)}{self.y}"

    def __repr__(self):
        return f"{chr(self.x)}{self.y}"

    def __eq__(self, other):
        if self.x == other.x and self.y == other.y:
            return True
        return False

    def is_out_of_bounds(self):
        if self.y > 8 or self.y < 1 or self.x < 65 or self.x > 72:
            return True
        return False

    def recreate(self, horizontal, vertical):
        p = Position(self.x, self.y)
        p.move_vertically(vertical)
        p.move_horizontally(horizontal)
        return p

    def move_vertically(self, vector: int):
        self.y += vector

    def move_horizontally(self, vector: int):
        self.x += vector
