import pygame
import functions as logic, gui, math
from game_state import GameState, GRID
from wallet_functions import Wallet
from ad_manager import AdManager
import config, sounds
import wallet_pro_gui as wallet_gui
from firebase_manager_lite import FirebaseManager
from referral_system import ReferralSystem
from withdraw_system import WithdrawSystem
from level import fix_board_pos, load_level
from ui import draw_all
from login_screen import show_auth_screen
from auth_manager import get_user_display_name, logout_user, get_current_user
import random, string
import os

pygame.init()
try: pygame.mixer.init()
except: print("[AUDIO] Mixer disabled")

W, H = 720, 1280
screen = pygame.display.set_mode((W, H))
config.init(W, H)
clock = pygame.time.Clock()

# === 300% PROFIT FINAL ===
config.DOUBLE_REWARD = 20
config.REPLAY_REWARD = 5
config.HINT_COST = 15

wallet = Wallet()

def do_login_flow():
    logged_email = show_auth_screen(screen, W, H, config)
    if logged_email:
        wallet.data['email'] = logged_email
        wallet.data['is_gmail_user'] = True
        if not wallet.data.get('referral_code'):
            wallet.data['referral_code'] = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
        wallet.save()
        return True
    else:
        pygame.quit(); exit()

if not wallet.data.get('is_gmail_user') or not wallet.data.get('email'):
    do_login_flow()

gs = GameState(W, H)
try: sounds.load(wallet.data.get("muted", False))
except: pass

fix_board_pos(gs, config.INNER_W, config.INNER_X, H)

try:
    target = int(wallet.data.get("level", 1))
    board, tray, solution, path = logic.generate_level(target)
    gs.board = board; gs.solution = solution; gs.path = path; gs.tray = tray; gs.level = target
    gs.locked = [[False]*GRID for _ in range(GRID)]
    for r in range(GRID):
        for c in range(GRID):
            if gs.board[r][c] in ('START', 'END', 'BLOCK'):
                gs.locked[r][c] = True
    gs.current_pipe = None; gs.get_next_pipe()
except:
    gs.level = int(wallet.data.get("level", 1))
    fix_board_pos(gs, config.INNER_W, config.INNER_X, H)

ad_manager = AdManager(W, H)

show_level_select = show_win_popup = False
level_btns = []; level_close_rect = pygame.Rect(0, 0, 0, 0)
wallet_btn = coins_btn = mute_btn = lvl_btn = pygame.Rect(0, 0, 0, 0)
wrong_highlight = []; selected_cell = None
running = True; mx, my = pygame.mouse.get_pos()

# === 300% PROFIT - REWARD VARIABLE ===
coins_to_give = 20

