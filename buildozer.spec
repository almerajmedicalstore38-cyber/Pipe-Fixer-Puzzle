[app]
title = Pipe Fixer Puzzle
package.name = pipefixerpuzzle
package.domain = com.shteditor

source.dir =.
source.include_exts = py,png,jpg,kv,atlas,json,ttf,mp3,wav
source.include_patterns = main.py,config.py,wallet_functions.py,ad_manager.py,functions.py,game_state.py,level.py,ui.py,gui.py,sounds.py,wallet_pro_gui.py,firebase_manager_lite.py,firebase_manager.py,referral_system.py,withdraw_system.py,login_screen.py,auth_manager.py,pipes.py,level_gen.py,checks.py,assets/*

version = 1.5
version.regex = __version__ = ['"](.*)['"]
version.filename = %(source.dir)s/main.py

requirements = python3,pygame,requests,pyjnius,android,openssl,certifi,charset-normalizer,idna,urllib3

# icon.filename = %(source.dir)s/icon.png
# presplash.filename = %(source.dir)s/presplash.png

orientation = portrait
fullscreen = 0

# === PERMISSIONS ===
android.permissions = INTERNET,ACCESS_NETWORK_STATE,ACCESS_WIFI_STATE,VIBRATE

# === API - FINAL FOR PLAY STORE ===
android.api = 33
android.minapi = 21
android.ndk = 25b
android.sdk = True

# === 32 + 64 BIT SUPPORT - SABSE ZAROORI ===
android.archs = armeabi-v7a, arm64-v8a

# === REAL ADMOB ADS ===
android.gradle_dependencies = com.google.android.gms:play-services-ads:22.5.0
android.meta-data = com.google.android.gms.ads.APPLICATION_ID=ca-app-pub-3940256099942544~3347511713

# === RELEASE BUILD ===
android.release_artifact = apk
android.accept_sdk_license_agreement = True

# === THEME ===
android.apptheme = @android:style/Theme.NoTitleBar
android.allow_backup = True

# === BUILD CONFIG ===
p4a.bootstrap = sdl2
p4a.port = 8000

android.logcat_filters = *:S python:D
android.logcat_pid_only = False

# === KEYSTORE - GITHUB ME AUTO BANEGA ===
# p4a will generate debug keystore for release if not provided
# For Play Store upload, use your own keystore later

[buildozer]
log_level = 2
warn_on_root = 1
# build_dir =./.buildozer
# bin_dir =./bin
