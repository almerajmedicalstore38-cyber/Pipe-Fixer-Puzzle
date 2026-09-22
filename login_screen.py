# login_screen.py - STABLE ANDROID SAFE VERSION - BY SHTEDITOR
import pygame
from auth_manager import signup_user, login_user, forgot_password

# === 1. KEYBOARD SAFE WRAPPER ===
IS_ANDROID = False
try:
    from jnius import autoclass
    from android.runnable import run_on_ui_thread
    IS_ANDROID = True
except Exception:
    IS_ANDROID = False
    def run_on_ui_thread(f): return f

@run_on_ui_thread
def show_keyboard():
    if not IS_ANDROID: return
    try:
        PythonActivity = autoclass('org.kivy.android.PythonActivity')
        activity = PythonActivity.mActivity
        Context = autoclass('android.content.Context')
        InputMethodManager = autoclass('android.view.inputmethod.InputMethodManager')
        imm = activity.getSystemService(Context.INPUT_METHOD_SERVICE)
        imm.toggleSoftInput(InputMethodManager.SHOW_FORCED, 0)
    except Exception as ex:
        print(f"[KEYBOARD SHOW ERR] {ex}")

@run_on_ui_thread
def hide_keyboard():
    if not IS_ANDROID: return
    try:
        PythonActivity = autoclass('org.kivy.android.PythonActivity')
        activity = PythonActivity.mActivity
        Context = autoclass('android.content.Context')
        InputMethodManager = autoclass('android.view.inputmethod.InputMethodManager')
        imm = activity.getSystemService(Context.INPUT_METHOD_SERVICE)
        v = activity.getCurrentFocus()
        if v: imm.hideSoftInputFromWindow(v.getWindowToken(), 0)
    except Exception as ex:
        print(f"[KEYBOARD HIDE ERR] {ex}")

# === 2. NO INTERNET FIX ===
def get_friendly_error(msg):
    s = str(msg).lower()
    if "nameresolution" in s or "failed to resolve" in s or "getaddrinfo" in s or "name or service" in s:
        return "No Internet! Turn On Data"
    if "connection" in s or "network" in s or "timeout" in s or "unreachable" in s:
        return "No Internet! Check Connection"
    return str(msg)

