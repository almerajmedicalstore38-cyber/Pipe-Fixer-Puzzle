import pygame, os, math, struct
click_sound=flow_sound=flow_channel=None
is_muted=False
def load(muted):
    global click_sound, flow_sound, is_muted
    is_muted=muted
    try:
        if os.path.exists("assets/click.mp3"): click_sound=pygame.mixer.Sound("assets/click.mp3")
        else:
            sr=44100; n=int(sr*0.06); buf=bytearray()
            for i in range(n):
                v=int(32767*0.3*math.sin(2*math.pi*800*i/sr)*(1-i/n))
                buf+=struct.pack('<h',v)*2
            click_sound=pygame.mixer.Sound(buffer=bytes(buf))
    except: pass
    try:
        if os.path.exists("assets/flow.mp3"): flow_sound=pygame.mixer.Sound("assets/flow.mp3")
        elif os.path.exists("assets/water.mp3"): flow_sound=pygame.mixer.Sound("assets/water.mp3")
        if flow_sound: flow_sound.set_volume(0.6)
        if os.path.exists("assets/bg_music.mp3"):
            pygame.mixer.music.load("assets/bg_music.mp3")
            pygame.mixer.music.set_volume(0.30)
            pygame.mixer.music.play(-1)
            if is_muted: pygame.mixer.music.pause()
    except: pass
def play_click():
    if not is_muted and click_sound:
        try: click_sound.play()
        except: pass
def play_flow():
    global flow_channel
    if is_muted or not flow_sound: return
    try: pygame.mixer.music.pause(); flow_channel=flow_sound.play(-1)
    except: pass
def stop_flow():
    global flow_channel
    try:
        if flow_channel: flow_channel.stop(); flow_channel=None
        if flow_sound: flow_sound.stop()
        if not is_muted: pygame.mixer.music.unpause()
    except: pass