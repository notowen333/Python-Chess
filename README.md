# Python-Chess
Chess built out in python to be played in the terminal. Eventually a chess AI will be added.

This Chess game uses long-form algebraic chess notation (So you say e2-e4, instead of e4, or you say Kb1xc3 to
say knight takes on c3). 

Right now, it's missing en-passant, insufficient material checks, and 50 king move stalemates.

The structure of the code is Object Oriented. Each piece is an object that has a __str__ method, a color, and a position. The board is an object that has a list of white pieces, a list of black pieces, most of the gameplay methods, and a __str__ method. The board is re-rendered after each move using the __str__ method to show all of the pieces which remain.

To show the background of the board, I use the colorama python library, and I use unicode characters to display the pieces.

I have a test_chess file which contains unit tests.

Before each move, all possible moves are generated and displayed. This includes double moves for pawns, kingside and queenside castles, checks to make sure a piece is not pinned, and captures. I check for illegal moves by creating a hypothetical board and checking to see if a player is in check. 

After a move is played, the game checks for stalemates where a player has no available moves and for repitition stalemates by hashing the board and checking if any hash points to a value of 3. Then the game auto-queens any pawns in the their respective final row.

Of course, the game ends with checkmate when a player is in check and has no available moves.

Gameplay Images:

**Gameplay**
![Gameplay](https://user-images.githubusercontent.com/51685858/103182577-702adf80-487a-11eb-9c55-b122a9f5b563.png)

**Scholar's Mate**
![Checkmate](https://user-images.githubusercontent.com/51685858/102663100-24778800-414e-11eb-9d4a-b4aee24581a2.jpg)

**Pawn Promotion**
![Promote](https://user-images.githubusercontent.com/51685858/103261929-49030980-4971-11eb-9db2-f3bd5dc0fc73.png)

**Stalemate**
![Stale](https://user-images.githubusercontent.com/51685858/103261953-620bba80-4971-11eb-9e40-fd156bcad1d4.png)


cicd demo

