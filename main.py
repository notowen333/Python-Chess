from chessengine.board import Board
import sys
print('cherries\n')


def main():
    print('bananas\n\n\n')
    currboard = Board(True)
    whiteToMove = True

    while True:

        legalMoves = currboard.generateLegalMoves(whiteToMove)
        print(legalMoves)
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

        currboard.createboard()
        print(currboard)


        whiteToMove = not whiteToMove


if __name__ == '__main__':
    print('apples ... and ')
    main()