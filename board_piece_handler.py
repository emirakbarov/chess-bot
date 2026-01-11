import numpy as np
import matplotlib.pyplot as plt
import tkinter as tk
from PIL import Image, ImageTk

SQUARE = 60
BOARD_SIZE = 8 * SQUARE
PIECE_SIZE = 60, 60
BACK_RANK = ["R", "N", "B", "Q", "K", "B", "N", "R"]

class Piece: # set up the piece class
    
    def __init__(self, type, colour, possible_moves, icon):
        self.type = type
        self.colour = colour
        self.possible_moves = possible_moves
        self.icon = icon
    

class Square:

    def __init__(self, matrix_pos):
        self.matrix_pos = matrix_pos
        self.state = None
        
    def set_state(self, piece):
        self.state = piece

class Board:
    
    def __init__(self): # init the board and assign each square a value in the matrix#
        self.images = []
        self.first_move = np.random.choice([0,1])
        self.root = tk.Tk()
        self.canvas = tk.Canvas(self.root, width=BOARD_SIZE, height=BOARD_SIZE, highlightthickness=0)
        self.canvas.pack()  

        self.draw_board()
        self.root.resizable(False, False)

        self.root.mainloop()
        
    
                    
    def add_piece(self, piece, r, c):
        img = Image.open(f"./piece_files/{piece.type}-{piece.colour}.png").convert("RGBA")
        img = img.resize(PIECE_SIZE, Image.Resampling.LANCZOS)
        tk_img = ImageTk.PhotoImage(img)

        self.images.append(tk_img)

        x, y = self.square_center(r, c)
        self.canvas.create_image(x, y, image=tk_img, tags=("piece",))



    def square_center(self, row, col):
        x = col * SQUARE + SQUARE // 2
        y = row * SQUARE + SQUARE // 2
        return x, y
    
    def draw_board(self):
        for r in range(8):
            for c in range(8):
                square_colour = "white" if (r + c) % 2 == 0 else "brown"
                x1, y1 = c * SQUARE, r * SQUARE
                x2, y2 = x1 + SQUARE, y1 + SQUARE
                pos = (x1, y1, x2, y2)
                self.canvas.create_rectangle(pos, fill=square_colour, outline="")

                if r in (0, 1, 6, 7):
                    piece_colour = "b" if r in (0, 1) else "w"

                    if r in (1, 6):
                        piece_type = "P"
                    else:
                        piece_type = BACK_RANK[c]

                    piece = Piece(piece_type, piece_colour, None, None)
                    self.add_piece(piece, r, c)


board = Board()