from firebase_manager_lite import FirebaseManager

class WithdrawSystem:
    def __init__(self, wallet):
        self.wallet = wallet
        self.fb = FirebaseManager()
        self.MIN_WITHDRAW_COINS = 10000  # 10000 coins = $1 (10x zyada lagega)
        self.COIN_TO_USD = 0.0001        # 10000 coins = $1 (Rate 10x kam)

        if 'saved_accounts' not in self.wallet.data:
            self.wallet.data['saved_accounts'] = {
                "USDT": {"address": ""},
                "JazzCash": {"name": "", "number": ""},
                "Easypaisa": {"name": "", "number": ""}
            }

    def save_account(self, method, name="", number="", address=""):
        if method == "USDT":
            self.wallet.data['saved_accounts']["USDT"] = {"address": address}
        elif method == "JazzCash":
            self.wallet.data['saved_accounts']["JazzCash"] = {"name": name, "number": number}
        elif method == "Easypaisa":
            self.wallet.data['saved_accounts']["Easypaisa"] = {"name": name, "number": number}
        self.wallet.save()
        return True

    def get_saved_account(self, method):
        return self.wallet.data.get('saved_accounts', {}).get(method, {})

    def withdraw(self, method, name="", number="", address=""):
        coins = self.wallet.data.get('coins',0)
        if coins < self.MIN_WITHDRAW_COINS:
            return False, f"Need {self.MIN_WITHDRAW_COINS - coins} more coins (Min {self.MIN_WITHDRAW_COINS})"
        
        if method == "USDT":
            if len(address) < 20:
                return False, "Invalid USDT address"
            self.save_account(method, address=address)
            acc_display = address[:12] + "..." + address[-6:]
        else:
            if len(name) < 3:
                return False, "Enter full name"
            if len(number) < 10:
                return False, "Invalid number"
            self.save_account(method, name=name, number=number)
            acc_display = f"{name} - {number}"

        # 10000 coins = $1
        usd_value = self.MIN_WITHDRAW_COINS * self.COIN_TO_USD
        
        ok, msg = self.fb.request_withdraw(
            self.wallet,
            method,
            acc_display,
            self.MIN_WITHDRAW_COINS,  # 10000 coins
            full_data={
                "name": name,
                "number": number,
                "address": address,
                "usd_value": usd_value  # $1
            }
        )
        if ok:
            self.wallet.data['coins'] -= self.MIN_WITHDRAW_COINS
            self.wallet.save()
        return ok, msg

    def get_progress(self):
        coins = self.wallet.data.get('coins', 0)
        usd = coins * self.COIN_TO_USD
        percent = (coins / self.MIN_WITHDRAW_COINS) * 100
        return {
            "coins": coins,
            "usd": usd,
            "percent": min(100, percent),
            "remaining": max(0, self.MIN_WITHDRAW_COINS - coins)
        }