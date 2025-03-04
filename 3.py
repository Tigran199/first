from typing import List

def tic_tac_toe_checker(board: List[List]) -> str:
    for row in board:
        if row[0] == row[1] == row[2] and row[0] != '-':
            return f"{row[0]} wins!"

    for col in range(3):
        if board[0][col] == board[1][col] == board[2][col] and board[0][col] != '-':
            return f"{board[0][col]} wins!"

    if board[0][0] == board[1][1] == board[2][2] and board[0][0] != '-':
        return f"{board[0][0]} wins!"

    if board[0][2] == board[1][1] == board[2][0] and board[0][2] != '-':
        return f"{board[0][2]} wins!"

    for row in board:
        if '-' in row:
            return "unfinished!"

    return "draw!"

board1 = [
    ['-', '-', 'o'],
    ['-', 'x', 'o'],
    ['x', 'o', 'x']
]
print(tic_tac_toe_checker(board1))  

board2 = [
    ['-', '-', 'o'],
    ['-', 'o', 'o'],
    ['x', 'x', 'x']
]
print(tic_tac_toe_checker(board2)) 