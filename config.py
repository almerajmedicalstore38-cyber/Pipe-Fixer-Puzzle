import pygame

# === APP INFO ===
APP_NAME = "Pipe Fixer Puzzle"
APP_DEV = "SHTEDITOR"
PACKAGE_NAME = "com.shteditor.pipefixerpuzzle"

# === 300% PROFIT LOGIC ===
LEVEL_REWARD = 5
DOUBLE_REWARD = 20
AD_REWARD_COINS = 20
REPLAY_REWARD = 5
HINT_COST = 15

COIN_TO_USD = 0.0005
MIN_WITHDRAW_COINS = 2000
REFERRAL_COMMISSION = 0.10

BANNER_ID = "ca-app-pub-3940256099942544/6300978111"
REWARDED_ID = "ca-app-pub-3940256099942544/5224354917"
APP_ID = "ca-app-pub-3940256099942544~3347511713"

MARGIN = 45
DRAG_OFFSET = 90
W = H = INNER_W = INNER_X = 0
F_TOP = F_SMALL = F_HINT = F_FLOW = F_WIN = F_POP = None
F_TITLE = None

def init(w, h):
    global W, H, INNER_W, INNER_X, F_TOP, F_SMALL, F_HINT, F_FLOW, F_WIN, F_POP, F_TITLE
    W, H = w, h
    INNER_W = W - MARGIN * 2 - 10
    INNER_X = MARGIN + 5
    F_TOP = pygame.font.SysFont("Arial", int(W*0.030), bold=True)
    F_SMALL = pygame.font.SysFont("Arial", int(W*0.026), bold=True)
    F_HINT = pygame.font.SysFont("Arial", int(W*0.038), bold=True)
    F_FLOW = pygame.font.SysFont("Arial", int(W*0.042), bold=True)
    F_WIN = pygame.font.SysFont("Arial", int(W*0.060), bold=True)
    F_POP = pygame.font.SysFont("Arial", int(W*0.036), bold=True)
    F_TITLE = pygame.font.SysFont("Arial", int(W*0.032), bold=True)