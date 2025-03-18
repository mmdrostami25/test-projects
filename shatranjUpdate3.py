import tkinter as tk
from tkinter import messagebox, filedialog
import json
from copy import deepcopy

class ChessGame:
    def __init__(self):
        self.reset_game()
        
    def reset_game(self):
        self.board = [
            ['♜', '♞', '♝', '♛', '♚', '♝', '♞', '♜'],
            ['♟', '♟', '♟', '♟', '♟', '♟', '♟', '♟'],
            [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
            [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
            [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
            [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
            ['♙', '♙', '♙', '♙', '♙', '♙', '♙', '♙'],
            ['♖', '♘', '♗', '♕', '♔', '♗', '♘', '♖']
        ]
        self.current_player = 'white'
        self.game_over = False
        self.move_log = []
        self.castling_rights = {'white': {'k': True, 'q': True},
                                'black': {'k': True, 'q': True}}
        self.en_passant = None
        self.check = False

    def get_piece(self, position):
        col = ord(position[0]) - ord('a')
        row = 8 - int(position[1])
        return self.board[row][col]

    def make_move(self, move):
        start, end = move[:2], move[2:]
        start_col = ord(start[0]) - ord('a')
        start_row = 8 - int(start[1])
        end_col = ord(end[0]) - ord('a')
        end_row = 8 - int(end[1])
        piece = self.board[start_row][start_col]

        # Handle castling
        if piece.lower() == '♔' and abs(end_col - start_col) == 2:
            self.handle_castling(start_row, end_col)

        # Update board
        self.board[start_row][start_col] = ' '
        self.board[end_row][end_col] = piece
        self.move_log.append(move)
        self.current_player = 'black' if self.current_player == 'white' else 'white'
        self.check = self.in_check()

    def is_valid_move(self, move):
        # Implement basic validation
        return True

    def in_check(self):
        # Basic check detection
        return False

class ChessGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Chess Game")
        self.geometry("640x680")
        self.game = ChessGame()
        self.selected_piece = None
        self.highlights = []
        
        self.colors = ["#f0d9b5", "#b58863"]
        self.piece_colors = {
            'white': {'♖', '♘', '♗', '♕', '♔', '♙'},
            'black': {'♜', '♞', '♝', '♛', '♚', '♟'}
        }
        
        self.canvas = tk.Canvas(self, width=640, height=640)
        self.canvas.pack()
        self.status = tk.Label(self, text="White's Turn", font=('Arial', 14))
        self.status.pack()
        
        self.draw_board()
        self.canvas.bind("<Button-1>", self.on_click)

    def draw_board(self):
        self.canvas.delete("all")
        for row in range(8):
            for col in range(8):
                x1 = col * 80
                y1 = row * 80
                color = self.colors[(row + col) % 2]
                self.canvas.create_rectangle(x1, y1, x1+80, y1+80, fill=color)
                piece = self.game.board[row][col]
                if piece != ' ':
                    self.draw_piece(x1, y1, piece)

    def draw_piece(self, x, y, piece):
        text_color = 'white' if piece in self.piece_colors['white'] else 'black'
        self.canvas.create_text(
            x + 40, y + 40,
            text=piece,
            font=("Segoe UI Symbol", 40, "bold"),
            fill=text_color
        )

    def on_click(self, event):
        col = event.x // 80
        row = event.y // 80
        position = f"{chr(col + 97)}{8 - row}"
        
        if self.selected_piece:
            if self.game.is_valid_move(self.selected_piece + position):
                self.game.make_move(self.selected_piece + position)
                self.update_display()
            self.selected_piece = None
            self.clear_highlights()
        else:
            piece = self.game.get_piece(position)
            if piece != ' ':
                self.selected_piece = position
                self.highlight_position(position)

    def update_display(self):
        self.draw_board()
        self.status.config(text=f"{self.game.current_player.capitalize()}'s Turn")
        if self.game.check:
            messagebox.showinfo("Check!", "You're in check!")

    def highlight_position(self, position):
        self.clear_highlights()
        col = ord(position[0]) - ord('a')
        row = 8 - int(position[1])
        x = col * 80 + 40
        y = row * 80 + 40
        self.highlights.append(self.canvas.create_oval(x-15, y-15, x+15, y+15, outline="blue", width=3))

    def clear_highlights(self):
        for item in self.highlights:
            self.canvas.delete(item)
        self.highlights = []

if __name__ == "__main__":
    app = ChessGUI()
    app.mainloop()