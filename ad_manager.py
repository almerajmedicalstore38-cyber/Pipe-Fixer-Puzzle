import pygame
import time

# === Android Detection (Safe) ===
IS_ANDROID = False
try:
    from jnius import autoclass
    IS_ANDROID = True
    print("[ADMOB] Real Ads Mode - APK")
except Exception as e:
    IS_ANDROID = False
    print(f"[ADMOB] Fake Test Mode - Pydroid ({e})")

class AdManager:
    def __init__(self, W, H):
        self.W = W
        self.H = H
        self.is_playing = False
        self.start_time = 0
        self.duration = 5.0  # 5 Seconds Fake Ad for Testing/Offline Fallback
        self.callback = None
        self.reward_coins = 20

        self.TEST_IDS = {
            "rewarded": "ca-app-pub-3940256099942544/5224354917",
            "banner": "ca-app-pub-3940256099942544/6300978111"
        }

        # Safe System Font Fix for Android
        self.F_BIG = pygame.font.Font(None, int(W * 0.07))
        self.F_MED = pygame.font.Font(None, int(W * 0.05))
        self.F_TINY = pygame.font.Font(None, int(W * 0.03))
        
        self.banner_h = int(H * 0.065)
        self.banner_rect = pygame.Rect(0, H - self.banner_h, W, self.banner_h)

    def start_ad(self, callback=None, reward=20):
        print(f"[AD] Requesting Ad - Reward: {reward} coins")
        self.callback = callback
        self.reward_coins = reward if reward > 0 else 20
        self.start_time = time.time()

        if IS_ANDROID:
            success = self.show_real_rewarded_ad()
            if not success:
                # Agar real ad load nahi ho paaye to fallback simulate karo
                self.is_playing = True
        else:
            # PC / Local Test Mode
            self.is_playing = True

    def show_real_rewarded_ad(self):
        try:
            print("[ADMOB] Attempting Native Ad Show...")
            PythonActivity = autoclass('org.kivy.android.PythonActivity')
            activity = PythonActivity.mActivity
            
            # AdMob SDK native binding check (Fallback to safety if SDK missing)
            # Future expansion: Yahan Google Mobile Ads Java bridge bind ho sakta hai
            return False 
        except Exception as e:
            print(f"[ADMOB] Native Show Fail: {e}")
            return False

    def update(self):
        if not self.is_playing: 
            return
        
        # Ad Complete Trigger Logic
        if time.time() - self.start_time >= self.duration:
            self.is_playing = False
            print(f"[AD] Watched Successfully - Rewarding {self.reward_coins} coins")
            
            # Reward callback runs ONLY after ad completes
            if self.callback:
                try:
                    self.callback()
                except Exception as e:
                    print(f"[AD CALLBACK ERROR] {e}")
                self.callback = None

    def draw(self, screen):
        if not self.is_playing: 
            return
        
        elapsed = time.time() - self.start_time
        progress = min(1.0, elapsed / self.duration)
        remaining = max(0, self.duration - elapsed)

        overlay = pygame.Surface((self.W, self.H))
        overlay.fill((0, 0, 0))
        overlay.set_alpha(230)
        screen.blit(overlay, (0, 0))

        box_w = int(self.W * 0.88)
        box_h = int(self.H * 0.45)
        box_x = (self.W - box_w) // 2
        box_y = (self.H - box_h) // 2

        pygame.draw.rect(screen, (30, 30, 30), (box_x, box_y, box_w, box_h), border_radius=20)
        pygame.draw.rect(screen, (255, 215, 0), (box_x, box_y, box_w, box_h), width=3, border_radius=20)

        title = self.F_BIG.render("WATCHING AD...", True, (0, 230, 255))
        screen.blit(title, title.get_rect(center=(self.W // 2, box_y + 60)))
        
        reward_txt = self.F_MED.render(f"Reward: +{self.reward_coins} Coins", True, (255, 230, 80))
        screen.blit(reward_txt, reward_txt.get_rect(center=(self.W // 2, box_y + 110)))
        
        count = self.F_MED.render(f"Reward in: {int(remaining) + 1}s", True, (255, 255, 255))
        screen.blit(count, count.get_rect(center=(self.W // 2, box_y + 160)))

        bar_w = box_w - 40
        bar_x = box_x + 20
        bar_y = box_y + box_h - 60
        pygame.draw.rect(screen, (60, 60, 60), (bar_x, bar_y, bar_w, 12), border_radius=6)
        pygame.draw.rect(screen, (0, 255, 130), (bar_x, bar_y, int(bar_w * progress), 12), border_radius=6)

    def draw_banner(self, screen):
        return

