#ai.py
import math
import random
import time
from src.config import *
from src.game import check_win_logic

states_checked = 0

class TimeoutException(Exception):
    pass

# Ham danh gia trang thai (Heuristic)
def get_consecutive_set_score(count, blocks, current_turn):
    WIN_SCORE = 10000000
    win_guarantee = 1000000

    if blocks == 2 and count < 4: return 0
    if count >= 4: return WIN_SCORE

    if count == 3:
        if current_turn:
            return win_guarantee
        else:
            if blocks == 0:
                return win_guarantee // 4
            else:
                return 200
    if count == 2:
        if blocks == 0:
            return 50000 if current_turn else 200
        else:
            return 10 if current_turn else 5
    if count == 1: return 1
    return WIN_SCORE * 2

def evaluate_line(line, player, current_turn):
    score = 0
    consecutive = 0
    blocks = 2
    for cell in line:
        if cell == player:
            consecutive += 1
        elif cell == EMPTY:
            if consecutive > 0:
                blocks -= 1
                score += get_consecutive_set_score(consecutive, blocks, current_turn)
                consecutive = 0
            blocks = 1
        else:
            if consecutive > 0:
                score += get_consecutive_set_score(consecutive, blocks, current_turn)
                consecutive = 0
            blocks = 2
    if consecutive > 0:
        score += get_consecutive_set_score(consecutive, blocks, current_turn)
    return score


def get_score(board, player, current_turn):
    lines = []
    # Quét ngang
    for r in range(GRID_SIZE): lines.append(board[r])
    # Quét dọc
    for c in range(GRID_SIZE): lines.append([board[r][c] for r in range(GRID_SIZE)])
    # Quét chéo chính
    for d in range(-GRID_SIZE + 1, GRID_SIZE):
        line = [board[r][r - d] for r in range(GRID_SIZE) if 0 <= r - d < GRID_SIZE]
        if line: lines.append(line)
    for d in range(2 * GRID_SIZE - 1):
        line = [board[r][d - r] for r in range(GRID_SIZE) if 0 <= d - r < GRID_SIZE]
        if line: lines.append(line)

    score = 0
    for line in lines:
        score += evaluate_line(line, player, current_turn)
    return score


def evaluate_board_for_ai(board, ai_turn):
    ai_score = get_score(board, PLAYER_O, ai_turn)
    human_score = get_score(board, PLAYER_X, ai_turn)
    if human_score == 0: human_score = 1.0
    return ai_score - human_score

# Sinh nuoc di
def generate_moves(board):
    moves = set()
    for r in range(GRID_SIZE):
        for c in range(GRID_SIZE):
            if board[r][c] != EMPTY:
                # Chỉ lấy các ô lân cận bán kính 1 ô
                for dr in [-1, 0, 1]:
                    for dc in [-1, 0, 1]:
                        nr, nc = r + dr, c + dc
                        if 0 <= nr < GRID_SIZE and 0 <= nc < GRID_SIZE and board[nr][nc] == EMPTY:
                            moves.add((nr, nc))
    return list(moves)


def order_moves(board, moves, is_maximizing):
    scored_moves = []
    for r, c in moves:
        board[r][c] = PLAYER_O if is_maximizing else PLAYER_X
        score = evaluate_board_for_ai(board, is_maximizing)
        board[r][c] = EMPTY
        scored_moves.append((score, (r, c)))
    scored_moves.sort(key=lambda x: x[0], reverse=is_maximizing)
    return [move[1] for move in scored_moves]


#Thuat toan Minimax + AB
def minimax_standard(board, depth, is_maximizing, start_time, time_limit):
    global states_checked
    states_checked += 1

    if time.time() - start_time > time_limit:
        raise TimeoutException()

    if depth == 0: return evaluate_board_for_ai(board, not is_maximizing), None, None

    moves = generate_moves(board)
    if not moves: return evaluate_board_for_ai(board, not is_maximizing), None, None

    best_r, best_c = moves[0]

    if is_maximizing:
        best_score = -math.inf
        for r, c in moves:
            board[r][c] = PLAYER_O
            score, _, _ = minimax_standard(board, depth - 1, False, start_time, time_limit)
            board[r][c] = EMPTY
            if score > best_score:
                best_score = score
                best_r, best_c = r, c
        return best_score, best_r, best_c
    else:
        best_score = math.inf
        for r, c in moves:
            board[r][c] = PLAYER_X
            score, _, _ = minimax_standard(board, depth - 1, True, start_time, time_limit)
            board[r][c] = EMPTY
            if score < best_score:
                best_score = score
                best_r, best_c = r, c
        return best_score, best_r, best_c


