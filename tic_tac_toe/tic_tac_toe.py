import tkinter as tk

from tkinter import simpledialog


import math
import random

def create_board():
    return [[" " for _ in range(3)] for _ in range(3)]

def is_winner(board, player):
    for row in board:
        if all(cell == player for cell in row):
            return True

    for col in range(3):
        if all(board[row][col] == player for row in range(3)):
            return True

    if all(board[i][i] == player for i in range(3)):
        return True

    if all(board[i][2 - i] == player for i in range(3)):
        return True
    return False
def is_draw(board):
    return all(board[i][j] != " " for i in range(3) for j in range(3))

def evaluate(board):
    if is_winner(board, "X"):
        return 1
    elif is_winner(board, "O"):
        return -1
    else:
        return 0

def minimax(board, depth, maximizing_player, alpha, beta):
    if depth == 0 or is_winner(board, "X") or is_winner(board, "O") or is_draw(board):
        return evaluate(board)

    if maximizing_player:
        max_eval = -math.inf
        for i in range(3):
            for j in range(3):
                if board[i][j] == " ":
                    board[i][j] = "X"
                    eval = minimax(board, depth - 1, False, alpha, beta)
                    board[i][j] = " "
                    max_eval = max(max_eval, eval)
                    alpha = max(alpha, eval)
                    if beta <= alpha:
                        break
        return max_eval
    else:
        min_eval = math.inf
        for i in range(3):
            for j in range(3):
                if board[i][j] == " ":
                    board[i][j] = "O"
                    eval = minimax(board, depth - 1, True, alpha, beta)
                    board[i][j] = " "
                    min_eval = min(min_eval, eval)
                    beta = min(beta, eval)
                    if beta <= alpha:
                        break
        return min_eval

def find_best_move(board, depth):
    best_eval = -math.inf
    best_move = None
    for i in range(3):
        for j in range(3):
            if board[i][j] == " ":
                board[i][j] = "X"
                eval = minimax(board, depth, False, -math.inf, math.inf)
                board[i][j] = " "
                if eval > best_eval:
                    best_eval = eval
                    best_move = (i, j)
    return best_move


def find_best_move_random(board):
    legal_moves = [(i, j) for i in range(3) for j in range(3) if board[i][j] == " "]
    return random.choice(legal_moves)

def on_click(row, col):
    global user_wins, ai_wins
    if board[row][col] == " " and not is_winner(board, "X") and not is_winner(board, "O") and not is_draw(board):
        board[row][col] = "O"
        buttons[row][col].config(text="O", state=tk.DISABLED)
        difficulty_level = difficulty.get()
        if not is_winner(board, "O") and not is_draw(board):
            if difficulty_level == "Easy":
                ai_move = find_best_move_random(board)
            elif difficulty_level == "Medium":
                ai_move = find_best_move(board, depth=4)
            else:
                ai_move = find_best_move(board, depth=6)
            board[ai_move[0]][ai_move[1]] = "X"
            buttons[ai_move[0]][ai_move[1]].config(text="X", state=tk.DISABLED)

        if is_winner(board, "X"):
            status_label.config(text="AI player (X) wins!", fg="#4CAF50")
            ai_wins_label.config(text=f"AI Wins: {ai_wins + 1}")
            ai_wins += 1
        elif is_winner(board, "O"):
            status_label.config(text="Human player (O) wins!", fg="#FF4C4C")
            user_wins_label.config(text=f"Human Wins: {user_wins + 1}")
            user_wins += 1
        elif is_draw(board):
            status_label.config(text="It's a draw!", fg="#F0A500")
def reset_game():
    global board
    board = create_board()
    for i in range(3):
        for j in range(3):
            buttons[i][j].config(text=" ", state=tk.NORMAL)
    status_label.config(text="")
    ai_wins_label.config(text=f"AI Wins: {ai_wins}")
    user_wins_label.config(text=f"Human Wins: {user_wins}")

root = tk.Tk()
root.withdraw()
user_symbol = simpledialog.askstring("Choose Your Symbol", "Choose 'X' or 'O' as your symbol:", initialvalue="X")
root.deiconify()

user_symbol = user_symbol.upper()
if user_symbol == "O":
    ai_symbol = "X"
else:
    ai_symbol = "O"
user_symbol_color = "black" if user_symbol == "X" else "blue"
ai_symbol_color = "black" if ai_symbol == "X" else "blue"

root.title("Tic-Tac-Toe")
root.configure(bg="#EAEAEA")


labl = tk.Label(root, text="Tic Tac Toe", font=("Helvetica", 15, "bold"), fg="red", bg="#202021")
labl.pack(pady=5)

game_frame = tk.Frame(root, bg="black", padx=10, pady=10)
game_frame.pack()

board = create_board()


buttons = [[None for _ in range(3)] for _ in range(3)]
for i in range(3):
    for j in range(3):
        buttons[i][j] = tk.Button(game_frame, text=" ", width=7, height=3, font=("Helvetica", 20, "bold"), bg="skyblue",
                                  command=lambda row=i, col=j: on_click(row, col))
        buttons[i][j].grid(row=i, column=j, padx=5, pady=5)

status_label = tk.Label(game_frame, text="", font=("Helvetica", 16, "bold"), bg="black")
status_label.grid(row=3, columnspan=3, pady=7)

reset_button = tk.Button(game_frame, text="Reset", font=("Helvetica", 14), bg="red", activebackground="red", bd=2,relief="ridge",
                         command=reset_game)
reset_button.grid(row=4, columnspan=3, pady=5)

# Difficulty Level Selection
difficulty = tk.StringVar()
difficulty.set("Medium")  # Default difficulty level
easy_button = tk.Radiobutton(game_frame, text="Easy", variable=difficulty, value="Easy", font=("Helvetica", 12),
                             bg="white")
easy_button.grid(row=5, column=0, padx=5, pady=5)
medium_button = tk.Radiobutton(game_frame, text="Medium", variable=difficulty, value="Medium", font=("Helvetica", 12),
                               bg="white")
medium_button.grid(row=5, column=1, padx=5, pady=5)
hard_button = tk.Radiobutton(game_frame, text="Hard", variable=difficulty, value="Hard", font=("Helvetica", 12),
                             bg="white")
hard_button.grid(row=5, column=2, padx=5, pady=5)

# Scoreboard
user_wins = 0
ai_wins = 0
user_wins_label = tk.Label(game_frame, text=f"Human Wins: {user_wins}", font=("Helvetica", 14), bg="#EAEAEA")
user_wins_label.grid(row=6, column=0, padx=5, pady=5)
ai_wins_label = tk.Label(game_frame, text=f"AI Wins: {ai_wins}", font=("Helvetica", 14), bg="#EAEAEA")
ai_wins_label.grid(row=6, column=2, padx=5, pady=5)

root.mainloop()
