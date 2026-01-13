from constants import BACK_RANK, STATIC_MOVES
from pieces import Piece
from numpy import random as np
import copy

class Game:

    def __init__(self):
        self.first_move = np.choice([0,1])
        self.turn = "w"
        self.game_starting_position = ("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR")
        self.board = self.start_board()
        print(self.board)

    def start_board(self):
        return self.decode_fen(self.game_starting_position)

    def update_board_state(self, from_rc, to_rc):
        r_prev, c_prev = from_rc
        r_new, c_new = to_rc
        previous_occupant = self.board[r_prev][c_prev]
        self.board[r_prev][c_prev] = None
        self.board[r_new][c_new] = previous_occupant 
        print(self.board)
        

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
        r_prev, c_prev = from_rc
        r_new, c_new = to_rc
        translation_r, translation_c = r_new - r_prev, c_new - c_prev
        #previous_occupant = self.board[r_prev][c_prev]
        #temporary_board = temporary_board = copy.deepcopy(self.board)
        #temporary_board[r_prev][c_prev] = None
        #temporary_board[r_new][c_new] = previous_occupant 
        if piece.type == "N":
            return [translation_r, translation_c] in (STATIC_MOVES[piece.type])
        else:
            return True

