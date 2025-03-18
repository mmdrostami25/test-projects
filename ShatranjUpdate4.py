import tkinter as tk
from tkinter import messagebox
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
        self.scores = {'white': 0, 'black': 0}

    def get_piece(self, position):
        try:
            col = ord(position[0].lower()) - ord('a')
            row = 8 - int(position[1])
            return self.board[row][col]
        except:
            return ' '

    def is_valid_move(self, move):
        start, end = move[:2], move[2:]
        start_col = ord(start[0].lower()) - ord('a')
        start_row = 8 - int(start[1])
        end_col = ord(end[0].lower()) - ord('a')
        end_row = 8 - int(end[1])
        
        if start_row < 0 or start_row > 7 or end_row < 0 or end_row > 7:
            return False
        if start_col < 0 or start_col > 7 or end_col < 0 or end_col > 7:
            return False
            
        piece = self.board[start_row][start_col]
        target = self.board[end_row][end_col]
        
        if piece == ' ':
            return False
            
        if (self.current_player == 'white' and piece.islower()) or \
           (self.current_player == 'black' and piece.isupper()):
            return False
            
        # حرکت پیاده
        if piece.lower() == '♟':
            return self.validate_pawn_move(start_row, start_col, end_row, end_col, piece)
            
        return True

    def validate_pawn_move(self, start_row, start_col, end_row, end_col, piece):
        direction = -1 if piece == '♙' else 1
        start_pos = (start_row, start_col)
        end_pos = (end_row, end_col)
        
        # حرکت مستقیم
        if start_col == end_col:
            if self.board[end_row][end_col] != ' ':
                return False
                
            if end_row == start_row + direction:
                return True
                
            if (piece == '♙' and start_row == 6) or (piece == '♟' and start_row == 1):
                if end_row == start_row + 2*direction:
                    if self.board[start_row + direction][start_col] == ' ':
                        return True
                        
        # حرکت ضربدری
        elif abs(start_col - end_col) == 1 and end_row == start_row + direction:
            if self.board[end_row][end_col] != ' ':
                return True
                
        return False

    def make_move(self, move):
        if self.game_over:
            return
            
        start, end = move[:2], move[2:]
        start_col = ord(start[0].lower()) - ord('a')
        start_row = 8 - int(start[1])
        end_col = ord(end[0].lower()) - ord('a')
        end_row = 8 - int(end[1])
        
        piece = self.board[start_row][start_col]
        self.board[start_row][start_col] = ' '
        self.board[end_row][end_col] = piece
        
        self.current_player = 'black' if self.current_player == 'white' else 'white'
        self.move_log.append(move)

class ChessGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("بازی شطرنج")
        self.geometry("640x720")
        self.game = ChessGame()
        self.selected_piece = None
        self.highlights = []
        
        self.colors = ["#f0d9b5", "#b58863"]
        self.highlight_color = "#4682b4"
        
        self.create_menu()
        self.create_widgets()
        self.update_display()

    def create_menu(self):
        menubar = tk.Menu(self)
        
        game_menu = tk.Menu(menubar, tearoff=0)
        game_menu.add_command(label="بازی جدید", command=self.new_game)
        game_menu.add_command(label="شروع مجدد", command=self.restart_game)
        game_menu.add_separator()
        game_menu.add_command(label="خروج", command=self.quit)
        menubar.add_cascade(label="بازی", menu=game_menu)

        info_menu = tk.Menu(menubar, tearoff=0)
        info_menu.add_command(label="امتیازات", command=self.show_scores)
        info_menu.add_command(label="راهنما", command=self.show_help)
        menubar.add_cascade(label="اطلاعات", menu=info_menu)

        self.config(menu=menubar)

    def create_widgets(self):
        self.canvas = tk.Canvas(self, width=640, height=640)
        self.canvas.pack()
        
        self.status_frame = tk.Frame(self, height=80)
        self.status_frame.pack(fill=tk.X)
        
        self.status_label = tk.Label(self.status_frame, 
                                   text="نوبت بازیکن سفید",
                                   font=('Tahoma', 14))
        self.status_label.pack(side=tk.LEFT, padx=20)
        
        self.score_label = tk.Label(self.status_frame,
                                  text="امتیازات: سفید 0 - سیاه 0",
                                  font=('Tahoma', 12))
        self.score_label.pack(side=tk.RIGHT, padx=20)

        self.canvas.bind("<Button-1>", self.handle_click)

    def handle_click(self, event):
        col = event.x // 80
        row = event.y // 80
        position = f"{chr(col + 97)}{8 - row}"
        
        if self.selected_piece:
            move = self.selected_piece + position
            if self.game.is_valid_move(move):
                self.game.make_move(move)
                self.update_display()
            self.selected_piece = None
            self.clear_highlights()
        else:
            piece = self.game.get_piece(position)
            if piece != ' ':
                self.selected_piece = position
                self.highlight_position(position)

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
        text_color = "white" if piece in {'♖','♘','♗','♕','♔','♙'} else "black"
        self.canvas.create_text(
            x + 40, y + 40,
            text=piece,
            font=("Segoe UI Symbol", 40, "bold"),
            fill=text_color
        )

    def highlight_position(self, position):
        self.clear_highlights()
        col = ord(position[0].lower()) - ord('a')
        row = 8 - int(position[1])
        x = col * 80 + 40
        y = row * 80 + 40
        self.highlights.append(
            self.canvas.create_oval(x-30, y-30, x+30, y+30, 
                                  outline=self.highlight_color, width=3)
        )

    def clear_highlights(self):
        for item in self.highlights:
            self.canvas.delete(item)
        self.highlights = []

    def update_display(self):
        self.draw_board()
        self.update_status()

    def update_status(self):
        player = "سفید" if self.game.current_player == 'white' else "سیاه"
        self.status_label.config(text=f"نوبت بازیکن {player}")
        self.score_label.config(
            text=f"امتیازات: سفید {self.game.scores['white']} - سیاه {self.game.scores['black']}"
        )

    def new_game(self):
        self.game = ChessGame()
        self.update_display()

    def restart_game(self):
        self.game.reset_game()
        self.update_display()

    def show_scores(self):
        messagebox.showinfo(
            "امتیازات",
            f"امتیاز بازیکن سفید: {self.game.scores['white']}\n"
            f"امتیاز بازیکن سیاه: {self.game.scores['black']}"
        )

    def show_help(self):
        help_text = """
        راهنمای بازی:
        1. روی مهره خود کلیک کنید
        2. روی خانه مقصد کلیک کنید
        3. پیاده‌ها می‌توانند:
           - یک خانه به جلو حرکت کنند
           - در حرکت اول دو خانه بروند
           - به صورت مورب مهره حریف را بزنند
        """
        messagebox.showinfo("راهنما", help_text)

if __name__ == "__main__":
    app = ChessGUI()
    app.mainloop()
    
"""
    
"""