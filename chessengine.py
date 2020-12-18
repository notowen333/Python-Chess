from colorama import Fore, Back, Style
import copy
import sys


#global constants
rank_letters = {'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h'}
letter_to_rank = {'a': 0, 'b': 1, 'c': 2, 'd': 3, 'e': 4, 'f': 5, 'g': 6, 'h': 7}
rank_to_letter = {v: k for k, v in letter_to_rank.items()}
possiblemoves = set()
for row in range(8):
    for rank in range(8):
        possiblemoves.add((row,rank))

kmoves = {(2,1),(2,-1),(-2,1),(-2,-1),(1,2),(1,-2),(-1,2),(-1,-2)}
kingmoves = {(0,1),(1,0),(1,1),(-1,-1),(-1,0),(0,-1),(1,-1),(-1,1)}

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

    def __str__(self):
        return ('♙' if self.color else '♟')

        

class Rook(Piece):

    def __init__(self, color,pos):
        super().__init__(Rook, color,pos)
        self.hasmoved = False

    def __str__(self):
        return ('♖' if self.color else '♜')

class Knight(Piece):

    def __init__(self, color,pos):
        super().__init__(Knight, color,pos)
    
    def __str__(self):
        return  ('♘' if self.color else '♞')

class Bishop(Piece):

    def __init__(self, color,pos):
        super().__init__(Bishop, color,pos)
    
    def __str__(self):
        return ('♗' if self.color else '♝')



class Queen(Piece):

    def __init__(self, color,pos):
        super().__init__(Queen, color,pos)

    def __str__(self):
        return ('♕' if self.color else '♛')


class King(Piece):

    def __init__(self, color,pos):
        super().__init__(King, color,pos)
        self.hasmoved = False
    
    def __str__(self):
        return ('♔' if self.color else '♚')


