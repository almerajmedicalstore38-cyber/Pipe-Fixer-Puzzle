import pygame
from wallet_tabs import WalletTabManager

def draw_wallet_page(surf, wallet, W, H):
    surf.fill((13, 19, 48))
    font_title = pygame.font.SysFont("Arial", 38, bold=True)
    font_btn = pygame.font.SysFont("Arial", 20, bold=True)
    font_card = pygame.font.SysFont("Arial", 20, bold=True)
    font_small = pygame.font.SysFont("Arial", 15)
    surf.blit(font_title.render("WALLET", True, (235, 240, 255)), (18, 18))
    close_btn = pygame.Rect(W - 72, 16, 56, 34)
    pygame.draw.rect(surf, (95, 98, 115), close_btn, border_radius=8)
    font_x = pygame.font.SysFont("Arial", 20, bold=True)
    surf.blit(font_x.render("X", True, (255,255,255)), (close_btn.centerx - 6, close_btn.centery - 10))
    coins = wallet.data.get('coins',0)
    usd = coins * 0.01
    card = pygame.Rect(12, 68, W - 24, 88)
    pygame.draw.rect(surf, (30, 42, 95), card, border_radius=16)
    pygame.draw.rect(surf, (0, 230, 255), card, width=2, border_radius=16)
    surf.blit(font_card.render(f"Coins: {coins} = ${usd:.1f}", True, (255, 230, 80)), (card.x + 14, card.y + 14))
    surf.blit(font_small.render("Rate: 1 Coin = $0.01 | 1 Level = 10 Coins", True, (165, 185, 235)), (card.x + 14, card.y + 48))
    btns = {}
    labels = [("Profile", "profile"), ("Withdraw", "withdraw"), ("History", "history"), ("Referrals", "referrals")]
    for i, (label, key) in enumerate(labels):
        r = pygame.Rect(12 + (i % 2) * (W // 2), 168 + (i // 2) * 58, W // 2 - 18, 48)
        pygame.draw.rect(surf, (42, 52, 102), r, border_radius=12)
        pygame.draw.rect(surf, (65, 75, 125), r, width=1, border_radius=12)
        surf.blit(font_btn.render(label, True, (220, 225, 245)), (r.x + 16, r.y + 13))
        btns[key] = r
    detail_y = 290
    detail_rect = pygame.Rect(12, detail_y, W - 24, H - detail_y - 18)
    pygame.draw.rect(surf, (27, 35, 85), detail_rect, border_radius=16)
    return btns, close_btn, detail_y

def open_wallet(screen, wallet, W=None, H=None):
    if W is None: W,H = screen.get_size()
    manager = WalletTabManager(wallet)
    clock = pygame.time.Clock()
    running = True
    while running:
        for e in pygame.event.get():
            if e.type == pygame.QUIT: return
            if e.type == pygame.MOUSEBUTTONDOWN:
                mx,my = e.pos
                btns, close_btn, detail_y = draw_wallet_page(screen, wallet, W, H)
                if close_btn.collidepoint(mx,my): return
                manager.handle_click((mx,my), btns)

        btns, close_btn, detail_y = draw_wallet_page(screen, wallet, W, H)
        manager.draw_content(screen, detail_y, W, H)
        pygame.display.flip()
        clock.tick(60)