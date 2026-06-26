import tkinter as tk
from tkinter import messagebox
import datetime

from algorithms import Minimax, alpha_beta, expectimax

EMPTY = Minimax.EMPTY
HUMAN = Minimax.X
AI = Minimax.O


class TicTacToeUI:
    def __init__(self, master):
        self.master = master
        master.title('Cờ caro 3x3 - Tic Tac Toe')
        master.geometry('900x500')

        self.algorithm_var = tk.StringVar(value='minimax')
        self.board = [[EMPTY for _ in range(3)] for _ in range(3)]
        self.buttons = [[None for _ in range(3)] for _ in range(3)]
        self.game_started = False
        self.move_count = 0

        # Tạo frame chính chứa bàn cờ và điều khiển
        main_frame = tk.Frame(master)
        main_frame.grid(row=0, column=0, padx=10, pady=10)

        # Tạo bàn cờ
        for i in range(3):
            for j in range(3):
                b = tk.Button(main_frame, text=' ', font=('Arial', 32), width=4, height=2,
                              command=lambda r=i, c=j: self.on_click(r, c))
                b.grid(row=i, column=j)
                self.buttons[i][j] = b

        # Nút Restart
        self.restart_btn = tk.Button(main_frame, text='Restart', command=self.restart)
        self.restart_btn.grid(row=3, column=0, columnspan=3, sticky='we')

        # Frame cho thuật toán và log (bên phải)
        right_frame = tk.Frame(master)
        right_frame.grid(row=0, column=1, padx=10, pady=10, sticky='n')

        # Chọn thuật toán
        algo_label = tk.Label(right_frame, text='Chọn thuật toán:', font=('Arial', 10, 'bold'))
        algo_label.pack(anchor='w', pady=(0, 5))
        
        self.radio_buttons = []
        rb1 = tk.Radiobutton(right_frame, text='Minimax', variable=self.algorithm_var,
                             value='minimax')
        rb1.pack(anchor='w')
        self.radio_buttons.append(rb1)
        rb2 = tk.Radiobutton(right_frame, text='Alpha-Beta', variable=self.algorithm_var,
                             value='alpha_beta')
        rb2.pack(anchor='w')
        self.radio_buttons.append(rb2)
        rb3 = tk.Radiobutton(right_frame, text='Expectimax', variable=self.algorithm_var,
                             value='expectimax')
        rb3.pack(anchor='w')
        self.radio_buttons.append(rb3)

        # Log
        log_label = tk.Label(right_frame, text='Lịch sử nước đi:', font=('Arial', 10, 'bold'))
        log_label.pack(anchor='w', pady=(15, 5))
        
        self.log_text = tk.Text(right_frame, width=45, height=20, font=('Courier', 9))
        self.log_text.pack(anchor='w', fill=tk.BOTH, expand=True)
        self.log_text.config(state='disabled')

    def on_click(self, i, j):
        if self.board[i][j] != EMPTY:
            return
        self.game_started = True
        self.disable_algorithm_selection()
        self.make_move(i, j, HUMAN)
        if self.check_end():
            return
        self.master.after(150, self.ai_move)

    def make_move(self, i, j, player):
        self.board[i][j] = player
        btn = self.buttons[i][j]
        btn.config(text=player, state='disabled')
        self.move_count += 1
        
        # Log the move
        if player == HUMAN:
            self.add_log(f"Nước {self.move_count}: Người chơi (X) chọn ({i}, {j})")
        else:
            algo_name = self._get_algorithm_name()
            self.add_log(f"Nước {self.move_count}: Agent ({algo_name}) chọn ({i}, {j})")

    def _get_algorithm_name(self):
        algo = self.algorithm_var.get()
        if algo == 'alpha_beta':
            return 'Alpha-Beta'
        elif algo == 'expectimax':
            return 'Expectimax'
        else:
            return 'Minimax'

    def add_log(self, message):
        self.log_text.config(state='normal')
        self.log_text.insert(tk.END, message + '\n')
        self.log_text.see(tk.END)
        self.log_text.config(state='disabled')

    def ai_move(self):
        algo = self.algorithm_var.get()
        if algo == 'alpha_beta':
            move = alpha_beta.get_best_move(self.board, AI)
        elif algo == 'expectimax':
            move = expectimax.get_best_move(self.board, AI)
        else:
            move = Minimax.get_best_move(self.board, AI)
        if move is None:
            return
        i, j = move
        self.make_move(i, j, AI)
        self.check_end()

    def check_end(self):
        if Minimax.is_winner(self.board, HUMAN):
            self.add_log('--- KẾT QUẢ: Người chơi thắng! ---')
            self.disable_all()
            return True
        if Minimax.is_winner(self.board, AI):
            self.add_log('--- KẾT QUẢ: Agent thắng! ---')
            self.disable_all()
            return True
        if Minimax.is_full(self.board):
            self.add_log('--- KẾT QUẢ: Hòa! ---')
            self.disable_all()
            return True
        return False

    def disable_all(self):
        for i in range(3):
            for j in range(3):
                self.buttons[i][j].config(state='disabled')

    def disable_algorithm_selection(self):
        for rb in self.radio_buttons:
            rb.config(state='disabled')

    def enable_algorithm_selection(self):
        for rb in self.radio_buttons:
            rb.config(state='normal')

    def reset_board(self):
        self.board = [[EMPTY for _ in range(3)] for _ in range(3)]
        for i in range(3):
            for j in range(3):
                b = self.buttons[i][j]
                b.config(text=' ', state='normal')
        self.game_started = False
        self.move_count = 0
        self.enable_algorithm_selection()
        
        # Clear log
        self.log_text.config(state='normal')
        self.log_text.delete(1.0, tk.END)
        self.log_text.config(state='disabled')

    def restart(self):
        self.reset_board()


if __name__ == '__main__':
    root = tk.Tk()
    app = TicTacToeUI(root)
    root.mainloop()
