[app]
title = Pipe Fixer Puzzle
package.name = pipefixerpuzzle
package.domain = com.shteditor.pipefixer
source.dir = .
source.include_exts = py,png,jpg,json,wav,mp3
source.include_patterns = assets/*
version = 1.5
requirements = python3,pygame==2.5.2
orientation = portrait
fullscreen = 0
android.permissions = INTERNET
android.api = 33
android.minapi = 21
android.ndk_path = /usr/local/lib/android/sdk/ndk/25.1.8937393
android.archs = arm64-v8a
android.accept_sdk_license_agreement = True
p4a.branch = master
p4a.bootstrap = sdl2

[buildozer]
log_level = 2
warn_on_root = 1
