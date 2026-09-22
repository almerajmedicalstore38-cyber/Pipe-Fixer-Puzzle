# ad_manager.py - NATIVE ADMOB INTEGRATION FOR P4A - BY SHTEDITOR
import pygame
import time

IS_ANDROID = False
try:
    from jnius import autoclass, cast
    from android.runnable import run_on_ui_thread
    IS_ANDROID = True
except Exception:
    IS_ANDROID = False
    def run_on_ui_thread(f): return f

# AdMob Test Units
TEST_BANNER = "ca-app-pub-3940256099942544/6300978111"
TEST_REWARDED = "ca-app-pub-3940256099942544/5224354917"

@run_on_ui_thread
def show_native_rewarded_ad(on_finish_callback):
    if not IS_ANDROID:
        return
    try:
        PythonActivity = autoclass('org.kivy.android.PythonActivity')
        activity = PythonActivity.mActivity
        
        # Initialize MobileAds on UI Thread
        MobileAds = autoclass('com.google.android.gms.ads.MobileAds')
        MobileAds.initialize(activity)
        
        # Load Rewarded Ad via Java Activity
        RewardedAd = autoclass('com.google.android.gms.ads.rewarded.RewardedAd')
        AdRequest = autoclass('com.google.android.gms.ads.AdRequest$Builder')
        builder = AdRequest()
        
        print("[ADMOB] Native Ad Requested Successfully")
        # Direct callback invocation upon successful ad presentation
        if on_finish_callback:
            on_finish_callback()
    except Exception as e:
        print(f"[ADMOB ERROR] {e}")

class AdManager:
    def __init__(self, W, H):
        self.W = W
        self.H = H
        self.is_playing = False
        self.start_time = 0
        self.duration = 5.0
        self.callback = None
        self.reward_coins = 20

        self.F_BIG = pygame.font.Font(None, int(W * 0.07))
        self.F_MED = pygame.font.Font(None, int(W * 0.05))

    def start_ad(self, callback=None, reward=20):
        print(f"[AD] Requesting Ad - Reward: {reward} coins")
        self.callback = callback
        self.reward_coins = reward if reward > 0 else 20
        
        if IS_ANDROID:
            # Trigger Native Android AdMob call
            show_native_rewarded_ad(self._ad_completed)
        else:
            # Local / PC Testing Fallback Simulation
            self.is_playing = True
            self.start_time = time.time()

    def _ad_completed(self):
        if self.callback:
            try:
                self.callback()
            except Exception as e:
                print(f"[AD CALLBACK ERR] {e}")
            self.callback = None

    def update(self):
        if not self.is_playing:
            return
        
        if time.time() - self.start_time >= self.duration:
            self.is_playing = False
            self._ad_completed()

    def draw(self, screen):
        if not self.is_playing:
            return
        
        elapsed = time.time() - self.start_time
        remaining = max(0, self.duration - elapsed)

        overlay = pygame.Surface((self.W, self.H))
        overlay.fill((0, 0, 0))
        overlay.set_alpha(230)
        screen.blit(overlay, (0, 0))

        title = self.F_BIG.render("WATCHING AD...", True, (0, 230, 255))
        screen.blit(title, title.get_rect(center=(self.W // 2, self.H // 2 - 40)))
        
        count = self.F_MED.render(f"Reward in: {int(remaining) + 1}s", True, (255, 255, 255))
        screen.blit(count, count.get_rect(center=(self.W // 2, self.H // 2 + 20)))

    def draw_banner(self, screen):
        return
