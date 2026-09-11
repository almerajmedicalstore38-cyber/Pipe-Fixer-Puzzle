import time
from datetime import datetime

def ensure_wallet_data(wallet):
    # Old wallet ko disturb kiye bina new keys add karo
    if 'profile' not in wallet.data:
        wallet.data['profile'] = {'name': 'Guest', 'id': f"USER{int(time.time())%100000}"}
    if 'total_levels' not in wallet.data:
        wallet.data['total_levels'] = wallet.data.get('max_level', 1)
    if 'withdraw_history' not in wallet.data:
        wallet.data['withdraw_history'] = []
    if 'referrals' not in wallet.data:
        wallet.data['referrals'] = []
    if 'referral_code' not in wallet.data:
        wallet.data['referral_code'] = f"REF{wallet.data['profile']['id'][-4:]}"
    wallet.save()

def get_balance_info(wallet):
    coins = wallet.data.get('coins', 0)
    return {
        'coins': coins,
        'usd': coins * 0.01,
        'can_withdraw': coins >= 100,
        'need_more': max(0, 100 - coins)
    }

def add_referral(wallet, code, coins=50):
    wallet.data['referrals'].append({
        'code': code,
        'coins': coins,
        'time': datetime.now().strftime("%d-%m-%Y")
    })
    wallet.add_coins(coins)