while running:
    for e in pygame.event.get():
        if e.type == pygame.QUIT: running = False
        if e.type == pygame.MOUSEMOTION: mx, my = e.pos
        if e.type == pygame.MOUSEBUTTONDOWN:
            mx, my = e.pos
            # Banner par click ko ignore karo (Real AdMob khud handle karega)
            if hasattr(ad_manager, 'banner_rect') and ad_manager.banner_rect.collidepoint(mx, my):
                continue

            if show_level_select:
                if level_close_rect.collidepoint(e.pos):
                    try: sounds.play_click()
                    except: pass
                    show_level_select = False; continue
                for rct, lvl in level_btns:
                    if rct.collidepoint(e.pos):
                        try: sounds.play_click()
                        except: pass
                        load_level(lvl, gs, wallet, config.INNER_W, config.INNER_X, H)
                        show_level_select = False; show_win_popup = False; selected_cell = None; wrong_highlight.clear(); break
                continue

            if show_win_popup:
                if claim_btn and claim_btn.collidepoint(e.pos):
                    try: sounds.play_click()
                    except: pass
                    load_level(gs.level+1, gs, wallet, config.INNER_W, config.INNER_X, H)
                    show_win_popup = False; selected_cell = None; wrong_highlight.clear()
                elif double_btn and double_btn.collidepoint(e.pos):
                    try: sounds.play_click()
                    except: pass
                    def give_double():
                        # === FINAL 300% ANTI-FARM LOGIC ===
                        max_lvl = wallet.data.get("max_level", 1)
                        if gs.level >= max_lvl:
                            wallet.add_coins(20)
                            print(f"[REWARD] New Level {gs.level} = +20C (300% Profit Safe)")
                        else:
                            wallet.add_coins(5)
                            print(f"[REWARD] Old Level Replay = +5C Only - Anti Farm")
                        try:
                            ref = ReferralSystem(wallet)
                            ref.on_ad_watched(20)
                        except Exception as ex:
                            print(f"Referral error: {ex}")
                        load_level(gs.level+1, gs, wallet, config.INNER_W, config.INNER_X, H)

                    # === REAL AD CALL - APK me Original Google Ad ayega ===
                    ad_manager.start_ad(callback=give_double, reward=coins_to_give)
                    show_win_popup = False; selected_cell = None; wrong_highlight.clear()
                continue

            if not gs.flow_active:
                if lvl_btn.collidepoint(e.pos):
                    try: sounds.play_click()
                    except: pass
                    show_level_select = True; continue
                if wallet_btn.collidepoint(e.pos) or coins_btn.collidepoint(e.pos):
                    try: sounds.play_click()
                    except: pass
                    result = wallet_gui.open_wallet(screen, wallet, W, H)
                    if result == "logout":
                        logout_user()
                        wallet.data['is_gmail_user'] = False
                        wallet.data['email'] = ""
                        wallet.save()
                        do_login_flow()
                    continue
                if mute_btn.collidepoint(e.pos):
                    sounds.is_muted = not sounds.is_muted; wallet.set_muted(sounds.is_muted)
                    try:
                        if sounds.is_muted: pygame.mixer.music.pause()
                        else: pygame.mixer.music.unpause()
                    except: pass
                    continue
                if hint_btn.collidepoint(e.pos) and not ad_manager.is_playing:
                    try: sounds.play_click()
                    except: pass
                    def give_hint():
                        wrong = logic.get_wrong_cells(gs.board, gs.solution)
                        if wrong:
                            wrong_highlight.clear(); wrong_highlight.extend(wrong); return
                        for (r, c), cp in gs.solution.items():
                            if gs.board[r][c] is None:
                                gs.push_undo(); gs.board[r][c] = cp; gs.locked[r][c] = True
                                if gs.current_pipe == cp: gs.get_next_pipe()
                                elif cp in gs.tray:
                                    try: gs.tray.remove(cp)
                                    except: pass
                                break
                    # === HINT REAL AD ===
                    ad_manager.start_ad(callback=give_hint, reward=0); continue
                if flow_btn.collidepoint(e.pos):
                    try: sounds.play_click()
                    except: pass
                    if gs.current_pipe is not None or len(gs.tray) > 0:
                        wrong_highlight.clear()
                        for (r, c), _ in gs.solution.items():
                            if gs.board[r][c] is None: wrong_highlight.append((r, c))
                        continue
                    wrong = logic.get_wrong_cells(gs.board, gs.solution)
                    if wrong:
                        wrong_highlight.clear(); wrong_highlight.extend(wrong); continue
                    ok, _ = logic.check_win(gs.board, gs.solution)
                    if ok:
                        try: sounds.play_flow()
                        except: pass
                        gs.flow_active = True; gs.win_path = gs.path; gs.anim = 0
                    continue
                if undo_btn.collidepoint(e.pos):
                    try: sounds.play_click()
                    except: pass
                    if selected_cell: gs.undo_specific(*selected_cell); selected_cell = None
                    else: gs.undo_last()
                    continue
                if pygame.Rect(box_x, box_y, box_size, box_size).collidepoint(e.pos) and gs.current_pipe:
                    try: sounds.play_click()
                    except: pass
                    gs.drag = gs.current_pipe; continue
                for r in range(GRID):
                    for c in range(GRID):
                        if gs.GX+c*gs.CELL < mx < gs.GX+(c+1)*gs.CELL and gs.GY+r*gs.CELL < my < gs.GY+(r+1)*gs.CELL:
                            val = gs.board[r][c]
                            if val and val not in ('START', 'END', 'BLOCK'):
                                try: sounds.play_click()
                                except: pass
                                selected_cell = None if selected_cell == (r, c) else (r, c)
                                break
        if e.type == pygame.MOUSEBUTTONUP and gs.drag:
            vx = mx; vy = my-config.DRAG_OFFSET; c = int((vx-gs.GX)//gs.CELL); r = int((vy-gs.GY)//gs.CELL); placed = False
            if 0 <= r < GRID and 0 <= c < GRID and gs.board[r][c] is None:
                gs.push_undo(); gs.board[r][c] = gs.drag; gs.locked[r][c] = True; gs.get_next_pipe(); placed = True
            if not placed:
                best = None; bd = gs.CELL*1.1
                for dr in (-1, 0, 1):
                    for dc in (-1, 0, 1):
                        rr = r+dr; cc = c+dc
                        if 0 <= rr < GRID and 0 <= cc < GRID and gs.board[rr][cc] is None:
                            cx = gs.GX+cc*gs.CELL+gs.CELL//2; cy = gs.GY+rr*gs.CELL+gs.CELL//2
                            d = math.hypot(vx-cx, vy-cy)
                            if d < bd: bd = d; best = (rr, cc)
                if best:
                    gs.push_undo(); gs.board[best[0]][best[1]] = gs.drag; gs.locked[best[0]][best[1]] = True; gs.get_next_pipe()
            gs.drag = None

    hover_valid = False
    if gs.drag:
        vx = mx; vy = my-config.DRAG_OFFSET; c = int((vx-gs.GX)//gs.CELL); r = int((vy-gs.GY)//gs.CELL)
        if 0 <= r < GRID and 0 <= c < GRID and gs.board[r][c] is None: hover_valid = True

    box_size = gs.CELL+16; gs.tray_h = box_size+36; tray_y = gs.GY+GRID*gs.CELL+18
    box_x = config.INNER_X+(config.INNER_W-box_size)//2; box_y = tray_y+10
    gap = 12; flow_w = int(config.INNER_W*0.58); undo_w = int(config.INNER_W*0.36)
    hint_y = tray_y+gs.tray_h+14; hint_btn = pygame.Rect(config.INNER_X, hint_y, config.INNER_W, 42)
    btn_y = hint_y+52; flow_btn = pygame.Rect(config.INNER_X, btn_y, flow_w, 44); undo_btn = pygame.Rect(config.INNER_X+flow_w+gap, btn_y, undo_w, 44)
    btn_w = config.INNER_W//4-6; top_y = int(H*0.015)
    lvl_btn = pygame.Rect(config.INNER_X+4, top_y+6, btn_w, int(H*0.065)-12)
    wallet_btn = pygame.Rect(config.INNER_X+btn_w+8, top_y+6, btn_w, int(H*0.065)-12)
    coins_btn = pygame.Rect(config.INNER_X+btn_w*2+12, top_y+6, btn_w, int(H*0.065)-12)
    mute_btn = pygame.Rect(config.INNER_X+btn_w*3+16, top_y+6, btn_w-8, int(H*0.065)-12)

    draw_all(screen, gs, logic, wallet, config, wrong_highlight, selected_cell, hover_valid, box_x, box_y, box_size, hint_btn, flow_btn, undo_btn, lvl_btn, wallet_btn, coins_btn, mute_btn, sounds.is_muted)
    if gs.drag:
        gui.draw_pipe(screen, logic.PIPES, gs.drag, mx-gs.CELL//2, my-gs.CELL//2-config.DRAG_OFFSET, gs.CELL, is_tray=True, valid_hint=hover_valid)

    claim_btn = double_btn = None
    if show_win_popup and not show_level_select:
        overlay = pygame.Surface((W, H)); overlay.fill((0, 0, 0)); overlay.set_alpha(180); screen.blit(overlay, (0, 0))
        pop_w, pop_h = int(config.INNER_W*0.92), int(H*0.32); pop_x = config.INNER_X+(config.INNER_W-pop_w)//2; pop_y = H//2-pop_h//2
        pygame.draw.rect(screen, (20, 30, 60), (pop_x, pop_y, pop_w, pop_h), border_radius=20)
        pygame.draw.rect(screen, (0, 230, 255), (pop_x, pop_y, pop_w, pop_h), width=2, border_radius=20)
        screen.blit(config.F_WIN.render("YOU WIN!", True, (0, 255, 130)), config.F_WIN.render("YOU WIN!", True, (0, 255, 130)).get_rect(center=(W//2, pop_y+50)))

        max_lvl = wallet.data.get("max_level", 1)
        is_new = (gs.level >= max_lvl)
        if is_new:
            reward_txt = f"New Level! Watch Ad +{config.DOUBLE_REWARD} coins"
            coins_to_give = config.DOUBLE_REWARD
            txt_double = f"AD +{config.DOUBLE_REWARD}C"
        else:
            reward_txt = f"Replay Level {gs.level} - Low Reward"
            coins_to_give = 5
            txt_double = f"AD +5C (Replay)"

        screen.blit(config.F_POP.render(reward_txt, True, (200, 200, 200)), (pop_x+20, pop_y+95))
        screen.blit(config.F_POP.render(f"2000 coins = $1.00", True, (255, 230, 80)), (pop_x+20, pop_y+120))
        claim_btn = pygame.Rect(pop_x+15, pop_y+pop_h-60, int(pop_w*0.42), 50)
        double_btn = pygame.Rect(pop_x+pop_w-int(pop_w*0.52), pop_y+pop_h-60, int(pop_w*0.46), 50)
        pygame.draw.rect(screen, (80, 90, 115), claim_btn, border_radius=14)
        pygame.draw.rect(screen, (255, 215, 0), double_btn, border_radius=14)
        txt1 = config.F_POP.render(f"SKIP (0C)", True, (255, 255, 255))
        txt2 = config.F_POP.render(txt_double, True, (0, 0, 0))
        screen.blit(txt1, txt1.get_rect(center=claim_btn.center))
        screen.blit(txt2, txt2.get_rect(center=double_btn.center))

    if show_level_select:
        overlay = pygame.Surface((W, H)); overlay.fill((0, 0, 0)); overlay.set_alpha(235); screen.blit(overlay, (0, 0))
        pop_w, pop_h = int(W*0.92), int(H*0.78); pop_x = (W-pop_w)//2; pop_y = (H-pop_h)//2
        pygame.draw.rect(screen, (20, 30, 60), (pop_x, pop_y, pop_w, pop_h), border_radius=22)
        title = config.F_WIN.render("SELECT LEVEL", True, (255, 215, 0)); screen.blit(title, title.get_rect(center=(W//2, pop_y+40)))
        max_lvl = wallet.data.get("max_level", wallet.data.get("level", 1))
        cols = 4; btn_s = pop_w//cols-16; gap = 10; start_y = pop_y+100; level_btns = []
        for i in range(1, max_lvl+1):
            row = (i-1)//cols; col = (i-1) % cols
            bx = pop_x+10+col*(btn_s+gap); by = start_y+row*(btn_s+gap)
            if by > pop_y+pop_h-75: break
            rect = pygame.Rect(bx, by, btn_s, btn_s); is_cur = (i == gs.level)
            pygame.draw.rect(screen, (0, 255, 130) if is_cur else (35, 55, 105), rect, border_radius=14)
            txt = config.F_POP.render(str(i), True, (0, 0, 0) if is_cur else (255, 255, 255)); screen.blit(txt, txt.get_rect(center=rect.center)); level_btns.append((rect, i))
        level_close_rect = pygame.Rect(pop_x+20, pop_y+pop_h-60, pop_w-40, 48)
        pygame.draw.rect(screen, (255, 80, 80), level_close_rect, border_radius=14)

    if gs.flow_active and not show_win_popup and not show_level_select and not ad_manager.is_playing:
        gs.anim += 0.50
        if gs.anim >= len(gs.win_path):
            try: sounds.stop_flow()
            except: pass
            gs.flow_active = False; show_win_popup = True

    # === FINAL BANNER LOGIC - Pydroid me clean, APK me Real AdMob ===
    # draw_banner ab andar se hi return kar dega - clean window
    try:
        ad_manager.draw_banner(screen)
    except: pass

    if ad_manager.is_playing:
        ad_manager.update(); ad_manager.draw(screen)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()