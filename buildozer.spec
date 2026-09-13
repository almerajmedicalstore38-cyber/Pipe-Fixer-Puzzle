[app]
title = Pipe Fixer Puzzle
package.name = pipefixerpuzzle
package.domain = com.shteditor.pipefixer
source.dir =.
source.include_exts = py,png,jpg,json,wav,mp3
source.include_patterns = assets/*
version = 1.5
requirements = python3,sdl2,sdl2_image,sdl2_mixer,sdl2_ttf,pygame==2.5.2
orientation = portrait
android.permissions = INTERNET
android.api = 32
android.minapi = 21
android.ndk = 23b
android.sdk_build_tools_version = 32.0.0
android.accept_sdk_license_agreement = True
android.archs = arm64-v8a
p4a.bootstrap = sdl2
p4a.branch = master
p4a.ndk_api = 21

[buildozer]
log_level = 2
