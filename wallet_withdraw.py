from datetime import datetime
import pygame

def request_withdraw(wallet, amount_coins=100):
    info = {
        'coins': wallet.data.get('coins',0),
        'min': 100
    }
    if info['coins'] < info['min']:
        return False, f"Need {info['min'] - info['coins']} more coins"

    # Deduct
    if not wallet.deduct_coins(amount_coins):
        return False, "Not enough coins"

    record = {
        'time': datetime.now().strftime("%d-%m %H:%M"),
        'amount': amount_coins,
        'usd': amount_coins * 0.01,
        'status': 'pending'
    }
    wallet.data['withdraw_history'].insert(0, record)
    wallet.save()
    return True, f"Withdraw ${record['usd']:.2f} requested!"

def draw_withdraw_button(surf, x, y, enabled=True):
    font = pygame.font.SysFont("Arial", 20, bold=True)
    btn = pygame.Rect(x, y, 180, 48)
    color = (0, 230, 255) if enabled else (80, 80, 90)
    pygame.draw.rect(surf, color, btn, border_radius=12)
    txt_color = (0,0,0) if enabled else (150,150,150)
    surf.blit(font.render("WITHDRAW $1", True, txt_color), (btn.x + 14, btn.y + 12))
    return btn