def show_auth_screen(screen, W, H, config):
    pygame.font.init()
    try:
        pygame.key.start_text_input()
    except Exception:
        pass

    # Android Safe System Fonts (Avoids SysFont Search Freeze)
    font_big = pygame.font.Font(None, 44)
    font_mid = pygame.font.Font(None, 30)
    font_small = pygame.font.Font(None, 24)
    font_tiny = pygame.font.Font(None, 20)

    name = ""
    email = ""
    password = ""
    active_field = "name"
    mode = "signup"
    message = "Apna Naam Likho"
    message_color = (255, 255, 255)

    # Screen Bounds safe calculations
    box_w = min(int(W * 0.85), 550)
    box_x = (W - box_w) // 2
    box_h = 50

    name_rect = pygame.Rect(box_x, int(H * 0.38), box_w, box_h)
    email_rect = pygame.Rect(box_x, int(H * 0.46), box_w, box_h)
    pass_rect = pygame.Rect(box_x, int(H * 0.54), box_w, box_h)

    btn_w = (box_w - 15) // 2
    login_btn = pygame.Rect(box_x, int(H * 0.63), btn_w, box_h)
    signup_btn = pygame.Rect(box_x + btn_w + 15, int(H * 0.63), btn_w, box_h)
    forgot_btn = pygame.Rect(box_x, int(H * 0.72), box_w, 38)

    guest_btn = pygame.Rect(box_x, int(H * 0.78), box_w, 42)

    clock = pygame.time.Clock()
    
    show_keyboard()

    while True:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                exit()
            if e.type == pygame.MOUSEBUTTONDOWN:
                pos = e.pos
                if mode == "signup" and name_rect.collidepoint(pos):
                    active_field = "name"
                    show_keyboard()
                elif email_rect.collidepoint(pos):
                    active_field = "email"
                    show_keyboard()
                elif pass_rect.collidepoint(pos):
                    active_field = "password"
                    show_keyboard()
                elif guest_btn.collidepoint(pos):
                    hide_keyboard()
                    return "guest_user@app.com"
                elif login_btn.collidepoint(pos):
                    if mode == "login":
                        try:
                            ok, msg = login_user(email, password)
                            message = get_friendly_error(msg)
                            message_color = (0, 255, 130) if ok else (255, 80, 80)
                            if ok:
                                pygame.time.wait(300)
                                hide_keyboard()
                                return email
                        except Exception as ex:
                            message = get_friendly_error(ex)
                            message_color = (255, 80, 80)
                    else:
                        mode = "login"
                        message = "Login karo"
                        active_field = "email"
                        show_keyboard()
                elif signup_btn.collidepoint(pos):
                    if mode == "signup":
                        if len(name) < 2:
                            message = "Naam 2 harf se zyada likho"
                            message_color = (255, 80, 80)
                        else:
                            try:
                                ok, msg = signup_user(email, password, name)
                                message = get_friendly_error(msg)
                                message_color = (0, 255, 130) if ok else (255, 80, 80)
                                if ok:
                                    pygame.time.wait(300)
                                    hide_keyboard()
                                    return email
                            except Exception as ex:
                                message = get_friendly_error(ex)
                                message_color = (255, 80, 80)
                    else:
                        mode = "signup"
                        message = "Naya account banao"
                        active_field = "name"
                        show_keyboard()
                elif forgot_btn.collidepoint(pos):
                    try:
                        ok, msg = forgot_password(email)
                        message = get_friendly_error(msg)
                        message_color = (0, 255, 130) if ok else (255, 80, 80)
                    except Exception as ex:
                        message = get_friendly_error(ex)
                        message_color = (255, 80, 80)
            
            if e.type == pygame.TEXTINPUT:
                if active_field == "name" and len(name) < 20:
                    name += e.text
                elif active_field == "email" and len(email) < 40:
                    email += e.text
                elif active_field == "password" and len(password) < 20:
                    password += e.text
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_BACKSPACE:
                    if active_field == "name":
                        name = name[:-1]
                    elif active_field == "email":
                        email = email[:-1]
                    else:
                        password = password[:-1]
                elif e.key == pygame.K_TAB:
                    if mode == "signup":
                        active_field = "email" if active_field == "name" else ("password" if active_field == "email" else "name")
                    else:
                        active_field = "password" if active_field == "email" else "email"

        screen.fill((10, 20, 50))
        app_title = getattr(config, 'APP_NAME', 'PIPE CONNECT')
        app_dev = getattr(config, 'APP_DEV', 'SHTEDITOR')

        title = font_big.render(app_title, True, (255, 215, 0))
        screen.blit(title, title.get_rect(center=(W//2, int(H * 0.15))))
        dev = font_tiny.render(f"BY {app_dev}", True, (0, 230, 255))
        screen.blit(dev, dev.get_rect(center=(W//2, int(H * 0.20))))

        mode_text = font_mid.render("LOGIN" if mode == "login" else "SIGN UP", True, (255, 255, 255))
        screen.blit(mode_text, mode_text.get_rect(center=(W//2, int(H * 0.28))))

        if mode == "signup":
            pygame.draw.rect(screen, (0, 230, 255) if active_field == "name" else (255,255,255), name_rect, 2, border_radius=12)
            n_txt = font_mid.render(name if name else "Your Full Name", True, (255,255,255) if name else (150,150,150))
            screen.blit(n_txt, (name_rect.x + 15, name_rect.y + 12))

        pygame.draw.rect(screen, (0, 230, 255) if active_field == "email" else (255,255,255), email_rect, 2, border_radius=12)
        pygame.draw.rect(screen, (0, 230, 255) if active_field == "password" else (255,255,255), pass_rect, 2, border_radius=12)

        e_txt = font_mid.render(email if email else "Email", True, (255,255,255) if email else (150,150,150))
        p_txt = font_mid.render("*"*len(password) if password else "Password (6+ chars)", True, (255,255,255) if password else (150,150,150))
        screen.blit(e_txt, (email_rect.x + 15, email_rect.y + 12))
        screen.blit(p_txt, (pass_rect.x + 15, pass_rect.y + 12))

        pygame.draw.rect(screen, (0, 255, 130), login_btn, border_radius=12)
        pygame.draw.rect(screen, (255, 215, 0), signup_btn, border_radius=12)
        pygame.draw.rect(screen, (80, 90, 115), guest_btn, border_radius=12)

        l_txt = font_mid.render("LOGIN" if mode == "login" else "BACK TO LOGIN", True, (0,0,0))
        s_txt = font_mid.render("SIGN UP" if mode == "signup" else "CREATE ACCOUNT", True, (0,0,0))
        g_txt = font_small.render("PLAY AS GUEST (SKIP LOGIN)", True, (255, 255, 255))

        screen.blit(l_txt, l_txt.get_rect(center=login_btn.center))
        screen.blit(s_txt, s_txt.get_rect(center=signup_btn.center))
        screen.blit(g_txt, g_txt.get_rect(center=guest_btn.center))

        f_txt = font_small.render("Forgot Password? Click Here", True, (100, 180, 255))
        screen.blit(f_txt, f_txt.get_rect(center=forgot_btn.center))

        m_txt = font_small.render(message, True, message_color)
        screen.blit(m_txt, m_txt.get_rect(center=(W//2, int(H * 0.85))))

        pygame.display.flip()
        clock.tick(60)
