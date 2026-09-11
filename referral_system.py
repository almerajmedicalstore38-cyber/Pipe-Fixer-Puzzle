from firebase_manager_lite import FirebaseManager
import re

class ReferralSystem:
    def __init__(self, wallet):
        self.wallet = wallet
        self.fb = FirebaseManager()
        # === FINAL 300% PROFIT SAFE ===
        self.COIN_TO_USD = 0.0001  # 10000 coins = $1 (10x kam)
        self.JOIN_BONUS = 0        # 0 = No loss on signup
        self.AD_REWARD = 20        # 1 Ad = 20 coins = $0.002 cost
        self.COMMISSION = 5        # Referral = 5 coins = $0.0005 cost - 300% profit safe

    def is_valid_code_format(self, code):
        if not code or len(code) < 6 or len(code) > 12:
            return False, "Invalid code length"
        if not re.match(r'^[A-Z0-9]+$', code.upper()):
            return False, "Invalid format"
        return True, "OK"

    def apply_code(self, code):
        code = code.strip().upper()
        my_code = self.wallet.data.get('referral_code','').upper()
        if code == my_code:
            return False, "Apna code nahi"
        if self.wallet.data.get('referredBy'):
            return False, "Already used"
        valid, msg = self.is_valid_code_format(code)
        if not valid:
            return False, msg
        
        if self.fb.online:
            try:
                docs = self.fb.db.collection("users").where("referral_code", "==", code).limit(1).get()
                if len(docs) == 0:
                    return False, "Code not found"
            except:
                pass
        
        self.wallet.data['referredBy'] = code
        if 'referrals' not in self.wallet.data:
            self.wallet.data['referrals']=[]

        self.wallet.data['referrals'].append({'code': code, 'coins': 0})
        self.wallet.save()
        try:
            if self.fb.online:
                self.fb.db.collection("referral_uses").add({
                    "new_user": self.wallet.data.get('email',''),
                    "inviter_code": code,
                    "bonus": 0
                })
        except:
            pass
        return True, f"Code Applied! Invite karo, har Ad par 5 coins milega"

    def on_ad_watched(self, ad_coins=20):
        """Har Ad par inviter ko 5 coins - 300% profit me bhi"""
        inviter_code = self.wallet.data.get('referredBy')
        if not inviter_code:
            return 0
        return self.COMMISSION  # 5 coins fixed

    def get_my_referrals(self):
        return self.wallet.data.get('referrals', [])