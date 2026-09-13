[app]
title = Pipe Fixer Puzzle
package.name = pipefixerpuzzle
package.domain = com.shteditor.pipefixer
source.dir =.
source.include_exts = py,png,jpg,json,wav,mp3
source.include_patterns = assets/*
version = 1.5
requirements = python3,pygame
orientation = portrait
android.permissions = INTERNET
android.api = 33
android.minapi = 21
android.ndk = 25b
android.sdk_build_tools_version = 33.0.2
android.accept_sdk_license_agreement = True
android.archs = arm64-v8a
p4a.bootstrap = sdl2
p4a.branch = master

[buildozer]
log_level = 2
