import functions as logic
from game_state import GRID
def fix_board_pos(gs, INNER_W, INNER_X, H):
    gs.CELL=(INNER_W-16)//GRID
    gs.GX=INNER_X+(INNER_W-GRID*gs.CELL)//2
    gs.GY=int(H*0.105)
def load_level(target_lvl, gs, wallet, INNER_W, INNER_X, H):
    board, tray, solution, path = logic.generate_level(target_lvl)
    gs.board=board; gs.solution=solution; gs.path=path; gs.tray=tray; gs.level=target_lvl
    gs.locked=[[False]*GRID for _ in range(GRID)]
    for r in range(GRID):
        for c in range(GRID):
            if gs.board[r][c] in ('START','END','BLOCK'): gs.locked[r][c]=True
    gs.current_pipe=None; gs.flow_active=False; gs.anim=0; gs.win_path=[]; gs.drag=None
    if hasattr(gs,'undo_stack'): gs.undo_stack.clear()
    gs.get_next_pipe()
    wallet.data["level"]=target_lvl
    if target_lvl > wallet.data.get("max_level",1): wallet.data["max_level"]=target_lvl
    wallet.save()
    fix_board_pos(gs, INNER_W, INNER_X, H)