[app]
# Title
title = Pipe Fixer Puzzle

# Package
package.name = pipefixerpuzzle
package.domain = com.shteditor.pipefixer

# Source
source.dir =.
source.include_exts = py,png,jpg,json,wav,mp3
source.include_patterns = assets/*

# Version
version = 1.5

# Requirements - YAHI MAIN FIX HAI - openssl add kiya purani file ki tarah
requirements = python3,pygame==2.5.2,sdl2,sdl2_image,sdl2_mixer,sdl2_ttf,openssl,libffi

# Orientation
orientation = portrait
fullscreen = 0

# Android Permissions
android.permissions = INTERNET

# Android API & NDK - Purani working wali settings
android.api = 33
android.minapi = 21
android.ndk = 25b
android.archs = arm64-v8a
android.accept_sdk_license_agreement = True

# python-for-android
p4a.branch = master
p4a.bootstrap = sdl2

[buildozer]
log_level = 2
warn_on_root = 1