class Board:

    def __init__(self,isNew,whitepieces=[],blackpieces=[]):
        self.board = []
    
        if isNew:
            self.whitepieces = []
            w = True
            self.whitepieces.append(Rook(w,(0,0)))  
            self.whitepieces.append(Knight(w,(0,1)))
            self.whitepieces.append(Bishop(w,(0,2)))
            self.whitepieces.append(Queen(w,(0,3)))
            self.whitepieces.append(King(w,(0,4)))
            self.whitepieces.append(Bishop(w,(0,5)))
            self.whitepieces.append(Knight(w,(0,6)))
            self.whitepieces.append(Rook(w,(0,7)))

            for i in range(8):
                self.whitepieces.append(Pawn(w,(1,i)))
            
            self.blackpieces = []
            
            w = False
            self.blackpieces.append(Rook(w,(7,0))) 
            self.blackpieces.append(Knight(w,(7,1)))
            self.blackpieces.append(Bishop(w,(7,2)))
            self.blackpieces.append(Queen(w,(7,3)))
            self.blackpieces.append(King(w,(7,4)))
            self.blackpieces.append(Bishop(w,(7,5)))
            self.blackpieces.append(Knight(w,(7,6)))
            self.blackpieces.append(Rook(w,(7,7)))


            #create black pawns
            for i in range(8):
                self.blackpieces.append(Pawn(w,(6,i)))
        else:
            self.whitepieces = whitepieces
            self.blackpieces = blackpieces
        
        self.enpassant = []

        self.createboard()
        

    def createboard(self):
        self.board = []
        for _ in range (8):
            row = [None, None, None, None, None, None, None, None]
            self.board.append(row)
    
        for Piece in self.whitepieces:
            row, rank = Piece.pos
            self.board[row][rank] = Piece
        for Piece in self.blackpieces:
            row, rank = Piece.pos
            self.board[row][rank] = Piece

    def getWhitePieces(self):
        return self.whitepieces
    
    def getBlackPieces(self):
        return self.blackpieces


    def currInCheck(self, isWhite):

        if isWhite:
            for Piece in self.whitepieces:
                if type(Piece) == King:
                    kingrow, kingrank = Piece.pos
        else:
            for Piece in self.blackpieces:
                if type(Piece) == King:
                    kingrow, kingrank = Piece.pos

        return (kingrow, kingrank) in self.generateControlledSquares(not isWhite)



    def willBeInCheck(self, isWhite, move):

        if move == 'O-O' or move == 'O-O-O':
            return False

        checkwhitepieces = copy.deepcopy(self.whitepieces)
        checkblackpieces = copy.deepcopy(self.blackpieces)

        checkBoard = Board(False,checkwhitepieces,checkblackpieces)
        checkBoard.move(move, isWhite)
        checkBoard.createboard()

        return checkBoard.currInCheck(isWhite)
    
    def generateLegalMoves(self, isWhite):

        l = []
        occupiedpositions = set()

        for Piece in self.whitepieces:
            occupiedpositions.add(Piece.pos)

        for Piece in self.blackpieces: 
            occupiedpositions.add(Piece.pos)

        if isWhite:
            pieces = self.whitepieces
        else:
            pieces = self.blackpieces

        
        controlledOpponent = self.generateControlledSquares(not isWhite)

        inCheck = self.currInCheck(isWhite)

        for Piece in pieces:
            if type(Piece) is Pawn:
                l.append(self.generatePawnMoves(Piece, occupiedpositions,inCheck))
            
            if type(Piece) is Rook:
                l.append(self.generateRookMoves(Piece, occupiedpositions,inCheck))

            if type(Piece) is Knight:
                l.append(self.generateKnightMoves(Piece, occupiedpositions,inCheck))
                
            if type(Piece) is Bishop:
                l.append(self.generateBishopMoves(Piece, occupiedpositions,inCheck))
            
            if type(Piece) is King:
                l.append(self.generateKingMoves(Piece, occupiedpositions,inCheck, controlledOpponent))
            
            if type(Piece) is Queen:
                l.append(self.generateQueenMoves(Piece, occupiedpositions,inCheck))
            
        flat_list = [item for sublist in l for item in sublist]

        kingside, queenside = self.Castle(isWhite)
        if kingside:
            flat_list.append('O-O')
        if queenside:
            flat_list.append('O-O-O')
        
        return flat_list

    
    def generatePawnMoves(self, Pawn, occupiedpositions,inCheck):

        l = []
        row, rank = Pawn.pos
        posstring = rank_to_letter.get(rank) + str(1+row)

        if Pawn.color:
            if not Pawn.hasmoved:
                if (row + 2, rank) in possiblemoves and (row + 2, rank) not in occupiedpositions:
                    move = posstring + '-' + rank_to_letter.get(rank) + str(row + 2 + 1)
                    if not self.willBeInCheck(Pawn.color, move):
                        l.append(move)
                        self.enpassant.append(move)

            
            if (row + 1, rank) in possiblemoves and (row + 1, rank) not in occupiedpositions:
                move = posstring + '-' + rank_to_letter.get(rank) + str(row + 1 + 1)
                if not self.willBeInCheck(Pawn.color, move):
                    l.append(move)
      

            if (row + 1, rank + 1) in possiblemoves:   
                if self.board[row + 1][rank + 1] is not None:
                    if self.board[row + 1][rank + 1].color != Pawn.color:
                        move = posstring+'x'+rank_to_letter.get(rank + 1)+str(row+1 + 1)
                        if not self.willBeInCheck(Pawn.color, move):
                            l.append(move)
         
            if (row + 1, rank -1) in possiblemoves:   
                if self.board[row + 1][rank - 1] is not None:
                    if self.board[row + 1][rank - 1].color != Pawn.color:
                        move = posstring+'x'+rank_to_letter.get(rank - 1)+str(row+1 + 1)
                        if not self.willBeInCheck(Pawn.color, move):
                            l.append(move)
        
        else:
            if not Pawn.hasmoved:
                if (row - 2, rank) in possiblemoves and (row - 2, rank) not in occupiedpositions:
                    move = posstring + '-' + rank_to_letter.get(rank) + str(row - 2 + 1)
                    if not self.willBeInCheck(Pawn.color, move):
                        l.append(move)
            if (row - 1, rank) in possiblemoves and (row - 1, rank) not in occupiedpositions:
                move = posstring + '-' + rank_to_letter.get(rank) + str(row - 1 + 1)
                if not self.willBeInCheck(Pawn.color, move):
                    l.append(move)
                    self.enpassant.append(move)
            
            if (row - 1, rank + 1) in possiblemoves:   
                if self.board[row - 1][rank + 1] is not None:
                    if self.board[row - 1][rank + 1].color != Pawn.color:
                        move = posstring + 'x'+rank_to_letter.get(rank + 1)+str(row-1 + 1)
                        if not self.willBeInCheck(Pawn.color, move):
                            l.append(move)
            
            if (row - 1, rank -1) in possiblemoves:   
                if self.board[row - 1][rank - 1] is not None:
                    if self.board[row - 1][rank - 1].color != Pawn.color:
                        move = posstring+'x'+rank_to_letter.get(rank - 1)+str(row-1 + 1)
                        if not self.willBeInCheck(Pawn.color, move):
                            l.append(move)
        return l


    def generateRookMoves(self, Rook, occupiedpositions,inCheck):

        l = []
        row, rank = Rook.pos
        posstring = 'R' + rank_to_letter.get(rank) + str(1+row)

        #try up
        crow = row + 1
        while crow < 8:
            if (crow,rank) not in occupiedpositions:
                move = posstring + '-' + rank_to_letter.get(rank) + str(crow + 1)
                if not self.willBeInCheck(Rook.color, move):
                    l.append(move)
            else:
                if self.board[crow][rank].color != Rook.color:
                    move = posstring + 'x' + rank_to_letter.get(rank) + str(crow + 1)
                    if not self.willBeInCheck(Rook.color, move):
                        l.append(move)
                else:
                    break
            crow += 1

        #try down
        crow = row - 1
        while crow > - 1:
            if (crow,rank) not in occupiedpositions:
                move = posstring + '-' + rank_to_letter.get(rank) + str(crow + 1)
                if not self.willBeInCheck(Rook.color, move):
                    l.append(move)
            else:
                if self.board[crow][rank].color != Rook.color:
                    move = posstring + 'x' + rank_to_letter.get(rank) + str(crow + 1)
                    if not self.willBeInCheck(Rook.color, move):
                        l.append(move)
                else:
                    break
            crow -= 1

        #try right
        crank = rank + 1
        while crank < 8:
            if (row,crank) not in occupiedpositions:
                move = posstring + '-' + rank_to_letter.get(crank) + str(row + 1)
                if not self.willBeInCheck(Rook.color, move):
                    l.append(move)
            else:
                if self.board[row][crank].color != Rook.color:
                    move = posstring + 'x' + rank_to_letter.get(crank) + str(row + 1)
                    if not self.willBeInCheck(Rook.color, move):
                        l.append(move)
                else:
                    break
            crank += 1

        crank = rank - 1
        while crank > - 1:
            if (row,crank) not in occupiedpositions:
                move = posstring + '-' + rank_to_letter.get(crank) + str(row + 1)
                if not self.willBeInCheck(Rook.color, move):
                    l.append(move)
            else:
                if self.board[row][crank].color != Rook.color:
                    move = posstring + 'x' + rank_to_letter.get(crank) + str(row + 1)
                    if not self.willBeInCheck(Rook.color, move):
                        l.append(move)
                else:
                    break
            crank -= 1

        return l
    
    def generateKnightMoves(self, Knight, occupiedpositions,inCheck):
        
        l = []
        row, rank = Knight.pos
        posstring = 'N' + rank_to_letter.get(rank) + str(row + 1)

        for (tryrow, tryrank) in kmoves:
            if (row + tryrow, rank + tryrank) in possiblemoves:
                if (row + tryrow, rank + tryrank) in occupiedpositions:
                    if self.board[row + tryrow][rank + tryrank].color != Knight.color:
                        move = posstring + 'x' + rank_to_letter.get(rank+tryrank) + str(row + tryrow + 1)
                        if not self.willBeInCheck(Knight.color, move): 
                            l.append(move)
                else:
                    move = posstring + '-' + rank_to_letter.get(rank+tryrank) + str(row + tryrow + 1)
                    if not self.willBeInCheck(Knight.color, move): 
                        l.append(move)
        return l


    
    def generateBishopMoves(self, Bishop, occupiedpositions,inCheck):

        l = []
        row, rank = Bishop.pos
        posstring = 'B' + rank_to_letter.get(rank) + str(1 + row)

        #try NE
        crow = row + 1
        crank = rank + 1
        while crow < 8 and crank < 8:
            if (crow, crank) not in occupiedpositions:
                move = posstring + '-' + rank_to_letter.get(crank) + str(crow + 1)
                if not self.willBeInCheck(Bishop.color, move):
                    l.append(move)
            else:
                if self.board[crow][crank].color != Bishop.color:
                    move = posstring + 'x' + rank_to_letter.get(crank) + str(crow + 1)
                    if not self.willBeInCheck(Bishop.color, move):
                        l.append(move)
                else:
                    break
            crow += 1
            crank += 1

            
        #try NW
        crow = row + 1
        crank = rank - 1
        while crow < 8 and crank > -1:
            if (crow, crank) not in occupiedpositions:
                move = posstring + '-' + rank_to_letter.get(crank) + str(crow + 1)
                if not self.willBeInCheck(Bishop.color, move):
                    l.append(move)
            else:
                if self.board[crow][crank].color != Bishop.color:
                    move = posstring + 'x' + rank_to_letter.get(crank) + str(crow + 1)
                    if not self.willBeInCheck(Bishop.color, move):
                        l.append(move)
                else:
                    break
            crow += 1
            crank -= 1


        #try SE
        crow = row - 1
        crank = rank + 1
        while crow > - 1 and crank < 8:
            if (crow, crank) not in occupiedpositions:
                move = posstring + '-' + rank_to_letter.get(crank) + str(crow + 1)
                if not self.willBeInCheck(Bishop.color, move):
                    l.append(move)
            else:
                if self.board[crow][crank].color != Bishop.color:
                    move = posstring + 'x' + rank_to_letter.get(crank) + str(crow + 1)
                    if not self.willBeInCheck(Bishop.color, move):
                        l.append(move)
                else:
                    break
            crow -= 1
            crank += 1

        #try SW
        crow = row - 1
        crank = rank - 1
        while crow > -1 and crank > -1:
            if (crow, crank) not in occupiedpositions:
                move = posstring + '-' + rank_to_letter.get(crank) + str(crow + 1)
                if not self.willBeInCheck(Bishop.color, move):
                    l.append(move)
            else:
                if self.board[crow][crank].color != Bishop.color:
                    move = posstring + 'x' + rank_to_letter.get(crank) + str(crow + 1)
                    if not self.willBeInCheck(Bishop.color, move):
                        l.append(move)
                else:
                    break
            crow -= 1
            crank -= 1
        
        return l

    
    def generateKingMoves(self, King, occupiedpositions,inCheck, controlledOpponent):

        row, rank = King.pos
        l = []
        posstring = 'K' + rank_to_letter.get(rank) + str(1 + row)

        for (tryrow, tryrank) in kingmoves:
            if (row + tryrow, rank + tryrank) in possiblemoves and (row + tryrow, rank + tryrank) not in occupiedpositions and (row + tryrow,rank + tryrank) not in controlledOpponent:
                l.append((posstring + '-' + rank_to_letter.get(rank + tryrank)+ str(row + tryrow + 1)))
            else:
                if (row + tryrow, rank + tryrank) in possiblemoves and (row + tryrow, rank + tryrank) in occupiedpositions:
                    if self.board[row+tryrow][rank+tryrank].color != King.color:
                        move = posstring + 'x' + rank_to_letter.get(rank+tryrank) + str(row+tryrow+1)
                        if not self.willBeInCheck(King.color, move):
                            l.append(move)
        return l
        
    
    def generateQueenMoves(self, Queen, occupiedpositions,inCheck):
        l = []
        row, rank = Queen.pos
        posstring = 'Q' + rank_to_letter.get(rank) + str(1 + row)

        #try NE
        crow = row + 1
        crank = rank + 1
        while crow < 8 and crank < 8:
            if (crow, crank) not in occupiedpositions:
                move = posstring + '-' + rank_to_letter.get(crank) + str(crow + 1)
                if not self.willBeInCheck(Queen.color, move):
                    l.append(move)
            else:
                if self.board[crow][crank].color != Queen.color:
                    move = posstring + 'x' + rank_to_letter.get(crank) + str(crow + 1)
                    if not self.willBeInCheck(Queen.color, move):
                        l.append(move)
                else:
                    break
            crow += 1
            crank += 1

            
        #try NW
        crow = row + 1
        crank = rank - 1
        while crow < 8 and crank > -1:
            if (crow, crank) not in occupiedpositions:
                move = posstring + '-' + rank_to_letter.get(crank) + str(crow + 1)
                if not self.willBeInCheck(Queen.color, move):
                    l.append(move)
            else:
                if self.board[crow][crank].color != Queen.color:
                    move = posstring + 'x' + rank_to_letter.get(crank) + str(crow + 1)
                    if not self.willBeInCheck(Queen.color, move):
                        l.append(move)
                else:
                    break
            crow += 1
            crank -= 1


        #try SE
        crow = row - 1
        crank = rank + 1
        while crow > -1 and crank < 8:
            if (crow, crank) not in occupiedpositions:
                move = posstring + '-' + rank_to_letter.get(crank) + str(crow + 1)
                if not self.willBeInCheck(Queen.color, move):
                    l.append(move)
            else:
                if self.board[crow][crank].color != Queen.color:
                    move = posstring + 'x' + rank_to_letter.get(crank) + str(crow + 1)
                    if not self.willBeInCheck(Queen.color, move):
                        l.append(move)
                else:
                    break
            crow -= 1
            crank += 1

        #try SW
        crow = row - 1
        crank = rank - 1
        while crow > -1 and crank > -1:
            if (crow, crank) not in occupiedpositions:
                move = posstring + '-' + rank_to_letter.get(crank) + str(crow + 1)
                if not self.willBeInCheck(Queen.color, move):
                    l.append(move)
            else:
                if self.board[crow][crank].color != Queen.color:
                    move = posstring + 'x' + rank_to_letter.get(crank) + str(crow + 1)
                    if not self.willBeInCheck(Queen.color, move):
                        l.append(move)
                else:
                    break
            crow -= 1
            crank -= 1
        

        #try right
        crow = row + 1
        while crow < 8:
            if (crow,rank) not in occupiedpositions:
                move = posstring + '-' + rank_to_letter.get(rank) + str(crow + 1)
                if not self.willBeInCheck(Queen.color, move):
                    l.append(move)
            else:
                if self.board[crow][rank].color != Queen.color:
                    move = posstring + 'x' + rank_to_letter.get(rank) + str(crow + 1)
                    if not self.willBeInCheck(Queen.color, move):
                        l.append(move)
                else:
                    break
            crow += 1

        #try down
        crow = row - 1
        while crow > - 1:
            if (crow,rank) not in occupiedpositions:
                move = posstring + '-' + rank_to_letter.get(rank) + str(crow + 1)
                if not self.willBeInCheck(Queen.color, move):
                    l.append(move)
            else:
                if self.board[crow][rank].color != Queen.color:
                    move = posstring + 'x' + rank_to_letter.get(rank) + str(crow + 1)
                    if not self.willBeInCheck(Queen.color, move):
                        l.append(move)
                else:
                    break
            crow -= 1

        #try right
        crank = rank + 1
        while crank < 8:
            if (row,crank) not in occupiedpositions:
                move = posstring + '-' + rank_to_letter.get(crank) + str(row + 1)
                if not self.willBeInCheck(Queen.color, move):
                    l.append(move)
            else:
                if self.board[row][crank].color != Queen.color:
                    move = posstring + 'x' + rank_to_letter.get(crank) + str(row + 1)
                    if not self.willBeInCheck(Queen.color, move):
                        l.append(move)
                else:
                    break
            crank += 1

        crank = rank - 1
        while crank > -1:
            if (row,crank) not in occupiedpositions:
                move = posstring + '-' + rank_to_letter.get(crank) + str(row + 1)
                if not self.willBeInCheck(Queen.color, move):
                    l.append(move)
            else:
                if self.board[row][crank].color != Queen.color:
                    move = posstring + 'x' + rank_to_letter.get(crank) + str(row + 1)
                    if not self.willBeInCheck(Queen.color, move):
                        l.append(move)
                else:
                    break
            crank -= 1

        return l

    def generateControlledSquares(self, isWhite):

        l = []
        occupiedpositions = set()

        for Piece in self.whitepieces:
            occupiedpositions.add(Piece.pos)

        for Piece in self.blackpieces: 
            occupiedpositions.add(Piece.pos)

        if isWhite:
            pieces = self.whitepieces
        else:
            pieces = self.blackpieces

        for Piece in pieces:
            if type(Piece) is Pawn:
                l.append(self.generatePawnSquares(Piece, occupiedpositions))
            
            if type(Piece) is Rook:
                l.append(self.generateRookSquares(Piece, occupiedpositions))

            if type(Piece) is Knight:
                l.append(self.generateKnightSquares(Piece, occupiedpositions))
                
            if type(Piece) is Bishop:
                l.append(self.generateBishopSquares(Piece, occupiedpositions))
            
            if type(Piece) is King:
                l.append(self.generateKingSquares(Piece, occupiedpositions))
            
            if type(Piece) is Queen:
                l.append(self.generateQueenSquares(Piece, occupiedpositions))

        return [item for sublist in l for item in sublist]

    
    def generatePawnSquares(self, Piece, occupiedpositions):

        row, rank = Piece.pos
        l = []

        if Piece.color:
            if (row + 1, rank + 1) in possiblemoves and (row + 1, rank + 1) not in occupiedpositions:
                l.append((row + 1, rank + 1))
            if (row + 1, rank - 1) in possiblemoves and (row + 1, rank - 1) not in occupiedpositions:
                l.append((row + 1, rank - 1))
        else:
            if (row - 1, rank + 1) in possiblemoves and (row - 1, rank + 1) not in occupiedpositions:
                l.append((row - 1, rank + 1))
            if (row - 1, rank - 1) in possiblemoves and (row - 1, rank - 1) not in occupiedpositions:
                l.append((row - 1, rank - 1))
        return l

    def generateKnightSquares(self, Piece, occupiedpositions):

        l = []
        row, rank = Piece.pos

        for (tryrow, tryrank) in kmoves:
            if (row + tryrow, rank + tryrank) in possiblemoves and (row + tryrow, rank + tryrank):
                l.append((row + tryrow, rank + tryrank))
        return l

    def generateRookSquares(self, Piece, occupiedpositions):

        l = []
        row, rank = Piece.pos

        #try up
        crow = row + 1
        while crow < 8:
            if (crow,rank) not in occupiedpositions:
                l.append((crow, rank))
            else:
                l.append((crow, rank))
                break
            crow += 1

        #try down
        crow = row - 1
        while crow > - 1:
            if (crow,rank) not in occupiedpositions:
                l.append((crow, rank))
            else:
                l.append((crow, rank))
                break
            crow -= 1

        #try right
        crank = rank + 1
        while crank < 8:
            if (row,crank) not in occupiedpositions:
                l.append((row, crank))
            else:
                l.append((row, crank))
                break
            crank += 1

        crank = rank - 1
        while crank > - 1:
            if (row,crank) not in occupiedpositions:
                l.append((row, crank))
            else:
                l.append((row, crank))
                break
            crank -= 1

        return l

    def generateQueenSquares(self, Piece, occupiedpositions):

        l = []
        row, rank = Piece.pos

        #try up
        crow = row + 1
        while crow < 8:
            if (crow,rank) not in occupiedpositions:
                l.append((crow, rank))
            else:
                l.append((crow, rank))
                break
            crow += 1

        #try down
        crow = row - 1
        while crow > - 1:
            if (crow,rank) not in occupiedpositions:
                l.append((crow, rank))
            else:
                l.append((crow, rank))
                break
            crow -= 1

        #try right
        crank = rank + 1
        while crank < 8:
            if (row,crank) not in occupiedpositions:
                l.append((row, crank))
            else:
                l.append((row, crank))
                break
            crank += 1

        crank = rank - 1
        while crank > - 1:
            if (row,crank) not in occupiedpositions:
                l.append((row, crank))
            else:
                l.append((row, crank))
                break
            crank -= 1

        #try NE
        crow = row + 1
        crank = rank + 1
        while crow < 8 and crank < 8:
            if (crow, crank) not in occupiedpositions:
                l.append((crow, crank))
            else:
                l.append((crow, crank))
                break
            crow += 1
            crank += 1

            
        #try NW
        crow = row + 1
        crank = rank - 1
        while crow < 8 and crank > -1:
            if (crow, crank) not in occupiedpositions:
                l.append((crow, crank))
            else:
                l.append((crow, crank))
                break
            crow += 1
            crank -= 1

        #try SE
        crow = row - 1
        crank = rank + 1
        while crow > - 1 and crank < 8:
            if (crow, crank) not in occupiedpositions:
                l.append((crow, crank))
            else:
                l.append((crow, crank))
                break
            crow -= 1
            crank += 1

        #try SW
        crow = row - 1
        crank = rank - 1
        while crow > -1 and crank > -1:
            if (crow, crank) not in occupiedpositions:
                l.append((crow, crank))
            else:
                l.append((crow, crank))
                break
            crow -= 1
            crank -= 1

        return l
    


    def generateKingSquares(self, Piece, occupiedpositions):

        row, rank = Piece.pos
        l = []

        for (tryrow, tryrank) in kingmoves:
            if (row + tryrow, rank + tryrank) in possiblemoves and (row + tryrow, rank + tryrank) not in occupiedpositions:
                l.append((row + tryrow, rank + tryrank))
        
        return l
        

    def generateBishopSquares(self, Piece, occupiedpositions):

        l = []
        row, rank = Piece.pos

        #try NE
        crow = row + 1
        crank = rank + 1
        while crow < 8 and crank < 8:
            if (crow, crank) not in occupiedpositions:
                l.append((crow, crank))
            else:
                l.append((crow, crank))
                break
            crow += 1
            crank += 1

            
        #try NW
        crow = row + 1
        crank = rank - 1
        while crow < 8 and crank > -1:
            if (crow, crank) not in occupiedpositions:
                l.append((crow, crank))
            else:
                l.append((crow, crank))
                break
            crow += 1
            crank -= 1


        #try SE
        crow = row - 1
        crank = rank + 1
        while crow > - 1 and crank < 8:
            if (crow, crank) not in occupiedpositions:
                l.append((crow, crank))
            else:
                l.append((crow, crank))
                break
            crow -= 1
            crank += 1

        #try SW
        crow = row - 1
        crank = rank - 1
        while crow > -1 and crank > -1:
            if (crow, crank) not in occupiedpositions:
                l.append((crow, crank))
            else:
                l.append((crow, crank))
                break
            crow -= 1
            crank -= 1
        
        return l

    def Castle(self,isWhite):

        kingside = True
        queenside = True
        controlled = self.generateControlledSquares(not isWhite)


        if isWhite:
            row = 0
        else:
            row = 7


        if (row, 5) in controlled:
            kingside = False
        
        if (row, 6) in controlled:
            kingside = False
        
        if (row, 1) in controlled:
            queenside = False
        
        if (row, 2) in controlled:
            queenside = False
        
        if (row, 3) in controlled:
            queenside = False

        if type(self.board[row][4]) != King:
            return (False, False)
            
        if self.board[row][4].hasmoved:
            return (False, False)

        if type(self.board[row][7]) != Rook:
            kingside = False
        else:
            if self.board[row][7].hasmoved:
                kingside = False
        
        if type(self.board[row][0]) != Rook:
            queenside = False
        else:
            if self.board[row][0].hasmoved:
                queenside = False
        
        if self.board[row][5] is not None:
            kingside = False
        
        if self.board[row][6] is not None:
            kingside = False
        
        if self.board[row][1] is not None:
            queenside = False
        
        if self.board[row][2] is not None:
            queenside = False
        
        if self.board[row][3] is not None:
            queenside = False

        return (kingside, queenside)
        
        

    def move(self, move, whiteToMove):


        if whiteToMove:
            castlerow = 0
        else:
            castlerow = 7

        if move == 'O-O':
            self.board[castlerow][4].pos = (castlerow, 6)
            self.board[castlerow][7].pos = (castlerow, 5)
            return

        if move == 'O-O-O':
            self.board[castlerow][4].pos = (castlerow, 2)
            self.board[castlerow][0].pos = (castlerow, 3)
            return

        if move[0] in rank_letters:
            crow = int(move[1]) - 1
            crank = letter_to_rank.get(move[0])
        else:
            crow = int(move[2]) - 1
            crank = letter_to_rank.get(move[1])

        currPiece = self.board[crow][crank]

        if type(currPiece) == Pawn:
            currPiece.hasmoved = True
        
        if type(currPiece) == King:
            currPiece.hasmoved = True
        
        if type(currPiece) == Rook:
            currPiece.hasmoved = True
        

        if '-' in move:
            target = move.split('-',1)[1]
            targetrow = int(target[1]) - 1
            targetrank = letter_to_rank.get(target[0])

            currPiece.move((targetrow, targetrank))

        if 'x' in move:
            color = self.board[crow][crank].color
            target = move.split('x',1)[1]
            targetrow = int(target[1]) - 1 
            targetrank = letter_to_rank.get(target[0])

            if color:
                self.blackpieces.remove(self.board[targetrow][targetrank])
            else:
                self.whitepieces.remove(self.board[targetrow][targetrank])
            
            currPiece.move((targetrow, targetrank))
        

    
    def __str__(self):

        rowtoprint = ['  ', 'a  ', 'b  ', 'c  ','d  ','e  ','f  ','g  ','h  ']
        for row in range(7,-1,-1):
            print(''.join(rowtoprint))
            rowtoprint = [Back.RESET + str(row + 1)]
            for rank in range(8):
                if (row + rank) % 2 == 0:
                    if self.board[row][rank] is None:
                        rowtoprint.append(Back.CYAN + '   ')
                    else:
                        rowtoprint.append(Back.CYAN + ' ' + str(self.board[row][rank]) + ' ')
                else:
                    if self.board[row][rank] is None: 
                        rowtoprint.append(Back.WHITE + '   ')
                    else:
                        rowtoprint.append(Back.WHITE + ' ' + str(self.board[row][rank])+ ' ')
                rowtoprint.append(Back.RESET + '')
        rowtoprint.append(Back.RESET + '')
        print(''.join(rowtoprint))        
        
        return ""




#game start
board = Board(True)
print(board)
whiteToMove = True

while True:

    legalMoves = board.generateLegalMoves(whiteToMove)
    inCheck = board.currInCheck(whiteToMove)

    if inCheck:
        print('Check')


    if not legalMoves and inCheck:
        print('Checkmate')
        sys.exit()
    
    if not legalMoves:
        print('Stalemate')
        sys.exit()


    validMove = True
    while validMove:
        if whiteToMove:
            entered_move = input('White to move: ')
        else:
            entered_move = input('Black to move: ')
        
        if entered_move in legalMoves:
            validMove = False

    
    board.move(entered_move, whiteToMove)

    board.createboard()
    print(board)


    whiteToMove = not whiteToMove





