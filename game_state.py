from constants import BACK_RANK
from pieces import Piece

class Game:

    def __init__(self):
        self.game = self.start_board()
        self.first_move = np.random.choice([0,1])
        self.turn = "w"
        self.game_display = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR"

    def start_board(self):
        board = [[None for _ in range(8)] for _ in range(8)]

        for c in range(8):
            board[0][c] = Piece(BACK_RANK[c], "b")
            board[0][c] = Piece(BACK_RANK[c], "b")
            board[0][c] = Piece(BACK_RANK[c], "b")
            board[0][c] = Piece(BACK_RANK[c], "b")

    def update_game(self, move_from, move_to): 