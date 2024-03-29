from colorama import Fore, Back, Style
import copy
import sys
from chessengine.pieces import Pawn, Rook, Knight, Queen, King, Bishop, Piece
import hashlib


#global constants
rank_letters = {'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h'}
letter_to_rank = {'a': 0, 'b': 1, 'c': 2, 'd': 3, 'e': 4, 'f': 5, 'g': 6, 'h': 7}
rank_to_letter = {v: k for k, v in letter_to_rank.items()}
BOARD_SIZE = 8

#all coordinates on the board
possiblemoves = set()
for row in range(BOARD_SIZE):
    for rank in range(BOARD_SIZE):
        possiblemoves.add((row,rank))

#possible coordinate deltas for knights/kings
kmoves = {(2,1),(2,-1),(-2,1),(-2,-1),(1,2),(1,-2),(-1,2),(-1,-2)}
kingmoves = {(0,1),(1,0),(1,1),(-1,-1),(-1,0),(0,-1),(1,-1),(-1,1)}


#back row coordinates for pawn promotion
backrow = set()
rows_to_check = {0,7}
for row in rows_to_check:
    for rank in range(BOARD_SIZE):
        backrow.add((row,rank))



class Board:

    def __init__(self,isNew,whitepieces=[],blackpieces=[]):
        self.board = []
        self.stale_game = {}
        self.movecounter = 0
    
        #routine for initialzing a board
        if isNew:

            self.whitepieces = []
            self.blackpieces = []
            plist = [Rook, Knight, Bishop, Queen, King, Bishop, Knight, Rook]
            for (i,p) in enumerate(plist):
                self.whitepieces.append(p(True,(0,i)))
                self.blackpieces.append(p(False,(7,i)))

            for i in range(BOARD_SIZE):
                 self.whitepieces.append(Pawn(True,(1,i)))
                 self.blackpieces.append(Pawn(False,(6,i)))
        #routine for creating a hypothetical board (used when checking for valid moves)
        else:
            self.whitepieces = whitepieces
            self.blackpieces = blackpieces

        #not yet implemented--reminder
        self.enpassant = []

        self.createboard()


    #updates board with positions of each piece and leaves None in empty squares
    #called after each move in the main method
    def createboard(self):
        self.board = []
        for _ in range (BOARD_SIZE):
            row = [None, None, None, None, None, None, None, None]
            self.board.append(row)

        for Piece in (self.whitepieces + self.blackpieces):
            row, rank = Piece.pos
            self.board[row][rank] = Piece

    def getWhitePieces(self):
        return self.whitepieces
    
    def getBlackPieces(self):
        return self.blackpieces

    #checks to see if a given player is currently in check with the generateControlledSquares method
    def currInCheck(self, isWhite):

        pieces = self.whitepieces if isWhite else self.blackpieces

        for Piece in pieces:
            if type(Piece) == King:
                kingrow, kingrank = Piece.pos

        return (kingrow, kingrank) in self.generateControlledSquares(not isWhite)


    #creates a hypothetical board where the move is made and sees if it would result in putting the player in check
    #uses deepcopy to deal with pointer issues
    def willBeInCheck(self, isWhite, move):

        if move == 'O-O' or move == 'O-O-O':
            return False

        checkwhitepieces = copy.deepcopy(self.whitepieces)
        checkblackpieces = copy.deepcopy(self.blackpieces)

        checkBoard = Board(False,checkwhitepieces,checkblackpieces)
        checkBoard.move(move, isWhite)
        checkBoard.createboard()

        return checkBoard.currInCheck(isWhite)
    
    #generates a list of legal moves
    def generateLegalMoves(self, isWhite):

        l = []
        occupiedpositions = set()

        for Piece in (self.whitepieces + self.blackpieces):
            occupiedpositions.add(Piece.pos)

        pieces = self.whitepieces if isWhite else self.blackpieces
        controlledOpponent = self.generateControlledSquares(not isWhite)
        inCheck = self.currInCheck(isWhite)

        methodDict = {Pawn: self.generatePawnMoves, Rook: self.generateRookMoves, Knight: self.generateKnightMoves, Bishop: self.generateBishopMoves,
              King: self.generateKingMoves, Queen: self.generateQueenMoves}
        for Piece in pieces:
                if type(Piece) is King:
                    l.append(self.generateKingMoves(Piece, occupiedpositions,inCheck, controlledOpponent))
                else:
                    l.append(methodDict[type(Piece)](Piece, occupiedpositions,inCheck))
            
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
        while crow < BOARD_SIZE:
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
        while crank < BOARD_SIZE:
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
        while crow < BOARD_SIZE and crank < BOARD_SIZE:
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
        while crow < BOARD_SIZE and crank > -1:
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
        while crow > - 1 and crank < BOARD_SIZE:
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
        while crow < BOARD_SIZE and crank < BOARD_SIZE:
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
        while crow < BOARD_SIZE and crank > -1:
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
        while crow > -1 and crank < BOARD_SIZE:
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
        while crow < BOARD_SIZE:
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
        while crank < BOARD_SIZE:
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

        for Piece in self.whitepieces + self.blackpieces:
            occupiedpositions.add(Piece.pos)

        pieces = self.whitepieces if isWhite else self.blackpieces

        pp = {Pawn: self.generatePawnSquares, Rook: self.generateRookSquares, Knight: self.generateKnightSquares, Bishop: self.generateBishopSquares,
              King: self.generateKingSquares, Queen: self.generateQueenSquares}
        for Piece in pieces:
            l.append(pp[type(Piece)](Piece, occupiedpositions))

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
        while crow < BOARD_SIZE:
            l.append((crow, rank))
            if (crow,rank) in occupiedpositions:
                break
            crow += 1

        #try down
        crow = row - 1
        while crow > - 1:
            l.append((crow, rank))
            if (crow,rank) in occupiedpositions:
                break
            crow -= 1

        #try right
        crank = rank + 1
        while crank < BOARD_SIZE:
            l.append((row, crank))
            if (row,crank) in occupiedpositions:
                break
            crank += 1

        crank = rank - 1
        while crank > - 1:
            l.append((row, crank))
            if (row,crank) in occupiedpositions:
                break
            crank -= 1

        return l

    def generateQueenSquares(self, Piece, occupiedpositions):
       return self.generateBishopSquares(Piece, occupiedpositions) + self.generateRookSquares(Piece, occupiedpositions)
        
    
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
        while crow < BOARD_SIZE and crank < BOARD_SIZE:
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
        while crow < BOARD_SIZE and crank > -1:
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
        while crow > - 1 and crank < BOARD_SIZE:
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


    def promote(self):     
        for i in range(2):
            pieces = self.whitepieces if i % 2 == 0 else self.blackpieces
            j = 0
            while j < len(pieces):
                piece = pieces[j]
                if type(piece) is Pawn and piece.pos in backrow:
                    row, col = piece.pos
                    color = piece.color
                    pieces[j] = Queen(color, (row,col))
                j += 1
        

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

        pieceset = {Pawn, King, Rook}

        if type(currPiece) in pieceset:
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

        self.hashBoard()
        self.promote()
        
        self.movecounter += 1

    def hashBoard(self):
        
        hash_key = hashlib.sha256(str(self.board).encode('utf-8')).hexdigest()
        try:
            self.stale_game[hash_key] += 1
        except KeyError:
            self.stale_game[hash_key] = 1

    def isStale(self):
        return max(self.stale_game.values()) >= 3
        
    
    def __str__(self):

        rowtoprint = ['  ', 'a  ', 'b  ', 'c  ','d  ','e  ','f  ','g  ','h  ']
        for row in range(7,-1,-1):
            print(''.join(rowtoprint))
            rowtoprint = [Back.RESET + str(row + 1)]
            for rank in range(BOARD_SIZE):
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