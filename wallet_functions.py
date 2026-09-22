# wallet_functions.py - SECURE ONLINE-ONLY SAVE - BY SHTEDITOR
import json, os
import threading
import requests

class Wallet:
    LEVEL_REWARD = 5       # Old Level Replay = 5C (Anti-Farm)
    DOUBLE_REWARD = 20     # New Level Ad = 20C
    REPLAY_REWARD = 5      # Old level = 5C
    HINT_COST = 15         # Hint 15C

    def __init__(self, filename="wallet.json"):
        base_dir = os.environ.get('ANDROID_PRIVATE', os.path.dirname(os.path.abspath(__file__)))
        self.path = os.path.join(base_dir, filename)
        self.wallet_data_path = os.path.join(base_dir, "wallet_data.json")
        self.user_name_path = os.path.join(base_dir, "user_name.json")

        self.data = {
            "coins": 0,
            "level": 1,
            "max_level": 1,
            "muted": False,
            "email": "",
            "is_gmail_user": False,
            "referral_code": "",
            "referrals": [],
            "saved_accounts": {},
            "withdraw_history": []
        }
        self.load()

    def is_guest(self):
        # Security Check: Guest user ya empty email detection
        email = self.data.get("email", "").strip().lower()
        return not email or email == "guest_user@app.com" or "guest" in email

    def load(self):
        try:
            if os.path.exists(self.path):
                with open(self.path, "r") as f:
                    d = json.load(f)
                    self.data.update(d)
                    if "max_level" not in d:
                        self.data["max_level"] = self.data.get("level", 1)
                        
            if os.path.exists(self.wallet_data_path):
                with open(self.wallet_data_path, "r") as f:
                    d2 = json.load(f)
                    if d2.get("email"):
                        self.data["email"] = d2.get("email")
                        self.data["is_gmail_user"] = True
        except Exception as e:
            print(f"[WALLET LOAD ERROR] {e}")

    def save(self):
        # === ANTI-HACK SECURITY GUARD ===
        # Guest ya Offline User ka progress local disk par SAVE NAHI HOGA
        if self.is_guest():
            print("[SECURITY] Guest/Offline mode detected. Progress will NOT be saved to disk.")
            return

        # Pure Legitimate Authenticated Users Only
        try:
            with open(self.path, "w") as f:
                json.dump(self.data, f)
            with open(self.wallet_data_path, "w") as f:
                json.dump({"email": self.data.get("email", "")}, f)
        except Exception as e:
            print(f"[WALLET SAVE ERROR] {e}")

        # === FIREBASE LIVE SYNC IN BACKGROUND THREAD ===
        def sync_firebase():
            try:
                email = self.data.get('email', '')
                if email and not self.is_guest():
                    project_id = "coin-wallet-pro"
                    safe_email = email.replace(".", "_").replace("@", "_").replace("-", "_")
                    url = f"https://firestore.googleapis.com/v1/projects/{project_id}/databases/(default)/documents/users/{safe_email}"
                    name = ""
                    try:
                        if os.path.exists(self.user_name_path):
                            with open(self.user_name_path, "r") as f:
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
                    requests.patch(url, json=payload, timeout=4)
            except Exception as ex:
                print(f"[FIREBASE SYNC ERROR] {ex}")

        threading.Thread(target=sync_firebase, daemon=True).start()

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
