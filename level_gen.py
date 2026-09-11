import random
from pipes import get_pipe_for_dirs

def generate_level(a=5, b=None):
    if b is None:
        level = int(a)
        grid_size = 5
    else:
        grid_size = int(a)
        level = int(b)
    if level < 1: level = 1
    random.seed(level * 7919 + grid_size * 1337)
    max_cells = grid_size * grid_size
    if max_cells % 2 == 0: max_cells -= 1
    target_cells = 13 + (level - 1) * 2
    if target_cells > max_cells: target_cells = max_cells
    START = (0, 0)
    END = (grid_size - 1, grid_size - 1)
    END_NEIGH = [(grid_size - 2, grid_size - 1), (grid_size - 1, grid_size - 2)]
    path = None
    for _ in range(15000):
        final_before = random.choice(END_NEIGH)
        p = [START]; visited = {START}
        while len(p) < target_cells - 1:
            r, c = p[-1]
            rem = (target_cells - 1) - len(p)
            if abs(r - final_before[0]) + abs(c - final_before[1]) > rem: break
            moves = []
            for dr, dc in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                nr, nc = r + dr, c + dc
                if 0 <= nr < grid_size and 0 <= nc < grid_size:
                    if (nr, nc) not in visited and (nr, nc)!= END:
                        if abs(nr - final_before[0]) + abs(nc - final_before[1]) <= rem - 1:
                            moves.append((nr, nc))
            if not moves: break
            random.shuffle(moves)
            p.append(moves[0]); visited.add(moves[0])
        if len(p) == target_cells - 1 and p[-1] == final_before:
            p.append(END); path = p; break
    if path is None:
        path = [(0,0),(0,1),(0,2),(1,2),(2,2),(2,1),(3,1),(3,2),(3,3),(2,3),(2,4),(3,4),(4,4)]
    board = [['BLOCK' for _ in range(grid_size)] for _ in range(grid_size)]
    solution = {}
    def d_of(fr, fc, tr, tc):
        if tr == fr - 1: return 0
        if tc == fc + 1: return 1
        if tr == fr + 1: return 2
        return 3
    for i in range(len(path)):
        r, c = path[i]
        if i == 0: board[r][c] = 'START'; continue
        if i == len(path) - 1: board[r][c] = 'END'; continue
        pr, pc = path[i-1]; nr, nc = path[i+1]
        pipe = get_pipe_for_dirs(d_of(r, c, pr, pc), d_of(r, c, nr, nc))
        solution[(r, c)] = pipe
        board[r][c] = None
    tray = list(solution.values())
    random.shuffle(tray)
    return board, tray, solution, path