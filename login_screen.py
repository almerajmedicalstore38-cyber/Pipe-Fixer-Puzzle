# login_screen.py - FINAL WITH NAME - KEYBOARD + NO INTERNET FIX - SHTEDITOR
import pygame
from auth_manager import signup_user, login_user, forgot_password

# === 1. KEYBOARD FIX FOR ANDROID ===
IS_ANDROID = False
try:
    from jnius import autoclass
    from android.runnable import run_on_ui_thread
    IS_ANDROID = True
except:
    IS_ANDROID = False
    def run_on_ui_thread(f): return f

@run_on_ui_thread
def show_keyboard():
    try:
        if not IS_ANDROID: return
        PythonActivity = autoclass('org.kivy.android.PythonActivity')
        activity = PythonActivity.mActivity
        Context = autoclass('android.content.Context')
        InputMethodManager = autoclass('android.view.inputmethod.InputMethodManager')
        imm = activity.getSystemService(Context.INPUT_METHOD_SERVICE)
        imm.toggleSoftInput(InputMethodManager.SHOW_FORCED, 0)
    except: pass

@run_on_ui_thread
def hide_keyboard():
    try:
        if not IS_ANDROID: return
        PythonActivity = autoclass('org.kivy.android.PythonActivity')
        activity = PythonActivity.mActivity
        Context = autoclass('android.content.Context')
        InputMethodManager = autoclass('android.view.inputmethod.InputMethodManager')
        imm = activity.getSystemService(Context.INPUT_METHOD_SERVICE)
        v = activity.getCurrentFocus()
        if v: imm.hideSoftInputFromWindow(v.getWindowToken(), 0)
    except: pass

# === 2. NO INTERNET FIX ===
def get_friendly_error(msg):
    s = str(msg).lower()
    if "nameresolution" in s or "failed to resolve" in s or "getaddrinfo" in s or "name or service" in s or "name resolution" in s:
        return "No Internet! Please Turn On Data"
    if "connection" in s or "network" in s or "timeout" in s or "unreachable" in s or "unable to" in s:
        return "No Internet! Check Connection"
    return msg  # Agar sahi message hai to waise hi dikhao

def show_auth_screen(screen, W, H, config):
    pygame.font.init()
    pygame.key.start_text_input()

    font_big = pygame.font.SysFont("Arial", 42, bold=True)
    font_mid = pygame.font.SysFont("Arial", 26, bold=True)
    font_small = pygame.font.SysFont("Arial", 22)
    font_tiny = pygame.font.SysFont("Arial", 18)

    name = ""
    email = ""
    password = ""
    active_field = "name"
    mode = "signup"
    message = "Apna Naam Likho"
    message_color = (255, 255, 255)

    name_rect = pygame.Rect(W//2 - 300, H//2 - 140, 600, 55)
    email_rect = pygame.Rect(W//2 - 300, H//2 - 70, 600, 55)
    pass_rect = pygame.Rect(W//2 - 300, H//2 + 0, 600, 55)
    login_btn = pygame.Rect(W//2 - 300, H//2 + 80, 290, 55)
    signup_btn = pygame.Rect(W//2 + 10, H//2 + 80, 290, 55)
    forgot_btn = pygame.Rect(W//2 - 150, H//2 + 150, 300, 40)

    clock = pygame.time.Clock()
    
    # First time keyboard kholo
    show_keyboard()
    pygame.key.set_text_input_rect(name_rect)

    while True:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                exit()
            if e.type == pygame.MOUSEBUTTONDOWN:
                if name_rect.collidepoint(e.pos) and mode == "signup":
                    active_field = "name"
                    pygame.key.set_text_input_rect(name_rect)
                    show_keyboard()  # <-- FIX: Keyboard dobara kholo
                elif email_rect.collidepoint(e.pos):
                    active_field = "email"
                    pygame.key.set_text_input_rect(email_rect)
                    show_keyboard()  # <-- FIX
                elif pass_rect.collidepoint(e.pos):
                    active_field = "password"
                    pygame.key.set_text_input_rect(pass_rect)
                    show_keyboard()  # <-- FIX
                elif login_btn.collidepoint(e.pos):
                    if mode == "login":
                        try:
                            ok, msg = login_user(email, password)
                            message = get_friendly_error(msg)
                            message_color = (0, 255, 130) if ok else (255, 80, 80)
                            if ok:
                                pygame.time.wait(600)
                                pygame.key.stop_text_input()
                                hide_keyboard()
                                return email
                        except Exception as ex:
                            message = get_friendly_error(ex)
                            message_color = (255, 80, 80)
                            show_keyboard()
                    else:
                        mode = "login"
                        message = "Login karo"
                        active_field = "email"
                        pygame.key.set_text_input_rect(email_rect)
                        show_keyboard()
                elif signup_btn.collidepoint(e.pos):
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
                                    pygame.time.wait(600)
                                    pygame.key.stop_text_input()
                                    hide_keyboard()
                                    return email
                            except Exception as ex:
                                message = get_friendly_error(ex)
                                message_color = (255, 80, 80)
                                show_keyboard()
                    else:
                        mode = "signup"
                        message = "Naya account banao"
                        active_field = "name"
                        pygame.key.set_text_input_rect(name_rect)
                        show_keyboard()
                elif forgot_btn.collidepoint(e.pos):
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
                        if active_field == "name":
                            active_field = "email"
                            pygame.key.set_text_input_rect(email_rect)
                            show_keyboard()
                        elif active_field == "email":
                            active_field = "password"
                            pygame.key.set_text_input_rect(pass_rect)
                            show_keyboard()
                        else:
                            active_field = "name"
                            pygame.key.set_text_input_rect(name_rect)
                            show_keyboard()
                    else:
                        if active_field == "email":
                            active_field = "password"
                            pygame.key.set_text_input_rect(pass_rect)
                            show_keyboard()
                        else:
                            active_field = "email"
                            pygame.key.set_text_input_rect(email_rect)
                            show_keyboard()

        screen.fill((10, 20, 50))
        title = font_big.render(config.APP_NAME, True, (255, 215, 0))
        screen.blit(title, title.get_rect(center=(W//2, H//2 - 270)))
        dev = font_tiny.render(f"BY {config.APP_DEV}", True, (0, 230, 255))
        screen.blit(dev, dev.get_rect(center=(W//2, H//2 - 235)))
        mode_text = font_mid.render("LOGIN" if mode == "login" else "SIGN UP", True, (255, 255, 255))
        screen.blit(mode_text, mode_text.get_rect(center=(W//2, H//2 - 200)))

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
        l_txt = font_mid.render("LOGIN" if mode == "login" else "BACK TO LOGIN", True, (0,0,0))
        s_txt = font_mid.render("SIGN UP" if mode == "signup" else "CREATE ACCOUNT", True, (0,0,0))
        screen.blit(l_txt, l_txt.get_rect(center=login_btn.center))
        screen.blit(s_txt, s_txt.get_rect(center=signup_btn.center))

        f_txt = font_small.render("Forgot Password? Click Here", True, (100, 180, 255))
        screen.blit(f_txt, f_txt.get_rect(center=forgot_btn.center))

        m_txt = font_small.render(message, True, message_color)
        screen.blit(m_txt, m_txt.get_rect(center=(W//2, H//2 + 200)))

        pygame.display.flip()
        clock.tick(60)