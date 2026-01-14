from constants import BACK_RANK, STATIC_MOVES
from pieces import Piece
from numpy import random as np
import copy

class Game:

    def __init__(self):
        self.first_move = np.choice([0,1])
        self.turn = "w"

        self.pieces_captured_by = { 
            "w": [],
            "b": []
        }

        self.game_starting_position = ("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR")
        self.board = self.start_board()

    def start_board(self):
        return self.decode_fen(self.game_starting_position)

    def update_board_state(self, from_rc, to_rc):
        if self.turn == "b":
            self.turn = "w" 
        elif self.turn == "w":
            self.turn = "b"
        r_prev, c_prev = from_rc
        r_new, c_new = to_rc
        previous_occupant = self.board[r_prev][c_prev]
        self.board[r_prev][c_prev] = None
        self.board[r_new][c_new] = previous_occupant


    def decode_fen(self, fen_string):

        output = [[None for _ in range(8)] for _ in range(8)]
        row = 0
        col = 0

        for square_value in fen_string:
            if square_value == '/':
                row += 1
                col = 0
            elif square_value.isdigit():
                col += int(square_value)
            else:
                if square_value.isupper():
                    output[row][col] = Piece(square_value, "W", None, None)
                else:
                    output[row][col] = Piece(square_value.upper(), "B", None, None)
                
                col += 1
        return output
    
    def check_legal_move(self, from_rc, to_rc, piece):
        if piece.colour != self.turn: return False

        r_prev, c_prev = from_rc
        r_new, c_new = to_rc
        translation_r, translation_c = r_new - r_prev, c_new - c_prev

        target = self.board[r_new][c_new]
        
        if (target):
            if (target.colour == piece.colour):
                return False
            else: self.capture_piece(target, piece)
        
        if piece.type == "N":
            return [translation_r, translation_c] in (STATIC_MOVES[piece.type])
        elif piece.type == "P":
            direction = -1 if piece.colour == "w" else 1
            start_row = 6 if piece.colour == "w" else 1

            if translation_c == 0 and translation_r == direction:
                return self.board[r_new][c_new] is None

            if translation_c == 0 and translation_r == 2 * direction and r_prev == start_row:
                if self.board[r_prev + direction][c_prev] is None and self.board[r_new][c_new] is None:
                    return True

            return False

        # Direction
        dir_r = 0 if translation_r == 0 else (1 if translation_r > 0 else -1)
        dir_c = 0 if translation_c == 0 else (1 if translation_c > 0 else -1)


        if piece.type == "R": 
            if dir_c != 0 and dir_r != 0: return False

        if piece.type == "B": 
            if abs(translation_r) != abs(translation_c): return False
            
        r, c = r_prev + dir_r, c_prev + dir_c

        while (r, c) != (r_new, c_new):
            if self.board[r][c] is not None: return False
            r += dir_r
            c += dir_c

        return True
    
    def capture_piece(self, target, piece):
        capturing_colour = piece.colour
        self.pieces_captured_by[capturing_colour].append(target)
