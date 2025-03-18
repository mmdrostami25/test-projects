import tkinter as tk
from tkinter import messagebox
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

        # Handle special moves
        if piece.lower() == '♔' and abs(end_col - start_col) == 2:
            self.handle_castling(start_row, end_col)

        # Update board
        self.board[start_row][start_col] = ' '
        self.board[end_row][end_col] = piece
        self.move_log.append(move)
        self.current_player = 'black' if self.current_player == 'white' else 'white'

    def handle_castling(self, row, end_col):
        if end_col == 6:  # Kingside
            self.board[row][5] = self.board[row][7]
            self.board[row][7] = ' '
        elif end_col == 2:  # Queenside
            self.board[row][3] = self.board[row][0]
            self.board[row][0] = ' '

    def is_valid_move(self, move):
        try:
            start, end = move[:2], move[2:]
            piece = self.get_piece(start)
            target = self.get_piece(end)
            
            if piece == ' ':
                return False
                
            # Check player turn
            if (self.current_player == 'white' and not piece.isupper()) or \
               (self.current_player == 'black' and piece.isupper()):
                return False
                
            # Basic movement rules (ساده شده)
            start_col = ord(start[0]) - ord('a')
            start_row = 8 - int(start[1])
            end_col = ord(end[0]) - ord('a')
            end_row = 8 - int(end[1])
            
            dx = abs(end_col - start_col)
            dy = abs(end_row - start_row)
            
            # Pawn movement
            if piece.lower() == '♟':
                direction = -1 if piece == '♙' else 1
                if start_col == end_col and target == ' ':
                    if (end_row == start_row + direction) or \
                       (start_row in (1,6) and end_row == start_row + 2*direction):
                        return True
                return False
                
            # Add other piece rules here
            
            return True
        except:
            return False

    def save_game(self, filename):
        data = {
            'board': self.board,
            'current_player': self.current_player,
            'move_log': self.move_log,
            'castling_rights': self.castling_rights,
            'en_passant': self.en_passant
        }
        with open(filename, 'w') as f:
            json.dump(data, f)

    def load_game(self, filename):
        with open(filename, 'r') as f:
            data = json.load(f)
        self.board = data['board']
        self.current_player = data['current_player']
        self.move_log = data['move_log']
        self.castling_rights = data['castling_rights']
        self.en_passant = data['en_passant']

class ChessGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("شطرنج پیشرفته")
        self.geometry("640x680")
        self.game = ChessGame()
        self.selected_piece = None
        self.highlights = []
        
        # ایجاد رابط کاربری
        self.canvas = tk.Canvas(self, width=640, height=640, bg='white')
        self.canvas.pack()
        self.status = tk.Label(self, text="نوبت سفید", font=('Arial', 14))
        self.status.pack()
        
        self.create_menu()
        self.draw_board()
        self.canvas.bind("<Button-1>", self.on_click)

    def create_menu(self):
        menubar = tk.Menu(self)
        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="بازی جدید", command=self.new_game)
        file_menu.add_command(label="ذخیره بازی", command=self.save_game)
        file_menu.add_command(label="بارگیری بازی", command=self.load_game)
        menubar.add_cascade(label="فایل", menu=file_menu)
        self.config(menu=menubar)

    def new_game(self):
        self.game.reset_game()
        self.draw_board()
        self.update_status()

    def save_game(self):
        filename = tk.filedialog.asksaveasfilename(defaultextension=".chess")
        if filename:
            self.game.save_game(filename)

    def load_game(self):
        filename = tk.filedialog.askopenfilename(filetypes=[("Chess Files", "*.chess")])
        if filename:
            self.game.load_game(filename)
            self.draw_board()
            self.update_status()

    def draw_board(self):
        self.canvas.delete("all")
        colors = ["#f0d9b5", "#b58863"]
        for row in range(8):
            for col in range(8):
                x1 = col * 80
                y1 = row * 80
                color = colors[(row + col) % 2]
                self.canvas.create_rectangle(x1, y1, x1+80, y1+80, fill=color, outline="")
                piece = self.game.board[row][col]
                if piece != ' ':
                    self.canvas.create_text(x1+40, y1+40, text=piece, font=("Arial", 40))

    def update_status(self):
        player = "سفید" if self.game.current_player == 'white' else "سیاه"
        self.status.config(text=f"نوبت {player}")

    def on_click(self, event):
        col = event.x // 80
        row = event.y // 80
        position = f"{chr(col + 97)}{8 - row}"
        
        if self.selected_piece:
            if self.game.is_valid_move(self.selected_piece + position):
                self.game.make_move(self.selected_piece + position)
                self.draw_board()
                self.update_status()
                self.check_game_over()
            self.selected_piece = None
            self.clear_highlights()
        else:
            piece = self.game.get_piece(position)
            if piece != ' ':
                self.selected_piece = position
                self.highlight_position(position)

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

    def check_game_over(self):
        # TODO: پیاده‌سازی منطق تشخیص کیش و مات
        pass

if __name__ == "__main__":
    app = ChessGUI()
    app.mainloop()