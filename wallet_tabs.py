import pygame
from wallet_logic import get_balance_info, ensure_wallet_data
from wallet_withdraw import request_withdraw, draw_withdraw_button

class WalletTabManager:
    def __init__(self, wallet):
        self.wallet = wallet
        self.current_tab = "profile"
        ensure_wallet_data(wallet)
        self.withdraw_btn = None
        self.last_message = ""

    def handle_click(self, pos, btns):
        for key, rect in btns.items():
            if rect.collidepoint(pos):
                self.current_tab = key
                return True
        if self.current_tab == "withdraw" and self.withdraw_btn:
            if self.withdraw_btn.collidepoint(pos):
                ok, msg = request_withdraw(self.wallet, 100)
                self.last_message = msg
                return True
        return False

    def draw_content(self, surf, detail_y, W, H):
        font = pygame.font.SysFont("Arial", 20, bold=True)
        font2 = pygame.font.SysFont("Arial", 18)
        small = pygame.font.SysFont("Arial", 15)
        x = 26
        y = detail_y + 16

        profile = self.wallet.data.get('profile', {'name': 'Guest', 'id': 'USER123'})
        total_levels = self.wallet.data.get('total_levels', 1)
        history = self.wallet.data.get('withdraw_history', [])
        referrals = self.wallet.data.get('referrals', [])
        balance = get_balance_info(self.wallet)

        if self.current_tab == "profile":
            surf.blit(font2.render(f"Name: {profile.get('name','Guest')}", True, (235,240,255)), (x,y)); y+=30
            surf.blit(small.render(f"ID: {profile.get('id','---')}", True, (160,180,220)), (x,y)); y+=26
            surf.blit(font.render(f"Levels Completed: {total_levels}", True, (0,255,140)), (x,y)); y+=30
            surf.blit(small.render(f"Referral Code: {self.wallet.data.get('referral_code','---')}", True, (255,215,0)), (x,y))

        elif self.current_tab == "withdraw":
            surf.blit(font.render(f"Available: {balance['coins']} Coins", True, (255,215,0)), (x,y)); y+=34
            surf.blit(small.render("Minimum withdraw: 100 Coins ($1)", True, (200,210,240)), (x,y)); y+=30
            if not balance['can_withdraw']:
                surf.blit(small.render(f"Need {balance['need_more']} more coins", True, (255,120,120)), (x,y))
                self.withdraw_btn = draw_withdraw_button(surf, x, y+26, False)
            else:
                self.withdraw_btn = draw_withdraw_button(surf, x, y+26, True)
                if self.last_message:
                    surf.blit(small.render(self.last_message, True, (0,255,130)), (x, y+85))

        elif self.current_tab == "history":
            if not history:
                surf.blit(font2.render("No withdraw history yet", True, (150,160,190)), (x,y)); y+=30
                surf.blit(small.render("Play levels to earn coins!", True, (100,120,150)), (x,y))
            else:
                for h in history[:12]:
                    surf.blit(small.render(f"{h['time']} - {h['amount']}c = ${h['usd']} [{h['status']}]", True, (230,235,255)), (x,y)); y+=22

        elif self.current_tab == "referrals":
            surf.blit(font.render("Refer & Earn 50 Coins", True, (0,255,160)), (x,y)); y+=30
            surf.blit(small.render(f"Your Code: {self.wallet.data.get('referral_code','')}", True, (255,215,0)), (x,y)); y+=28
            surf.blit(small.render("Share your code with friends", True, (160,180,220)), (x,y)); y+=30
            if not referrals:
                surf.blit(small.render("No referrals yet", True, (120,130,160)), (x,y))
            else:
                for r in referrals[:12]:
                    surf.blit(small.render(f"{r['code']} +{r['coins']} Coins", True, (200,255,210)), (x,y)); y+=22