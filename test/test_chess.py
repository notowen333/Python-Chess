from typing import ClassVar
import unittest
from chessengine.board import Board 

class TestChess(unittest.TestCase):

    def test_badmove(self):
        test_board = Board(True)
        waserr = False
        try:
            test_board.move('fdsjkl', True)
        except:
            waserr = True
        self.assertTrue(waserr)

    def test_newboard(self):
        test_board = Board(True)
        legal_moves = test_board.generateLegalMoves(True)
        self.assertEqual(legal_moves, ['Nb1-a3', 'Nb1-c3', 'Ng1-f3', 'Ng1-h3', 'a2-a4', 'a2-a3', 'b2-b4', 'b2-b3', 'c2-c4', 'c2-c3', 'd2-d4', 'd2-d3', 'e2-e4', 'e2-e3', 'f2-f4', 'f2-f3', 'g2-g4', 'g2-g3', 'h2-h4', 'h2-h3'])

    def test_scholar(self):
        move_list = ['e2-e4', 'e7-e5','Bf1-c4']
        check_list = [
              ['Nb1-a3', 'Nb1-c3', 'Ng1-f3', 'Ng1-h3', 'a2-a4', 'a2-a3', 'b2-b4', 'b2-b3', 'c2-c4', 'c2-c3', 'd2-d4', 'd2-d3', 'e2-e4', 'e2-e3', 'f2-f4', 'f2-f3', 'g2-g4', 'g2-g3', 'h2-h4', 'h2-h3'],
              ['Nb8-a6', 'Nb8-c6', 'Ng8-f6', 'Ng8-h6', 'a7-a5', 'a7-a6', 'b7-b5', 'b7-b6', 'c7-c5', 'c7-c6', 'd7-d5', 'd7-d6', 'e7-e5', 'e7-e6', 'f7-f5', 'f7-f6', 'g7-g5', 'g7-g6', 'h7-h5', 'h7-h6'],
              ['Nb1-a3', 'Nb1-c3', 'Qd1-e2', 'Qd1-f3', 'Qd1-g4', 'Qd1-h5', 'Ke1-e2', 'Bf1-e2', 'Bf1-d3', 'Bf1-c4', 'Bf1-b5', 'Bf1-a6', 'Ng1-f3', 'Ng1-h3', 'Ng1-e2', 'a2-a4', 'a2-a3', 'b2-b4', 'b2-b3', 'c2-c4', 'c2-c3', 'd2-d4', 'd2-d3', 'f2-f4', 'f2-f3', 'g2-g4', 'g2-g3', 'h2-h4', 'h2-h3'],
              ['Nb8-a6', 'Nb8-c6', 'Qd8-e7', 'Qd8-f6', 'Qd8-g5', 'Qd8-h4', 'Ke8-e7', 'Bf8-e7', 'Bf8-d6', 'Bf8-c5', 'Bf8-b4', 'Bf8-a3', 'Ng8-f6', 'Ng8-e7', 'Ng8-h6', 'a7-a5', 'a7-a6', 'b7-b5', 'b7-b6', 'c7-c5', 'c7-c6', 'd7-d5', 'd7-d6', 'f7-f5', 'f7-f6', 'g7-g5', 'g7-g6', 'h7-h5', 'h7-h6']
             ]

        test_board = Board(True)
        white_to_move = True

        for (i, move) in enumerate(move_list):
            legal_moves = test_board.generateLegalMoves(white_to_move)
            self.assertEqual(legal_moves, check_list[i])
            test_board.move(move,white_to_move)
            test_board.createboard()
            white_to_move = not white_to_move

    def test_longer(self):
        move_list = ['a2-a3','Nb8-a6','Ra1-a2','Na6-b4','d2-d3','Nb4xc2','Ke1-d2','c7-c5','Kd2xc2','c5-c4']
        check_list = [
            ['Nb1-a3', 'Nb1-c3', 'Ng1-f3', 'Ng1-h3', 'a2-a4', 'a2-a3', 'b2-b4', 'b2-b3', 'c2-c4', 'c2-c3', 'd2-d4', 'd2-d3', 'e2-e4', 'e2-e3', 'f2-f4', 'f2-f3', 'g2-g4', 'g2-g3', 'h2-h4', 'h2-h3'],
            ['Nb8-a6', 'Nb8-c6', 'Ng8-f6', 'Ng8-h6', 'a7-a5', 'a7-a6', 'b7-b5', 'b7-b6', 'c7-c5', 'c7-c6', 'd7-d5', 'd7-d6', 'e7-e5', 'e7-e6', 'f7-f5', 'f7-f6', 'g7-g5', 'g7-g6', 'h7-h5', 'h7-h6'],
            ['Ra1-a2', 'Nb1-c3', 'Ng1-f3', 'Ng1-h3', 'a3-a4', 'b2-b4', 'b2-b3', 'c2-c4', 'c2-c3', 'd2-d4', 'd2-d3', 'e2-e4', 'e2-e3', 'f2-f4', 'f2-f3', 'g2-g4', 'g2-g3', 'h2-h4', 'h2-h3'],
            ['Ra8-b8', 'Na6-b8', 'Na6-b4', 'Na6-c5', 'Ng8-f6', 'Ng8-h6', 'a7-a5', 'b7-b5', 'b7-b6', 'c7-c5', 'c7-c6', 'd7-d5', 'd7-d6', 'e7-e5', 'e7-e6', 'f7-f5', 'f7-f6', 'g7-g5', 'g7-g6', 'h7-h5', 'h7-h6'],
            ['Ra2-a1', 'Nb1-c3', 'Ng1-f3', 'Ng1-h3', 'a3-a4', 'a3xb4', 'b2-b3', 'c2-c4', 'c2-c3', 'd2-d4', 'd2-d3', 'e2-e4', 'e2-e3', 'f2-f4', 'f2-f3', 'g2-g4', 'g2-g3', 'h2-h4', 'h2-h3'],
            ['Ra8-b8', 'Nb4-a6', 'Nb4-d5', 'Nb4xa2', 'Nb4-c6', 'Nb4xc2', 'Nb4xd3', 'Ng8-f6', 'Ng8-h6', 'a7-a5', 'a7-a6', 'b7-b5', 'b7-b6', 'c7-c5', 'c7-c6', 'd7-d5', 'd7-d6', 'e7-e5', 'e7-e6', 'f7-f5', 'f7-f6', 'g7-g5', 'g7-g6', 'h7-h5', 'h7-h6'],
            ['Qd1xc2', 'Ke1-d2'],
            ['Ra8-b8', 'Nc2-b4', 'Nc2-e3', 'Nc2-d4', 'Nc2-a1', 'Nc2xa3', 'Nc2-e1', 'Ng8-f6', 'Ng8-h6', 'a7-a5', 'a7-a6', 'b7-b5', 'b7-b6', 'c7-c5', 'c7-c6', 'd7-d5', 'd7-d6', 'e7-e5', 'e7-e6', 'f7-f5', 'f7-f6', 'g7-g5', 'g7-g6', 'h7-h5', 'h7-h6'],
            ['Ra2-a1', 'Nb1-c3', 'Qd1xc2', 'Qd1-b3', 'Qd1-a4', 'Qd1-e1', 'Kd2-c3', 'Kd2xc2', 'Ng1-f3', 'Ng1-h3', 'a3-a4', 'b2-b4', 'b2-b3', 'd3-d4', 'e2-e4', 'e2-e3', 'f2-f4', 'f2-f3', 'g2-g4', 'g2-g3', 'h2-h4', 'h2-h3'],
            ['Ra8-b8', 'Qd8-c7', 'Qd8-b6', 'Qd8-a5', 'Ng8-f6', 'Ng8-h6', 'a7-a5', 'a7-a6', 'b7-b5', 'b7-b6', 'c5-c4', 'd7-d5', 'd7-d6', 'e7-e5', 'e7-e6', 'f7-f5', 'f7-f6', 'g7-g5', 'g7-g6', 'h7-h5', 'h7-h6'],
            ['Ra2-a1', 'Nb1-d2', 'Nb1-c3', 'Bc1-d2', 'Bc1-e3', 'Bc1-f4', 'Bc1-g5', 'Bc1-h6', 'Qd1-d2', 'Qd1-e1', 'Kc2-d2', 'Kc2-c3', 'Ng1-f3', 'Ng1-h3', 'a3-a4', 'b2-b4', 'b2-b3', 'd3-d4', 'd3xc4', 'e2-e4', 'e2-e3', 'f2-f4', 'f2-f3', 'g2-g4', 'g2-g3', 'h2-h4', 'h2-h3'],   
        ]
        
        tb = Board(True)

        for i, move in enumerate(move_list):
            white_to_move = True if i % 2 == 0 else False
            legal_moves = tb.generateLegalMoves(white_to_move)
            self.assertEqual(legal_moves, check_list[i])
            tb.move(move,white_to_move)
            tb.createboard()

if __name__ == '__main__':
    unittest.main()