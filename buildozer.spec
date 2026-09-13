[app]
title = Pipe Fixer Puzzle
package.name = pipefixerpuzzle
package.domain = com.shteditor.pipefixer
source.dir =.
source.include_exts = py,png,jpg,json,wav,mp3
source.include_patterns = assets/*
version = 1.5
requirements = python3,pygame==2.6.1
orientation = portrait
android.permissions = INTERNET
android.api = 33
android.minapi = 21
android.ndk = 28c
android.sdk_build_tools_version = 33.0.2
android.accept_sdk_license_agreement = True
android.archs = arm64-v8a
p4a.bootstrap = sdl2
p4a.branch = master
p4a.sdk_dir = /usr/local/lib/android/sdk
p4a.ndk_dir = /usr/local/lib/android/sdk/ndk/28.1.13356709

[buildozer]
log_level = 2
