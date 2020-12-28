# Python-Chess
Chess built out in python to be played in the terminal. Eventually a chess AI will be added.

This Chess game uses long-form algebraic chess notation (So you say e2-e4, instead of e4, or you say Kb1xc3 to
say knight takes on c3). 

Right now, it's missing en-passant and pawn promtion.

The structure of the code is Object Oriented. So each piece is an object and the board is an object that contains all the pices. The board is re-rendered after each move to show all of the pieces which remain.

To show the background of the board, I use the colorama python library, and I use unicode characters to display the pieces.

Before each move, all possible moves are generated and displayed. The game ends if there are no available moves and the king is not in check—stalemate—or if there are no available moves and the king is in check—checkmate.

Gameplay Images:


![Gameplay](https://user-images.githubusercontent.com/51685858/103182577-702adf80-487a-11eb-9c55-b122a9f5b563.png)

![Checkmate](https://user-images.githubusercontent.com/51685858/102663100-24778800-414e-11eb-9d4a-b4aee24581a2.jpg)

