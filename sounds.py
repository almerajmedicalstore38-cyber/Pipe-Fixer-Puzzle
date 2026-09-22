import pygame, os, math, struct

click_sound = flow_sound = flow_channel = None
is_muted = False

# Base directory for absolute Android asset paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def get_asset_path(filename):
    return os.path.join(BASE_DIR, "assets", filename)

def load(muted):
    global click_sound, flow_sound, is_muted
    is_muted = muted

    # 1. Click Sound Load (with Synthetic Fallback)
    try:
        click_path = get_asset_path("click.mp3")
        if os.path.exists(click_path):
            click_sound = pygame.mixer.Sound(click_path)
        else:
            sr = 44100
            n = int(sr * 0.06)
            buf = bytearray()
            for i in range(n):
                v = int(32767 * 0.3 * math.sin(2 * math.pi * 800 * i / sr) * (1 - i / n))
                buf += struct.pack('<h', v) * 2
            click_sound = pygame.mixer.Sound(buffer=bytes(buf))
    except Exception as e:
        print(f"[SOUND LOG] Click sound load skipped: {e}")

    # 2. Flow Sound Load
    try:
        flow_path = get_asset_path("flow.mp3")
        water_path = get_asset_path("water.mp3")

        if os.path.exists(flow_path):
            flow_sound = pygame.mixer.Sound(flow_path)
        elif os.path.exists(water_path):
            flow_sound = pygame.mixer.Sound(water_path)

        if flow_sound:
            flow_sound.set_volume(0.6)
    except Exception as e:
        print(f"[SOUND LOG] Flow sound load skipped: {e}")

    # 3. Background Music Load (Safe)
    try:
        bg_path = get_asset_path("bg_music.mp3")
        if os.path.exists(bg_path):
            pygame.mixer.music.load(bg_path)
            pygame.mixer.music.set_volume(0.30)
            pygame.mixer.music.play(-1)
            if is_muted:
                pygame.mixer.music.pause()
    except Exception as e:
        print(f"[SOUND LOG] BG Music load skipped: {e}")

def play_click():
    if not is_muted and click_sound:
        try:
            click_sound.play()
        except:
            pass

def play_flow():
    global flow_channel
    if is_muted or not flow_sound:
        return
    try:
        if pygame.mixer.music.get_busy():
            pygame.mixer.music.pause()
        flow_channel = flow_sound.play(-1)
    except:
        pass

def stop_flow():
    global flow_channel
    try:
        if flow_channel:
            flow_channel.stop()
            flow_channel = None
        if flow_sound:
            flow_sound.stop()
        if not is_muted and not pygame.mixer.music.get_busy():
            pygame.mixer.music.unpause()
    except:
        pass
