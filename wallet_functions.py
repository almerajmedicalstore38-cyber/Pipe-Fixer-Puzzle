# wallet_functions.py - FINAL 300% PROFIT - BY SHTEDITOR
import json, os
import requests

class Wallet:
    LEVEL_REWARD = 5       # FINAL - Old Level Replay = 5C (Anti-Farm)
    DOUBLE_REWARD = 20     # FINAL - New Level Ad = 20C = $0.01
    REPLAY_REWARD = 5      # Old level = 5C
    HINT_COST = 15         # FINAL - Hint 15C (Tumhe profit)

    def __init__(self, path="wallet.json"):
        self.path = path
        self.data = {
            "coins": 0,
            "level": 1,
            "max_level": 1,  # === ANTI-FARM TRACKER ===
            "muted": False,
            "email": "",
            "is_gmail_user": False,
            "referral_code": "",
            "referrals": [],
            "saved_accounts": {},
            "withdraw_history": []
        }
        self.load()

    def load(self):
        try:
            if os.path.exists(self.path):
                with open(self.path, "r") as f:
                    d = json.load(f)
                    self.data.update(d)
                    # Purane users ke liye max_level fix
                    if "max_level" not in d:
                        self.data["max_level"] = self.data.get("level", 1)
                        
            if os.path.exists("wallet_data.json"):
                with open("wallet_data.json", "r") as f:
                    d2 = json.load(f)
                    if d2.get("email"):
                        self.data["email"] = d2.get("email")
                        self.data["is_gmail_user"] = True
        except: pass

    def save(self):
        try:
            with open(self.path, "w") as f:
                json.dump(self.data, f)
            with open("wallet_data.json", "w") as f:
                json.dump({"email": self.data.get("email","")}, f)
        except: pass

        # === FIREBASE LIVE SYNC ===
        try:
            email = self.data.get('email', '')
            if email:
                project_id = "coin-wallet-pro"
                safe_email = email.replace(".", "_").replace("@", "_").replace("-", "_")
                url = f"https://firestore.googleapis.com/v1/projects/{project_id}/databases/(default)/documents/users/{safe_email}"
                name = ""
                try:
                    if os.path.exists("user_name.json"):
                        with open("user_name.json", "r") as f:
                            name = json.load(f).get("name", "")
                except: pass
                payload = {
                    "fields": {
                        "email": {"stringValue": email},
                        "name": {"stringValue": name},
                        "coins": {"integerValue": str(self.data.get('coins', 0))},
                        "level": {"integerValue": str(self.data.get('level', 1))},
                        "max_level": {"integerValue": str(self.data.get('max_level', 1))},
                        "referral_code": {"stringValue": self.data.get('referral_code','')}
                    }
                }
                requests.patch(url, json=payload, timeout=3)
        except: pass

    def add_coins(self, amount):
        self.data["coins"] += amount
        self.save()
        print(f"[COINS] +{amount} = Total: {self.data['coins']}")

    def deduct_coins(self, amount):
        if self.data["coins"] >= amount:
            self.data["coins"] -= amount
            self.save()
            print(f"[COINS] -{amount} = Total: {self.data['coins']}")
            return True
        return False

    def set_level(self, lvl):
        # === 300% ANTI-FARM LOGIC ===
        self.data["level"] = lvl
        if lvl > self.data.get("max_level", 1):
            self.data["max_level"] = lvl
            print(f"[LEVEL] New MAX: {lvl} - Will get 20C")
        else:
            print(f"[LEVEL] Replay Old Level {lvl} - Will get only 5C")
        self.save()

    def set_muted(self, val):
        self.data["muted"] = val
        self.save()

    def get_max_level(self):
        return self.data.get("max_level", 1)