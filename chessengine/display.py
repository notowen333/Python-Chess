"""
Reusable chess board display module.
Provides colored terminal output with Unicode chess pieces.
"""

# ANSI escape codes for colors
class Colors:
    # Background colors - green/cream like a real chess board
    LIGHT_SQ = '\033[48;5;222m'  # Light tan/cream
    DARK_SQ = '\033[48;5;94m'    # Brown/dark green
    # Foreground colors for pieces
    WHITE_PIECE = '\033[38;5;255m'  # Bright white
    BLACK_PIECE = '\033[38;5;0m'    # Black
    RESET = '\033[0m'
    BOLD = '\033[1m'

# Unicode chess pieces
PIECES = {
    'K': '♔', 'Q': '♕', 'R': '♖', 'B': '♗', 'N': '♘', 'P': '♙',
    'k': '♚', 'q': '♛', 'r': '♜', 'b': '♝', 'n': '♞', 'p': '♟',
    '.': ' ', None: ' ', '': ' '
}


def get_piece_symbol(piece):
    """Convert a piece to its Unicode symbol."""
    if piece is None or piece == '.' or piece == '':
        return ' ', None
    # If it's already a unicode piece, return it
    if piece in '♔♕♖♗♘♙':
        return piece, True  # white piece
    if piece in '♚♛♜♝♞♟':
        return piece, False  # black piece
    # If it's a piece object with __str__, use that
    if hasattr(piece, '__str__') and not isinstance(piece, str):
        symbol = str(piece)
        # Determine color from the piece object if possible
        is_white = getattr(piece, 'color', None)
        return symbol, is_white
    # Otherwise look up in our dict
    symbol = PIECES.get(piece, str(piece))
    is_white = piece.isupper() if isinstance(piece, str) and piece.isalpha() else None
    return symbol, is_white


def render_board(board, flipped=False):
    """
    Render a chess board to a string with colors.

    Args:
        board: Either an 8x8 2D list of pieces, or an object with a .board attribute
        flipped: If True, show from black's perspective

    Returns:
        String representation of the board
    """
    # Handle board objects that have a .board attribute
    if hasattr(board, 'board'):
        board_data = board.board
    else:
        board_data = board

    lines = []

    # Column headers
    if flipped:
        lines.append('     h   g   f   e   d   c   b   a')
    else:
        lines.append('     a   b   c   d   e   f   g   h')

    # Rows
    row_range = range(8) if flipped else range(7, -1, -1)

    for row in row_range:
        row_num = row + 1
        row_str = f' {row_num} '

        col_range = range(7, -1, -1) if flipped else range(8)

        for col in col_range:
            piece = board_data[row][col]
            symbol, is_white = get_piece_symbol(piece)

            # Alternate square colors (light/dark like a real board)
            if (row + col) % 2 == 1:
                bg = Colors.LIGHT_SQ
            else:
                bg = Colors.DARK_SQ

            # Set piece color for contrast
            if is_white is True:
                fg = Colors.WHITE_PIECE + Colors.BOLD
            elif is_white is False:
                fg = Colors.BLACK_PIECE
            else:
                fg = ''

            row_str += f'{bg}{fg} {symbol} {Colors.RESET}'

        row_str += f' {row_num}'
        lines.append(row_str)

    # Column headers again
    if flipped:
        lines.append('     h   g   f   e   d   c   b   a')
    else:
        lines.append('     a   b   c   d   e   f   g   h')

    return '\n'.join(lines)


def print_board(board, flipped=False):
    """Print the chess board with colors."""
    print(render_board(board, flipped))


def render_board_simple(board):
    """
    Render a simple ASCII board without colors (for environments without colorama).

    Args:
        board: Either an 8x8 2D list of pieces, or an object with a .board attribute

    Returns:
        String representation of the board
    """
    if hasattr(board, 'board'):
        board_data = board.board
    else:
        board_data = board

    lines = []
    lines.append('    a   b   c   d   e   f   g   h')
    lines.append('  +---+---+---+---+---+---+---+---+')

    for row in range(7, -1, -1):
        row_num = row + 1
        row_str = f'{row_num} |'

        for col in range(8):
            piece = board_data[row][col]
            symbol, _ = get_piece_symbol(piece)
            row_str += f' {symbol} |'

        row_str += f' {row_num}'
        lines.append(row_str)
        lines.append('  +---+---+---+---+---+---+---+---+')

    lines.append('    a   b   c   d   e   f   g   h')

    return '\n'.join(lines)


def piece_to_symbol(piece):
    """Get just the symbol for a piece (convenience function)."""
    symbol, _ = get_piece_symbol(piece)
    return symbol


def print_board_simple(board):
    """Print a simple ASCII board without colors."""
    print(render_board_simple(board))
