#game.py
from src.config import *

def check_win_logic(board):
    for r in range(GRID_SIZE):
        for c in range(GRID_SIZE - 3):
            if board[r][c] == board[r][c+1] == board[r][c+2] == board[r][c+3] != EMPTY:
                return board[r][c], [(r,c), (r,c+1), (r,c+2), (r,c+3)]
    for c in range(GRID_SIZE):
        for r in range(GRID_SIZE - 3):
            if board[r][c] == board[r+1][c] == board[r+2][c] == board[r+3][c] != EMPTY:
                return board[r][c], [(r,c), (r+1,c), (r+2,c), (r+3,c)]
    for r in range(GRID_SIZE - 3):
        for c in range(GRID_SIZE - 3):
            if board[r][c] == board[r+1][c+1] == board[r+2][c+2] == board[r+3][c+3] != EMPTY:
                return board[r][c], [(r,c), (r+1,c+1), (r+2,c+2), (r+3,c+3)]
    for r in range(GRID_SIZE - 3):
        for c in range(3, GRID_SIZE):
            if board[r][c] == board[r+1][c-1] == board[r+2][c-2] == board[r+3][c-3] != EMPTY:
                return board[r][c], [(r,c), (r+1,c-1), (r+2,c-2), (r+3,c-3)]
    for r in range(GRID_SIZE):
        for c in range(GRID_SIZE):
            if board[r][c] == EMPTY: return False, []
    return "Tie", []

class CaroGame:
    def __init__(self):
        self.grid = [[EMPTY for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
        self.current_player = PLAYER_X
        self.mode = "PvP"
        self.ai_algo = "Alpha-Beta"
        self.x_ai = "Minimax"
        self.winner = None
        self.win_cells = []
        self.game_over = False
        self.sound_played = False

    def make_move(self, row, col):
        if self.grid[row][col] == EMPTY and not self.game_over:
            self.grid[row][col] = self.current_player
            winner, cells = check_win_logic(self.grid)
            if winner:
                self.winner = winner
                self.win_cells = cells
                self.game_over = True
            else:
                self.current_player = PLAYER_O if self.current_player == PLAYER_X else PLAYER_X
            return True
        return False

    def reset(self):
        current_mode = self.mode
        current_algo = self.ai_algo
        current_x_ai = self.x_ai
        self.__init__()
        self.mode = current_mode
        self.ai_algo = current_algo
        self.x_ai = current_x_ai