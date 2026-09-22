import pygame
import time
from admob_bridge import init_admob, load_and_show_rewarded_ad, IS_ANDROID

class AdManager:
    def __init__(self, W, H):
        self.W = W
        self.H = H
        self.is_playing = False
        self.callback = None
        self.reward_coins = 20

        init_admob()

        self.F_BIG = pygame.font.Font(None, int(W * 0.07))
        self.F_MED = pygame.font.Font(None, int(W * 0.05))

    def start_ad(self, callback=None, reward=20):
        self.callback = callback
        self.reward_coins = reward if reward > 0 else 20

        def on_reward_verified():
            if self.callback:
                try:
                    self.callback()
                except Exception as e:
                    print(f"[AD CALLBACK ERROR] {e}")
                self.callback = None

        if IS_ANDROID:
            load_and_show_rewarded_ad(on_reward_verified)
        else:
            self.is_playing = True
            self.start_time = time.time()

    def update(self):
        if not self.is_playing:
            return
        
        if time.time() - self.start_time >= 5.0:
            self.is_playing = False
            if self.callback:
                self.callback()
                self.callback = None

    def draw(self, screen):
        if not self.is_playing:
            return

        overlay = pygame.Surface((self.W, self.H))
        overlay.fill((0, 0, 0))
        overlay.set_alpha(235)
        screen.blit(overlay, (0, 0))

        title = self.F_BIG.render("LOADING REAL TEST AD...", True, (0, 230, 255))
        screen.blit(title, title.get_rect(center=(self.W // 2, self.H // 2)))

    def draw_banner(self, screen):
        return
