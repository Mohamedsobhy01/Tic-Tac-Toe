import tkinter as tk
import random

class TicTacToe:
    def __init__(self, root):
        self.root = root
        self.root.title("Tic-Tac-Toe")

        self.player_score = 0
        self.computer_score = 0
        self.buttons = [[None for _ in range(3)] for _ in range(3)]

        self.build_ui()

    def build_ui(self):
        self.score_label = tk.Label(self.root, text=self.get_score_text(),
                                    font=("Arial", 14), fg="blue")
        self.score_label.grid(row=0, column=0, columnspan=3, pady=10)

        self.status_label = tk.Label(self.root, text="", font=("Arial", 20, "bold"))
        self.status_label.grid(row=1, column=0, columnspan=3, pady=10)

        start_button = tk.Button(self.root, text="Start New Round", font=("Arial", 13),
                                 command=self.reset_board, bg="#0C83FF", fg="white")
        start_button.grid(row=2, column=0, columnspan=3, pady=10)

        for i in range(3):
            for j in range(3):
                btn = tk.Button(
                    self.root, text="", width=8, height=3,
                    font=("Arial", 25, "bold"),
                    bg="white",
                    command=lambda i=i, j=j: self.on_click(i, j)
                )
                btn.grid(row=i+3, column=j, padx=5, pady=5)
                self.buttons[i][j] = btn

    def on_click(self, i, j):
        if self.buttons[i][j]["text"] != "":
            return

        self.buttons[i][j]["text"] = "X"
        winner = self.check_winner()

        if winner:
            self.finish_round(winner)
            return

        self.computer_play()
        winner = self.check_winner()
        if winner:
            self.finish_round(winner)

    def computer_play(self):
        move = self.find_best_move()
        if move:
            i, j = move
        else:
            empty_cells = [(i, j) for i in range(3) for j in range(3)
                           if self.buttons[i][j]["text"] == ""]
            if not empty_cells:
                return
            i, j = random.choice(empty_cells)

        self.buttons[i][j]["text"] = "O"
        self.buttons[i][j]["bg"] = "#F6C6C6"

    def find_best_move(self):
        for i in range(3):
            for j in range(3):
                if self.buttons[i][j]["text"] == "":
                    self.buttons[i][j]["text"] = "X"
                    if self.check_winner() == "X":
                        self.buttons[i][j]["text"] = ""
                        return (i, j)
                    self.buttons[i][j]["text"] = ""
        return None

    def check_winner(self):
        b = self.buttons

        for i in range(3):
            if b[i][0]["text"] == b[i][1]["text"] == b[i][2]["text"] != "":
                self.highlight((i,0), (i,1), (i,2))
                return b[i][0]["text"]

            if b[0][i]["text"] == b[1][i]["text"] == b[2][i]["text"] != "":
                self.highlight((0,i), (1,i), (2,i))
                return b[0][i]["text"]

        if b[0][0]["text"] == b[1][1]["text"] == b[2][2]["text"] != "":
            self.highlight((0,0),(1,1),(2,2))
            return b[0][0]["text"]

        if b[0][2]["text"] == b[1][1]["text"] == b[2][0]["text"] != "":
            self.highlight((0,2),(1,1),(2,0))
            return b[0][2]["text"]

        for row in b:
            for btn in row:
                if btn["text"] == "":
                    return None

        return "Draw"

    def finish_round(self, winner):
        if winner == "Draw":
            self.status_label.config(text="Tie! Nobody wins", fg="black")
        else:
            self.status_label.config(text=f"{winner} Wins!", fg="green")
            self.update_score(winner)

        self.disable_buttons()

    def disable_buttons(self):
        for row in self.buttons:
            for btn in row:
                btn.config(state="disabled")

    def enable_buttons(self):
        for row in self.buttons:
            for btn in row:
                btn.config(state="normal", bg="white")

    def reset_board(self):
        self.status_label.config(text="")
        self.enable_buttons()

        for i in range(3):
            for j in range(3):
                self.buttons[i][j]["text"] = ""
                self.buttons[i][j]["bg"] = "white"

    def highlight(self, *cells):
        for i, j in cells:
            self.buttons[i][j].config(bg="#90EE90")

    def update_score(self, winner):
        if winner == "X":
            self.player_score += 1
        elif winner == "O":
            self.computer_score += 1

        self.score_label.config(text=self.get_score_text())

    def get_score_text(self):
        return f"You: {self.player_score}    Computer: {self.computer_score}"


root = tk.Tk()
game = TicTacToe(root)
root.mainloop()
