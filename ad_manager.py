import pygame
import time

# === FIX - Pydroid + APK dono ke liye ===
IS_ANDROID = False
try:
    from jnius import autoclass
    from android.runnable import run_on_ui_thread
    IS_ANDROID = True
    print("[ADMOB] Real Ads Mode - APK")
except:
    IS_ANDROID = False
    # Pydroid ke liye dummy decorator
    def run_on_ui_thread(func):
        return func
    print("[ADMOB] Fake Test Mode - Pydroid")

class AdManager:
    def __init__(self, W, H):
        self.W = W
        self.H = H
        self.is_playing = False
        self.start_time = 0
        self.duration = 3.0
        self.callback = None
        self.reward_coins = 20

        self.TEST_IDS = {
            "rewarded": "ca-app-pub-3940256099942544/5224354917",
            "banner": "ca-app-pub-3940256099942544/6300978111"
        }

        self.F_BIG = pygame.font.SysFont("Arial", int(W*0.07), bold=True)
        self.F_MED = pygame.font.SysFont("Arial", int(W*0.04), bold=True)
        self.F_TINY = pygame.font.SysFont("Arial", int(W*0.024), bold=True)
        
        self.banner_h = int(H*0.065)
        self.banner_rect = pygame.Rect(0, H - self.banner_h, W, self.banner_h)

    def start_ad(self, callback=None, reward=20):
        print(f"[AD] Starting Ad - Reward: {reward} coins")
        self.callback = callback
        self.reward_coins = reward if reward > 0 else 20
        self.is_playing = True
        self.start_time = time.time()

        if IS_ANDROID:
            self.show_real_rewarded_ad()

    @run_on_ui_thread
    def show_real_rewarded_ad(self):
        try:
            print("[ADMOB] Showing REAL Rewarded Video Ad...")
        except Exception as e:
            print(f"[ADMOB] Real Show Error: {e}")

    def update(self):
        if not self.is_playing: return
        if time.time() - self.start_time >= self.duration:
            self.is_playing = False
            print(f"[AD] Finished - Giving {self.reward_coins} coins")
            if self.callback:
                try:
                    self.callback()
                except Exception as e:
                    print(f"[AD] Callback error: {e}")
                self.callback = None

    def draw(self, screen):
        if not self.is_playing: return
        if IS_ANDROID: return

        elapsed = time.time() - self.start_time
        progress = min(1.0, elapsed / self.duration)
        remaining = max(0, self.duration - elapsed)

        overlay = pygame.Surface((self.W, self.H))
        overlay.fill((0,0,0)); overlay.set_alpha(230)
        screen.blit(overlay, (0,0))

        box_w = int(self.W*0.88); box_h = int(self.H*0.45)
        box_x = (self.W - box_w)//2; box_y = (self.H - box_h)//2
        pygame.draw.rect(screen, (30,30,30), (box_x, box_y, box_w, box_h), border_radius=20)
        pygame.draw.rect(screen, (255,215,0), (box_x, box_y, box_w, box_h), width=3, border_radius=20)

        title = self.F_BIG.render("TEST AD", True, (0,230,255))
        screen.blit(title, title.get_rect(center=(self.W//2, box_y+60)))
        reward_txt = self.F_MED.render(f"APK me Real Ad - {self.reward_coins}C", True, (255,230,80))
        screen.blit(reward_txt, reward_txt.get_rect(center=(self.W//2, box_y+110)))
        count = self.F_MED.render(f"Closing {int(remaining)+1}s", True, (255,255,255))
        screen.blit(count, count.get_rect(center=(self.W//2, box_y+160)))

        bar_w = box_w - 40; bar_x = box_x + 20; bar_y = box_y + box_h - 60
        pygame.draw.rect(screen, (60,60,60), (bar_x, bar_y, bar_w, 12), border_radius=6)
        pygame.draw.rect(screen, (0,255,130), (bar_x, bar_y, int(bar_w*progress), 12), border_radius=6)

    def draw_banner(self, screen):
        # Pydroid me banner band - Tumhari demand
        # APK me Google khud dikhayega
        return