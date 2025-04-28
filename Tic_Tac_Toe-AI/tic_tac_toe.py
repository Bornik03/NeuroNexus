import tkinter as tk
import math

class TicTacToe:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Tic-Tac-Toe AI")

        self.board = [' ' for _ in range(9)]
        self.buttons = []

        self.create_buttons()
        self.window.mainloop()

    def create_buttons(self):
        for i in range(9):
            button = tk.Button(self.window, text=' ', font=('Arial', 40), width=5, height=2,
                               command=lambda i=i: self.human_move(i))
            button.grid(row=i//3, column=i%3)
            self.buttons.append(button)

    def human_move(self, index):
        if self.board[index] == ' ':
            self.board[index] = 'X'
            self.buttons[index].config(text='X')
            if self.check_game_over('X'):
                return
            self.window.after(0, self.ai_move)

    def ai_move(self):
        move = self.minimax('O', -math.inf, math.inf)['position']
        if move is not None:
            self.board[move] = 'O'
            self.buttons[move].config(text='O')
            self.check_game_over('O')

    def available_moves(self):
        return [i for i, spot in enumerate(self.board) if spot == ' ']

    def winner(self, player):
        win_combinations = [
            [0,1,2], [3,4,5], [6,7,8],
            [0,3,6], [1,4,7], [2,5,8],
            [0,4,8], [2,4,6]
        ]
        return any(all(self.board[i] == player for i in combo) for combo in win_combinations)

    def is_draw(self):
        return ' ' not in self.board

    def check_game_over(self, player):
        if self.winner(player):
            self.show_result(f"{player} wins!")
            return True
        elif self.is_draw():
            self.show_result("It's a draw!")
            return True
        return False

    def show_result(self, message):
        result = tk.Label(self.window, text=message, font=('Arial', 24))
        result.grid(row=3, column=0, columnspan=3)
        for button in self.buttons:
            button.config(state="disabled")

    def minimax(self, player, alpha, beta):
        max_player = 'O'
        other_player = 'X' if player == 'O' else 'O'

        if self.winner(other_player):
            return {'position': None, 'score': 1 * (len(self.available_moves()) + 1) if other_player == max_player else -1 * (len(self.available_moves()) + 1)}
        elif self.is_draw():
            return {'position': None, 'score': 0}

        if player == max_player:
            best = {'position': None, 'score': -math.inf}
        else:
            best = {'position': None, 'score': math.inf}

        for possible_move in self.available_moves():
            self.board[possible_move] = player
            sim_score = self.minimax(other_player, alpha, beta)
            self.board[possible_move] = ' '
            sim_score['position'] = possible_move

            if player == max_player:
                if sim_score['score'] > best['score']:
                    best = sim_score
                alpha = max(alpha, sim_score['score'])
            else:
                if sim_score['score'] < best['score']:
                    best = sim_score
                beta = min(beta, sim_score['score'])

            if beta <= alpha:
                break

        return best

if __name__ == "__main__":
    TicTacToe()
