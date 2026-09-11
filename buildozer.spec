[app]

# === APP INFO ===
title = Pipe Fixer Puzzle
package.name = pipefixerpuzzle
package.domain = com.shteditor

source.dir =.
source.include_exts = py,png,jpg,kv,atlas,json,ttf,mp3,wav

# === VERSION ===
version = 1.5
version.regex = __version__ = ['"](.*)['"]
version.filename = %(source.dir)s/main.py

# === MAIN FILES - TUMHARI SARI FILES ===
source.include_patterns = main.py,config.py,wallet_functions.py,ad_manager.py,functions.py,game_state.py,level.py,ui.py,gui.py,sounds.py,wallet_pro_gui.py,firebase_manager_lite.py,referral_system.py,withdraw_system.py,login_screen.py,auth_manager.py,pipes.py,level_gen.py,checks.py,assets/*,images/*

# === REQUIREMENTS - REAL ADMOB KE LIYE FINAL ===
requirements = python3,pygame,requests,pyjnius,android,openssl

# === ICON ===
# icon.filename = %(source.dir)s/icon.png
# presplash.filename = %(source.dir)s/presplash.png

# === ANDROID PERMISSIONS ===
android.permissions = INTERNET,ACCESS_NETWORK_STATE,ACCESS_WIFI_STATE

# === ORIENTATION ===
orientation = portrait

# === ANDROID API ===
android.api = 33
android.minapi = 21
android.ndk = 25b
android.sdk = True

# === ADMOB REAL ADS - SABSE ZARURI ===
# Ye 2 lines se Real Google Ads ayenge APK me
android.gradle_dependencies = com.google.android.gms:play-services-ads:22.5.0

android.meta-data = com.google.android.gms.ads.APPLICATION_ID=ca-app-pub-3940256099942544~3347511713

# === ANDROID BUILD TYPE ===
# Test ke liye debug, Play Store ke liye release
android.release_artifact = apk

# === ALLOW BACKUP ===
android.allow_backup = True

# === FULLSCREEN ===
fullscreen = 0

# === LOGCAT FILTER ===
android.logcat_filters = *:S python:D
android.logcat_pid_only = False

# === P4A SETTINGS ===
p4a.bootstrap = sdl2
p4a.port = 8000

# === APP THEME ===
android.apptheme = @android:style/Theme.NoTitleBar

# === WHITELIST ===
# android.whitelist =

# === BUILD DIR ===
# build_dir =./.buildozer

[buildozer]

# === LOG LEVEL ===
log_level = 2

# === BUILD DIR ===
warn_on_root = 1

# === BINARIES ===
# bin_dir =./bin