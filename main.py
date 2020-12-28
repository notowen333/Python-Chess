from chessengine.board import Board
import sys

def main():
    currboard = Board(True)
    whiteToMove = True

    while True:

        legalMoves = currboard.generateLegalMoves(whiteToMove)
        print(legalMoves)
        print(currboard)
        inCheck = currboard.currInCheck(whiteToMove)

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

        
        currboard.move(entered_move, whiteToMove)
        if currboard.isStale():
            print(currboard)
            print('Stalemate by repitition')
            sys.exit()

        currboard.createboard()
        whiteToMove = not whiteToMove


if __name__ == '__main__':
    main()
