import pygame
from withdraw_system import WithdrawSystem
from referral_system import ReferralSystem
# === NAME FIX IMPORT ===
from auth_manager import get_user_display_name, get_current_user

METHODS = ["USDT", "JazzCash", "Easypaisa"]
COIN_TO_USD = 0.0001   # FINAL 300% - Pehle 0.001 tha
MIN_WITHDRAW = 10000   # FINAL 300% - Pehle 1000 tha

def draw_wallet_page(surf, wallet, W, H):
    surf.fill((13, 19, 48))
    ft = pygame.font.SysFont("Arial", 24, bold=True)
    surf.blit(ft.render("WALLET", True, (255,255,255)), (20, 10))
    close_btn = pygame.Rect(W-60, 8, 45, 28)
    pygame.draw.rect(surf, (90,90,110), close_btn, border_radius=6)
    f = pygame.font.SysFont("Arial", 16, bold=True)
    surf.blit(f.render("X", True, (255,255,255)), (close_btn.centerx-5, close_btn.centery-8))
    coins = wallet.data.get('coins',0)
    usd = coins * COIN_TO_USD
    card = pygame.Rect(10, 42, W-20, 38)
    pygame.draw.rect(surf, (30,42,95), card, border_radius=8)
    surf.blit(f.render(f"Coins: {coins} = ${usd:.3f}", True, (255,230,80)), (card.x+8, card.y+8))
    btns = {}
    labels = ["Profile","Withdraw","History","Referrals"]
    for i, label in enumerate(labels):
        r = pygame.Rect(10 + (i%2)*(W//2), 88 + (i//2)*38, W//2 - 14, 32)
        pygame.draw.rect(surf, (42,52,102), r, border_radius=8)
        surf.blit(f.render(label, True, (255,255,255)), (r.x+8, r.y+7))
        btns[label.lower()] = r
    pygame.draw.rect(surf, (22,30,75), pygame.Rect(10, 170, W-20, H-190), border_radius=10)
    return btns, close_btn, 170

def open_wallet(screen, wallet, W=None, H=None):
    if W is None: W,H = screen.get_size()
    wd_system = WithdrawSystem(wallet)
    ref_system = ReferralSystem(wallet)
    current_tab = "profile"
    method_idx = 1
    saved = wallet.data.get('saved_accounts', {})
    name_text = saved.get('JazzCash',{}).get('name','')
    number_text = saved.get('JazzCash',{}).get('number','')
    usdt_text = saved.get('USDT',{}).get('address','')
    ref_input_text = ""
    active = ""
    message = f"Min {MIN_WITHDRAW} coins = $1"
    clock = pygame.time.Clock()
    pygame.key.start_text_input()
    acc = wd_system.get_saved_account("JazzCash")
    name_text = acc.get('name','')
    number_text = acc.get('number','')
    logout_rect = pygame.Rect(0,0,0,0)
    running = True
    while running:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.key.stop_text_input()
                return
            if e.type == pygame.TEXTINPUT:
                if active == "name" and len(name_text) < 30: name_text += e.text
                elif active == "number" and len(number_text) < 15:
                    if e.text.isdigit() or e.text in "+": number_text += e.text
                elif active == "usdt" and len(usdt_text) < 60: usdt_text += e.text
                elif active == "ref" and len(ref_input_text) < 15: ref_input_text += e.text
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_BACKSPACE:
                    if active == "name": name_text = name_text[:-1]
                    elif active == "number": number_text = number_text[:-1]
                    elif active == "usdt": usdt_text = usdt_text[:-1]
                    elif active == "ref": ref_input_text = ref_input_text[:-1]
                elif e.key == pygame.K_RETURN:
                    active = ""
                    pygame.key.stop_text_input()
                    pygame.key.start_text_input()
            if e.type == pygame.MOUSEBUTTONDOWN:
                mx,my = e.pos
                btns, close_btn, top = draw_wallet_page(screen, wallet, W, H)
                if close_btn.collidepoint(mx,my):
                    pygame.key.stop_text_input()
                    return
                if current_tab == "profile" and logout_rect.collidepoint(mx,my):
                    pygame.key.stop_text_input()
                    return "logout"
                for k,r in btns.items():
                    if r.collidepoint(mx,my):
                        current_tab = k
                        active = ""
                        message = ""
                if current_tab == "withdraw":
                    for i in range(3):
                        r = pygame.Rect(15 + i*110, top+5, 100, 28)
                        if r.collidepoint(mx,my):
                            method_idx = i
                            m = METHODS[method_idx]
                            acc = wd_system.get_saved_account(m)
                            if m == "USDT":
                                usdt_text = acc.get('address','')
                                active = "usdt"
                            else:
                                name_text = acc.get('name','')
                                number_text = acc.get('number','')
                                active = "name"
                            pygame.key.set_text_input_rect(pygame.Rect(15, top+40, W-40, 36))
                            pygame.key.start_text_input()
                    m = METHODS[method_idx]
                    if m == "USDT":
                        inp = pygame.Rect(15, top+40, W-40, 40)
                        if inp.collidepoint(mx,my):
                            active = "usdt"
                            pygame.key.set_text_input_rect(inp)
                            pygame.key.start_text_input()
                            message = "Mobile keyboard se USDT likho"
                        save_btn = pygame.Rect(15, top+90, 130, 40)
                        wd_btn = pygame.Rect(155, top+90, 160, 40)
                        if save_btn.collidepoint(mx,my):
                            wd_system.save_account("USDT", address=usdt_text)
                            message = "USDT SAVED! ✓"
                            active = ""
                            pygame.key.stop_text_input()
                        elif wd_btn.collidepoint(mx,my):
                            ok, msg = wd_system.withdraw("USDT", address=usdt_text)
                            message = msg
                            active = ""
                            pygame.key.stop_text_input()
                    else:
                        inp1 = pygame.Rect(15, top+40, W-40, 40)
                        inp2 = pygame.Rect(15, top+90, W-40, 40)
                        if inp1.collidepoint(mx,my):
                            active = "name"
                            pygame.key.set_text_input_rect(inp1)
                            pygame.key.start_text_input()
                            message = "Mobile keyboard se Name likho"
                        elif inp2.collidepoint(mx,my):
                            active = "number"
                            pygame.key.set_text_input_rect(inp2)
                            pygame.key.start_text_input()
                            message = "Mobile keyboard se Number likho"
                        else:
                            save_btn = pygame.Rect(15, top+140, 130, 40)
                            wd_btn = pygame.Rect(155, top+140, 160, 40)
                            if save_btn.collidepoint(mx,my):
                                wd_system.save_account(m, name=name_text, number=number_text)
                                message = f"{m} SAVED! ✓"
                                active = ""
                                pygame.key.stop_text_input()
                            elif wd_btn.collidepoint(mx,my):
                                ok, msg = wd_system.withdraw(m, name=name_text, number=number_text)
                                message = msg
                                active = ""
                                pygame.key.stop_text_input()
                elif current_tab == "referrals":
                    inp_ref = pygame.Rect(15, top+50, W-40, 40)
                    apply_btn = pygame.Rect(15, top+100, W-40, 40)
                    if inp_ref.collidepoint(mx,my):
                        active = "ref"
                        pygame.key.set_text_input_rect(inp_ref)
                        pygame.key.start_text_input()
                        message = "Paste referral code here"
                    elif apply_btn.collidepoint(mx,my):
                        if ref_input_text.strip() == "":
                            message = "Enter code first!"
                        else:
                            ok, msg = ref_system.apply_code(ref_input_text.strip())
                            message = msg
                            if ok:
                                ref_input_text = ""
                                active = ""
                                pygame.key.stop_text_input()
        btns, close_btn, top = draw_wallet_page(screen, wallet, W, H)
        font = pygame.font.SysFont("Arial", 16, bold=True)
        small = pygame.font.SysFont("Arial", 12)
        x = 15
        if current_tab == "withdraw":
            for i,m in enumerate(METHODS):
                r = pygame.Rect(x + i*110, top+5, 100, 28)
                sel = (i == method_idx)
                pygame.draw.rect(screen, (0,230,255) if sel else (60,70,120), r, border_radius=6)
                c = (0,0,0) if sel else (255,255,255)
                screen.blit(small.render(m, True, c), (r.x+20, r.y+7))
            m = METHODS[method_idx]
            if m == "USDT":
                inp = pygame.Rect(x, top+40, W-40, 40)
                pygame.draw.rect(screen, (40,50,100), inp, border_radius=6)
                pygame.draw.rect(screen, (0,230,255) if active=="usdt" else (80,80,100), inp, width=2, border_radius=6)
                txt = usdt_text if usdt_text else "Tap here - mobile keyboard"
                col = (255,255,255) if usdt_text else (130,130,150)
                screen.blit(font.render(txt[-28:], True, col), (inp.x+6, inp.y+10))
                save_btn = pygame.Rect(x, top+90, 130, 40)
                wd_btn = pygame.Rect(x+140, top+90, 160, 40)
                pygame.draw.rect(screen, (80,90,200), save_btn, border_radius=8)
                pygame.draw.rect(screen, (0,230,255), wd_btn, border_radius=8)
                screen.blit(font.render("SAVE", True, (255,255,255)), (save_btn.x+35, save_btn.y+10))
                screen.blit(font.render(f"WITHDRAW $1", True, (0,0,0)), (wd_btn.x+20, wd_btn.y+10))
            else:
                inp1 = pygame.Rect(x, top+40, W-40, 40)
                pygame.draw.rect(screen, (40,50,100), inp1, border_radius=6)
                pygame.draw.rect(screen, (0,230,255) if active=="name" else (80,80,100), inp1, width=2, border_radius=6)
                txt1 = name_text if name_text else "Tap - Name"
                col1 = (255,255,255) if name_text else (130,130,150)
                screen.blit(font.render(txt1, True, col1), (inp1.x+6, inp1.y+10))
                inp2 = pygame.Rect(x, top+90, W-40, 40)
                pygame.draw.rect(screen, (40,50,100), inp2, border_radius=6)
                pygame.draw.rect(screen, (0,230,255) if active=="number" else (80,80,100), inp2, width=2, border_radius=6)
                txt2 = number_text if number_text else "Tap - Number"
                col2 = (255,255,255) if number_text else (130,130,150)
                screen.blit(font.render(txt2, True, col2), (inp2.x+6, inp2.y+10))
                save_btn = pygame.Rect(x, top+140, 130, 40)
                wd_btn = pygame.Rect(x+140, top+140, 160, 40)
                pygame.draw.rect(screen, (80,90,200), save_btn, border_radius=8)
                pygame.draw.rect(screen, (0,230,255), wd_btn, border_radius=8)
                screen.blit(font.render("SAVE", True, (255,255,255)), (save_btn.x+35, save_btn.y+10))
                screen.blit(font.render("WITHDRAW $1", True, (0,0,0)), (wd_btn.x+20, wd_btn.y+10))
            coins = wallet.data.get('coins',0)
            prog = min(1.0, coins / MIN_WITHDRAW)
            bar_bg = pygame.Rect(x, top+190, W-30, 10)
            bar_fg = pygame.Rect(x, top+190, int((W-30)*prog), 10)
            pygame.draw.rect(screen, (60,60,80), bar_bg, border_radius=5)
            pygame.draw.rect(screen, (0,255,130), bar_fg, border_radius=5)
            if message: screen.blit(small.render(message, True, (0,255,130)), (x, top+210))
            screen.blit(small.render(f"Progress: {coins}/{MIN_WITHDRAW} = ${coins*COIN_TO_USD:.3f} / $1.00", True, (200,200,200)), (x, top+225))
        elif current_tab == "profile":
            real_name = get_user_display_name()
            real_email = wallet.data.get('email','') or get_current_user() or ""
            big_font = pygame.font.SysFont("Arial", 22, bold=True)
            pygame.draw.rect(screen, (35,45,90), pygame.Rect(x, top+10, W-30, 90), border_radius=12)
            screen.blit(big_font.render(f"{real_name}", True, (255,215,0)), (x+15, top+20))
            screen.blit(font.render(f"My Code: {wallet.data.get('referral_code','')}", True, (255,230,80)), (x+15, top+50))
            screen.blit(small.render(f"Email: {real_email}", True, (200,200,200)), (x+15, top+75))
            logout_rect = pygame.Rect(x, top+110, W-30, 45)
            pygame.draw.rect(screen, (255, 80, 80), logout_rect, border_radius=10)
            screen.blit(font.render("LOGOUT", True, (255,255,255)), (logout_rect.centerx-30, logout_rect.y+12))
        elif current_tab == "history":
            hist = wallet.data.get('withdraw_history',[])
            yy = top+10
            for h in hist[:8]:
                screen.blit(small.render(f"{h['time']} {h['method']} {h['status']}", True, (255,255,255)), (x, yy)); yy+=15
                screen.blit(small.render(f" {h['account'][:30]}", True, (180,180,200)), (x, yy)); yy+=15
        elif current_tab == "referrals":
            my_code = wallet.data.get('referral_code','NOCODE')
            screen.blit(font.render(f"My Code: {my_code}", True, (255,230,80)), (x, top+10))
            screen.blit(small.render("Share code, get 5 coins per Ad! - 300% Profit", True, (200,200,200)), (x, top+30))
            inp_ref = pygame.Rect(x, top+50, W-40, 40)
            pygame.draw.rect(screen, (40,50,100), inp_ref, border_radius=6)
            pygame.draw.rect(screen, (0,230,255) if active=="ref" else (80,80,100), inp_ref, width=2, border_radius=6)
            txt_show = ref_input_text if ref_input_text else "Tap - Paste Code Here"
            col = (255,255,255) if ref_input_text else (130,130,150)
            screen.blit(font.render(txt_show, True, col), (inp_ref.x+6, inp_ref.y+10))
            apply_btn = pygame.Rect(x, top+100, W-40, 40)
            pygame.draw.rect(screen, (0,230,255), apply_btn, border_radius=8)
            screen.blit(font.render("APPLY CODE", True, (0,0,0)), (apply_btn.x+70, apply_btn.y+10))
            yy = top+150
            screen.blit(small.render(f"Referred: {len(wallet.data.get('referrals',[]))}", True, (200,200,200)), (x, yy)); yy+=18
            refs = wallet.data.get('referrals', [])
            if not refs:
                screen.blit(small.render("No referrals yet - Share your code", True, (150,150,150)), (x, yy))
            else:
                for r in refs[:6]:
                    screen.blit(small.render(f"- {r.get('code','')} +{r.get('coins',0)}C", True, (255,255,255)), (x, yy)); yy+=15
            if message: screen.blit(small.render(message, True, (0,255,130)), (x, top+230))
        pygame.display.flip()
        clock.tick(60)