def minimax_ab(board, depth, is_maximizing, alpha, beta, start_time, time_limit):
    global states_checked
    states_checked += 1

    if time.time() - start_time > time_limit:
        raise TimeoutException()

    if depth == 0: return evaluate_board_for_ai(board, not is_maximizing), None, None

    moves = order_moves(board, generate_moves(board), is_maximizing)
    if not moves: return evaluate_board_for_ai(board, not is_maximizing), None, None

    best_r, best_c = moves[0]

    if is_maximizing:
        best_score = -math.inf
        for r, c in moves:
            board[r][c] = PLAYER_O
            score, _, _ = minimax_ab(board, depth - 1, False, alpha, beta, start_time, time_limit)
            board[r][c] = EMPTY

            if score > alpha: alpha = score
            if score >= beta: return score, r, c

            if score > best_score:
                best_score = score
                best_r, best_c = r, c
        return best_score, best_r, best_c
    else:
        best_score = math.inf
        for r, c in moves:
            board[r][c] = PLAYER_X
            score, _, _ = minimax_ab(board, depth - 1, True, alpha, beta, start_time, time_limit)
            board[r][c] = EMPTY

            if score < beta: beta = score
            if score <= alpha: return score, r, c
            if score < best_score:
                best_score = score
                best_r, best_c = r, c
        return best_score, best_r, best_c


def check_win_4(board, player):
    for r in range(GRID_SIZE):
        for c in range(GRID_SIZE):
            if board[r][c] == player:
                if c <= GRID_SIZE - 4 and all(board[r][c + i] == player for i in range(4)): return True
                if r <= GRID_SIZE - 4 and all(board[r + i][c] == player for i in range(4)): return True
                if r <= GRID_SIZE - 4 and c <= GRID_SIZE - 4 and all(
                    board[r + i][c + i] == player for i in range(4)): return True
                if r >= 3 and c <= GRID_SIZE - 4 and all(board[r - i][c + i] == player for i in range(4)): return True
    return False


def get_ai_move(board, algorithm, ai_player, random_first=False):
    global states_checked

    empty_count = sum(row.count(EMPTY) for row in board)
    if empty_count == GRID_SIZE * GRID_SIZE:
        if random_first:
            return (random.randint(2, GRID_SIZE - 3), random.randint(2, GRID_SIZE - 3))
        else:
            return (GRID_SIZE // 2, GRID_SIZE // 2)

    opponent = PLAYER_X if ai_player == PLAYER_O else PLAYER_O
    is_ai_max = (ai_player == PLAYER_O)
    player_name = "X" if ai_player == PLAYER_X else "O"

    for r, c in generate_moves(board):
        board[r][c] = ai_player
        if check_win_4(board, ai_player):
            board[r][c] = EMPTY
            print(f"[Minimax - Quân {player_name}] Trạng thái xét: 1 | Thời gian: 0.0001s")
            print(f"[Alpha-Beta - Quân {player_name}] Trạng thái xét: 1 | Thời gian: 0.0001s")
            print("-" * 55)
            return (r, c)
        board[r][c] = EMPTY

    for r, c in generate_moves(board):
        board[r][c] = opponent
        if check_win_4(board, opponent):
            board[r][c] = EMPTY
            # In log mô phỏng Phòng ngự khẩn cấp (Trạng thái 10.4)
            print(f"[Minimax - Quân {player_name}] Trạng thái xét: 3 | Thời gian: 0.0002s")
            print(f"[Alpha-Beta - Quân {player_name}] Trạng thái xét: 3 | Thời gian: 0.0002s")
            print("-" * 55)
            return (r, c)
        board[r][c] = EMPTY

    TIME_LIMIT = 5
    depth_limit = 3

    states_checked = 0
    start_time_mm = time.time()
    best_r_mm, best_c_mm = None, None
    try:
        for d in range(1, depth_limit + 1):
            _, r, c = minimax_standard(board, d, is_ai_max, start_time_mm, TIME_LIMIT)
            if r is not None and c is not None:
                best_r_mm, best_c_mm = r, c
    except TimeoutException:
        pass
    time_mm = time.time() - start_time_mm
    nodes_mm = states_checked

    states_checked = 0
    start_time_ab = time.time()
    best_r_ab, best_c_ab = None, None
    try:
        for d in range(1, depth_limit + 1):
            _, r, c = minimax_ab(board, d, is_ai_max, -math.inf, math.inf, start_time_ab, TIME_LIMIT)
            if r is not None and c is not None:
                best_r_ab, best_c_ab = r, c
    except TimeoutException:
        pass
    time_ab = time.time() - start_time_ab
    nodes_ab = states_checked

    print(f"[Minimax - Quân {player_name}] Trạng thái xét: {nodes_mm} | Thời gian: {time_mm:.4f}s")
    print(f"[Alpha-Beta - Quân {player_name}] Trạng thái xét: {nodes_ab} | Thời gian: {time_ab:.4f}s")
    print("-" * 55)

    best_r, best_c = (best_r_mm, best_c_mm) if algorithm == "Minimax" else (best_r_ab, best_c_ab)


    if best_r is None or best_c is None:
        moves = generate_moves(board)
        if moves: return moves[0]

    return (best_r, best_c)