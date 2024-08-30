import numpy as np
import tkinter as tk
from tkinter import ttk, messagebox

BLUE = "#0000FF"
BLACK = "#000000"
RED = "#FF0000"
YELLOW = "#FFFF00"

ROW_COUNT = 6
COLUMN_COUNT = 7

def create_board():
    board = np.zeros((ROW_COUNT, COLUMN_COUNT))
    return board

def drop_piece(board, row, col, piece):
    board[row][col] = piece

def is_valid_location(board, col):
    return board[ROW_COUNT - 1][col] == 0

def get_next_open_row(board, col):
    for r in range(ROW_COUNT):
        if board[r][col] == 0:
            return r

def print_board(board):
    print(np.flip(board, 0))

def winning_move(board, piece):
    # Check horizontal locations for win
    for c in range(COLUMN_COUNT - 3):
        for r in range(ROW_COUNT):
            if board[r][c] == piece and board[r][c + 1] == piece and board[r][c + 2] == piece and board[r][c + 3] == piece:
                return True

    # Check vertical locations for win
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT - 3):
            if board[r][c] == piece and board[r + 1][c] == piece and board[r + 2][c] == piece and board[r + 3][c] == piece:
                return True

    # Check positively sloped diagonals
    for c in range(COLUMN_COUNT - 3):
        for r in range(ROW_COUNT - 3):
            if board[r][c] == piece and board[r + 1][c + 1] == piece and board[r + 2][c + 2] == piece and board[r + 3][c + 3] == piece:
                return True

    # Check negatively sloped diagonals
    for c in range(COLUMN_COUNT - 3):
        for r in range(3, ROW_COUNT):
            if board[r][c] == piece and board[r - 1][c + 1] == piece and board[r - 2][c + 2] == piece and board[r - 3][c + 3] == piece:
                return True

def draw_board(board):
    canvas.delete("all")
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            canvas.create_rectangle(c * SQUARESIZE, r * SQUARESIZE + SQUARESIZE, (c + 1) * SQUARESIZE, (r + 1) * SQUARESIZE + SQUARESIZE, fill=BLUE)
            canvas.create_oval(c * SQUARESIZE + 5, r * SQUARESIZE + SQUARESIZE + 5, (c + 1) * SQUARESIZE - 5, (r + 1) * SQUARESIZE + SQUARESIZE - 5, fill=BLACK)

    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            if board[r][c] == 1:
                canvas.create_oval(c * SQUARESIZE + 5, (ROW_COUNT - r - 1) * SQUARESIZE + SQUARESIZE + 5, (c + 1) * SQUARESIZE - 5, (ROW_COUNT - r) * SQUARESIZE + SQUARESIZE - 5, fill=RED)
            elif board[r][c] == 2:
                canvas.create_oval(c * SQUARESIZE + 5, (ROW_COUNT - r - 1) * SQUARESIZE + SQUARESIZE + 5, (c + 1) * SQUARESIZE - 5, (ROW_COUNT - r) * SQUARESIZE + SQUARESIZE - 5, fill=YELLOW)

def on_click(event):
    global turn, game_over

    if game_over:
        return

    x = event.x
    col = x // SQUARESIZE

    if is_valid_location(board, col):
        row = get_next_open_row(board, col)
        drop_piece(board, row, col, turn + 1)

        if winning_move(board, turn + 1):
            game_over = True
            winner = "Player 1" if turn == 0 else "Player 2"
            messagebox.showinfo("Connect 4", f"{winner} wins!!")
        
        print_board(board)
        draw_board(board)
        turn = (turn + 1) % 2

board = create_board()
print_board(board)
game_over = False
turn = 0

# Initialize tkinter
root = tk.Tk()
root.title("Connect 4")

SQUARESIZE = 100
width = COLUMN_COUNT * SQUARESIZE
height = (ROW_COUNT + 1) * SQUARESIZE

style = ttk.Style()
style.theme_use("clam")  # You can choose other themes like 'alt', 'default', 'classic'

canvas = tk.Canvas(root, width=width, height=height, bg="white", highlightthickness=0)
canvas.pack()

draw_board(board)

canvas.bind("<Button-1>", on_click)

root.mainloop()
