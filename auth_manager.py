# auth_manager.py - FINAL WITH NAME - BY SHTEDITOR
import requests, json, os

API_KEY = "AIzaSyCIgBbWMt5KEm7yrSjfn00GtmZ0T5AlVxE"
current_user_email = None

# --- NAME SAVE SYSTEM ---
def save_name_locally(email, name):
    try:
        with open("user_name.json", "w") as f:
            json.dump({"email": email, "name": name}, f)
    except: pass

def get_user_display_name():
    try:
        if os.path.exists("user_name.json"):
            with open("user_name.json", "r") as f:
                d = json.load(f)
                return d.get("name", "Guest")
    except: pass
    if current_user_email:
        return current_user_email.split('@')[0].capitalize()
    return "Guest"

def signup_user(email, password, name=""):
    global current_user_email
    url = f"https://identitytoolkit.googleapis.com/v1/accounts:signUp?key={API_KEY}"
    data = {"email": email, "password": password, "returnSecureToken": True}
    try:
        r = requests.post(url, json=data, timeout=10)
        res = r.json()
        if r.status_code == 200:
            current_user_email = email

            # Naam Firebase aur Local me save karo
            id_token = res.get("idToken")
            if name and id_token:
                url2 = f"https://identitytoolkit.googleapis.com/v1/accounts:update?key={API_KEY}"
                try:
                    requests.post(url2, json={"idToken": id_token, "displayName": name, "returnSecureToken": True}, timeout=10)
                except: pass
                save_name_locally(email, name)

            _create_user_in_firestore(email, name)
            return True, f"Welcome {name}! Account ban gaya!"
        else:
            error = res.get("error", {}).get("message", "")
            if "EMAIL_EXISTS" in error: return False, "Ye email pehle se hai"
            elif "WEAK_PASSWORD" in error: return False, "Password 6 harf ka rakho"
            else: return False, f"Error: {error}"
    except Exception as e:
        return False, f"Internet Error: {e}"

def login_user(email, password):
    global current_user_email
    url = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={API_KEY}"
    data = {"email": email, "password": password, "returnSecureToken": True}
    try:
        r = requests.post(url, json=data, timeout=10)
        res = r.json()
        if r.status_code == 200:
            current_user_email = email
            # Login pe naam load karo
            display_name = res.get("displayName", "")
            if display_name:
                save_name_locally(email, display_name)
            return True, "Login ho gaya!"
        else:
            error = res.get("error", {}).get("message", "")
            if "INVALID_LOGIN_CREDENTIALS" in error or "INVALID_PASSWORD" in error:
                return False, "Email ya Password galat hai"
            else: return False, f"Error: {error}"
    except Exception as e:
        return False, f"Internet Error: {e}"

def forgot_password(email):
    url = f"https://identitytoolkit.googleapis.com/v1/accounts:sendOobCode?key={API_KEY}"
    data = {"requestType": "PASSWORD_RESET", "email": email}
    try:
        r = requests.post(url, json=data, timeout=10)
        res = r.json()
        if r.status_code == 200:
            return True, "Reset link email par bhej diya!"
        else:
            error = res.get("error", {}).get("message", "")
            return False, f"Error: {error}"
    except Exception as e:
        return False, f"Internet Error: {e}"

def _create_user_in_firestore(email, name=""):
    try:
        project_id = "coin-wallet-pro"
        safe_email = email.replace(".", "_").replace("@", "_").replace("-", "_")
        url = f"https://firestore.googleapis.com/v1/projects/{project_id}/databases/(default)/documents/users/{safe_email}"
        payload = {
            "fields": {
                "email": {"stringValue": email},
                "name": {"stringValue": name},
                "coins": {"integerValue": "0"},
                "createdAt": {"stringValue": "new"}
            }
        }
        requests.patch(url, json=payload, timeout=10)
    except: pass

def get_current_user():
    return current_user_email

def logout_user():
    global current_user_email
    current_user_email = None
    try:
        if os.path.exists("wallet_data.json"): os.remove("wallet_data.json")
        if os.path.exists("user_name.json"): os.remove("user_name.json")
    except: pass