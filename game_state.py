import functions as logic
import copy
import os
import json

GRID = 5
SAVE_FILE = "savegame.json"

class GameState:
    def __init__(self, W, H):
        self.W, self.H = W, H
        self.CELL = 70
        self.GX = 0
        self.GY = 0
        self.tray_h = 110

        # Level load from save
        self.level = 1
        if os.path.exists(SAVE_FILE):
            try:
                with open(SAVE_FILE, "r") as f:
                    data = json.load(f)
                    self.level = data.get("level", 1)
            except:
                self.level = 1

        self.board = []
        self.tray = []
        self.solution = {}
        self.path = []
        self.current_pipe = None
        self.drag = None
        self.locked = []
        self.undo_stack = []
        self.flow_active = False
        self.win_path = []
        self.anim = 0
        self.flow_phase = 0

        # Tank - 1.0 = full, 0.0 = empty
        self.start_tank = 1.0
        self.end_tank = 0.0

        self.new_level()

    def new_level(self):
        self.board, self.tray, self.solution, self.path = logic.generate_level(GRID, self.level)
        self.locked = [[False]*GRID for _ in range(GRID)]
        for r in range(GRID):
            for c in range(GRID):
                if self.board[r][c] in ('START','END','BLOCK'):
                    self.locked[r][c] = True
        self.get_next_pipe()
        self.undo_stack = []
        self.flow_active = False
        self.win_path = []
        self.anim = 0
        self.flow_phase = 0
        self.start_tank = 1.0
        self.end_tank = 0.0

    def get_next_pipe(self):
        if self.tray:
            self.current_pipe = self.tray.pop(0)
        else:
            self.current_pipe = None

    def push_undo(self):
        self.undo_stack.append({
            'board': copy.deepcopy(self.board),
            'tray': self.tray.copy(),
            'current': self.current_pipe,
            'locked': copy.deepcopy(self.locked),
            'start_tank': self.start_tank,
            'end_tank': self.end_tank
        })

    def undo_last(self):
        if not self.undo_stack:
            return
        last = self.undo_stack.pop()
        self.board = last['board']
        self.tray = last['tray']
        self.current_pipe = last['current']
        self.locked = last['locked']
        self.start_tank = last.get('start_tank', 1.0)
        self.end_tank = last.get('end_tank', 0.0)

    def undo_specific(self, r, c):
        if self.board[r][c] is None or self.board[r][c] in ('START','END','BLOCK'):
            return
        self.push_undo()
        removed_pipe = self.board[r][c]
        self.board[r][c] = None
        self.locked[r][c] = False
        if self.current_pipe:
            self.tray.append(self.current_pipe)
        self.current_pipe = removed_pipe

    def save_level(self):
        try:
            data = {}
            if os.path.exists(SAVE_FILE):
                with open(SAVE_FILE, "r") as f:
                    data = json.load(f)
            data["level"] = self.level
            with open(SAVE_FILE, "w") as f:
                json.dump(data, f)
        except:
            pass

    def next_level(self):
        self.level += 1
        self.save_level()
        self.new_level()