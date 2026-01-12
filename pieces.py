class Piece: # set up the piece class
    
    #knight_moves = [2, 1], [-2, 1], [2, -1], [-2, -1], [1, 2], [-1, 2], [-1,-2], [1, -2]
    #pawn_moves = [0, 1], [0, 2], [1, 1], [-1, 1]
    #king_moves = [1,1], [1,-1], [-1,-1], [-1, 1], [0, 1], [0, -1], [1, 0], [-1, 0]

    #def rook_moves():

    def __init__(self, type, colour, possible_moves, icon):
        self.type = type
        self.colour = colour
        self.possible_moves = possible_moves


class Square:

    def __init__(self, matrix_pos):
        self.matrix_pos = matrix_pos
        self.state = None
        
    def set_state(self, piece):
        self.state = piece