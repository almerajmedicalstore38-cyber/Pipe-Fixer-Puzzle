[app]
title = Pipe Fixer Puzzle
package.name = pipefixerpuzzle
package.domain = com.shteditor

source.dir =.
source.include_exts = py,png,jpg,kv,atlas,json,ttf,mp3,wav
source.include_patterns = assets/*,*.py

version = 1.5

requirements = python3,pygame,requests,pyjnius,android,openssl,certifi,charset-normalizer,idna,urllib3

orientation = portrait
fullscreen = 0

android.permissions = INTERNET,ACCESS_NETWORK_STATE

android.api = 33
android.minapi = 21
android.ndk = 25b

# 32 + 64 BIT - DONO
android.archs = armeabi-v7a, arm64-v8a

android.accept_sdk_license_agreement = True
p4a.bootstrap = sdl2

[buildozer]
log_level = 2
warn_on_root = 1
