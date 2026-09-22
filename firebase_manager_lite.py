import requests
import json
import os
import ssl

# Android SSL Certificate Crash Bypass Fix
try:
    ssl._create_default_https_context = ssl._create_unverified_context
except AttributeError:
    pass

class FirebaseManager:
    def __init__(self):
        self.online = False
        self.project_id = "coin-wallet-pro-fb8vc"
        # Firestore REST API - no need for serviceAccountKey.json
        self.base_url = f"https://firestore.googleapis.com/v1/projects/{self.project_id}/databases/(default)/documents"
        self.online = True
        print("[FIREBASE LITE] Online ✓ (REST Mode)")

    def save_user(self, email, data):
        try:
            url = f"{self.base_url}/users/{email}"
            payload = {"fields": self._to_fields(data)}
            # Timeout aur verify=False add kiya gaya hai crash rokne ke liye
            r = requests.patch(url, json=payload, timeout=5, verify=False)
            return r.status_code in [200, 201]
        except Exception as e:
            print(f"Save error: {e}")
            return False

    def get_user_by_code(self, code):
        try:
            url = f"{self.base_url}:runQuery"
            query = {
                "structuredQuery": {
                    "from": [{"collectionId": "users"}],
                    "where": {
                        "fieldFilter": {
                            "field": {"fieldPath": "referral_code"},
                            "op": "EQUAL",
                            "value": {"stringValue": code}
                        }
                    },
                    "limit": 1
                }
            }
            r = requests.post(url, json=query, timeout=5, verify=False)
            if r.status_code == 200 and r.json():
                return True
            return False
        except Exception as e:
            print(f"Query error: {e}")
            return False

    def _to_fields(self, data):
        fields = {}
        for k, v in data.items():
            if isinstance(v, str):
                fields[k] = {"stringValue": v}
            elif isinstance(v, int):
                fields[k] = {"integerValue": str(v)}
            elif isinstance(v, bool):
                fields[k] = {"booleanValue": v}
            elif isinstance(v, float):
                fields[k] = {"doubleValue": v}
        return fields
