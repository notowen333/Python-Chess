class Piece:

    def __init__(self, type = None, color = None, pos = (0,0)):
        self.type = type
        self.color = color
        self.pos = pos

    def move(self, pos):
        self.pos = pos

class Pawn(Piece):

    def __init__(self,color,pos):
        super().__init__(Pawn, color,pos)
        self.hasmoved = False
        self.pieceHash = 17

    def __str__(self):
        return ('♙' if self.color else '♟')

    
class Rook(Piece):

    def __init__(self, color,pos):
        super().__init__(Rook, color,pos)
        self.hasmoved = False
        self.pieceHash = 53

    def __str__(self):
        return ('♖' if self.color else '♜')

class Knight(Piece):

    def __init__(self, color,pos):
        super().__init__(Knight, color,pos)
        self.pieceHash = 1571
    
    def __str__(self):
        return  ('♘' if self.color else '♞')

class Bishop(Piece):

    def __init__(self, color,pos):
        super().__init__(Bishop, color,pos)
        self.pieceHash = 2089
    
    def __str__(self):
        return ('♗' if self.color else '♝')


class Queen(Piece):

    def __init__(self, color,pos):
        super().__init__(Queen, color,pos)
        self.pieceHash = 2239

    def __str__(self):
        return ('♕' if self.color else '♛')


class King(Piece):

    def __init__(self, color,pos):
        super().__init__(King, color,pos)
        self.hasmoved = False
        self.pieceHash = 1667
    
    def __str__(self):
        return ('♔' if self.color else '♚')