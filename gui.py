import numpy as np
import tkinter as tk
from PIL import Image, ImageTk

from constants import SQUARE, BOARD_SIZE, PIECE_SIZE, BACK_RANK
from pieces import Piece
from game_state import Game

class Board:
    
    def __init__(self):

        # Piece data
        self.images = []
        self.item_to_piece = {}
        self.item_to_pos = {}
        self.game = Game() # nitialisae the new game 
        self.game.start_board()

        # Drag state 
        self.drag_item = None
        self.drag_x = 0
        self.drag_y = 0
        self.drag_start_rc = None

        # Generate GUI 
        self.root = tk.Tk()
        self.canvas = tk.Canvas(self.root, width=BOARD_SIZE, height=BOARD_SIZE, highlightthickness=0)
        self.canvas.pack()  
        self.draw_board()
        self.root.resizable(False, False)

        # Binding for drag
        self.canvas.tag_bind("piece", "<ButtonPress-1>", self.on_drag_start)
        self.canvas.tag_bind("piece", "<B1-Motion>", self.on_drag_motion)
        self.canvas.tag_bind("piece", "<ButtonRelease-1>", self.on_drag_release)

    # Draw board 
    def run(self):
        self.root.mainloop()
    
                    
    def add_piece(self, piece, r, c):
        # Open piece icons
        img = Image.open(f"./piece_files/{piece.type}-{piece.colour}.png").convert("RGBA")
        img = img.resize(PIECE_SIZE, Image.Resampling.LANCZOS)
        tk_img = ImageTk.PhotoImage(img)
        self.images.append(tk_img)

        # Create and centre piece on square 
        x, y = self.square_center(r, c)
        item_id = self.canvas.create_image(x, y, image=tk_img, tags=("piece",))

        # Append to piece data
        self.item_to_piece[item_id] = piece
        self.item_to_pos[item_id] = (r, c)

    # Drawing function      
    def draw_board(self):
        for r in range(8):
            for c in range(8):
                # Set square colour and positions
                square_colour = "white" if (r + c) % 2 == 0 else "brown"
                x1, y1 = c * SQUARE, r * SQUARE
                x2, y2 = x1 + SQUARE, y1 + SQUARE
                pos = (x1, y1, x2, y2)
                self.canvas.create_rectangle(pos, fill=square_colour, outline="")
                # place pieces on board
                if r in (0, 1, 6, 7):
                    piece_colour = "b" if r in (0, 1) else "w"

                    if r in (1, 6):
                        piece_type = "P"
                    else:
                        piece_type = BACK_RANK[c]

                    piece = Piece(piece_type, piece_colour, None, None)
                    self.add_piece(piece, r, c)
        #self.game.upddate

    # Center piece on square 
    def square_center(self, row, col):
        x = col * SQUARE + SQUARE // 2
        y = row * SQUARE + SQUARE // 2
        return x, y
    
    # Convert coordinates to squares for drag
    def xy_to_rc(self, x, y):
        c = x // SQUARE
        r = y // SQUARE
        return int(r), int(c)

    # Onclick
    def on_drag_start(self, event):
        item = self.canvas.find_withtag("current")
        if not item: return
        self.drag_item = item[0]
        self.canvas.tag_raise(self.drag_item)
        self.root.config(cursor="hand2")
        self.drag_x = event.x
        self.drag_y = event.y

    # When piece is being dragged
    def on_drag_motion(self, event):
        dx = event.x - self.drag_x
        dy = event.y - self.drag_y
        self.canvas.move(self.drag_item, dx, dy)
        self.drag_x = event.x
        self.drag_y = event.y
        if not (0 <= dx // SQUARE < 8 and 0 <= dy // SQUARE < 8) :
            return None

    # When piece is releaed 
    def on_drag_release(self, event):
        self.root.config(cursor="arrow")
        r, c = self.xy_to_rc(event.x, event.y)

        from_rc = self.item_to_pos[self.drag_item]
        to_rc = (r, c)

        if self.game.make_move(from_rc, to_rc):

            for item, pos in list(self.item_to_pos.items()):
                if pos == to_rc and item != self.drag_item:
                    self.canvas.delete(item)
                    del self.item_to_pos[item]
                    del self.item_to_piece[item]
                    break

            self.canvas.coords(self.drag_item, self.square_center(r, c))
            self.item_to_pos[self.drag_item] = to_rc
            self.canvas.tag_raise("piece")
        else:
            x, y = self.square_center(*from_rc)
            self.canvas.coords(self.drag_item, x, y)
            print("illegal move")
