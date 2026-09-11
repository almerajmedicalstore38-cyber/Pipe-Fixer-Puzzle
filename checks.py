import math
from pipes import DRAG_OFFSET

def check_win(board, solution):
    for (r, c), correct in solution.items():
        if board[r][c]!= correct: return False, []
    for r in range(len(board)):
        for c in range(len(board[0])):
            val = board[r][c]
            if val in ('START','END','BLOCK',None): continue
            if (r,c) not in solution: return False, []
    return True, list(solution.keys())

def get_hover_valid(drag_pipe, mx, my, board, solution, GX, GY, CELL, GRID):
    if not drag_pipe: return False
    vcx = mx; vcy = my - DRAG_OFFSET
    for r in range(GRID):
        for c in range(GRID):
            if board[r][c] is not None: continue
            bcx = GX + c * CELL + CELL // 2; bcy = GY + r * CELL + CELL // 2
            if math.hypot(vcx-bcx, vcy-bcy) < CELL*1.1: return True
    return False

def find_drop_cell(drag_pipe, mx, my, board, solution, GX, GY, CELL, GRID):
    if not drag_pipe: return None
    vcx = mx; vcy = my - DRAG_OFFSET
    best=None; best_dist=9999
    for r in range(GRID):
        for c in range(GRID):
            if board[r][c] is not None: continue
            bcx = GX + c * CELL + CELL // 2; bcy = GY + r * CELL + CELL // 2
            dist = math.hypot(vcx-bcx, vcy-bcy)
            if dist < CELL*1.3 and dist < best_dist: best_dist=dist; best=(r,c)
    return best

def get_wrong_cells(board, solution):
    wrong=[]
    for (r,c), correct in solution.items():
        if board[r][c] is not None and board[r][c]!=correct: wrong.append((r,c))
    for r in range(len(board)):
        for c in range(len(board[0])):
            if board[r][c] in ('START','END','BLOCK',None): continue
            if (r,c) not in solution and (r,c) not in wrong: wrong.append((r,c))
    return wrong