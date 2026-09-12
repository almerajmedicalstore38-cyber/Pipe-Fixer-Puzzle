[app]
title = Pipe Fixer Puzzle
package.name = pipefixerpuzzle
package.domain = com.shteditor

source.dir =.
source.include_exts = py,png,jpg,json
source.include_patterns = assets/*,*.py

version = 1.5

requirements = python3==3.10.13,pygame,requests,pyjnius,openssl,certifi,charset-normalizer,urllib3

orientation = portrait
fullscreen = 0

android.permissions = INTERNET,ACCESS_NETWORK_STATE

android.api = 33
android.minapi = 21
android.ndk = 25b
android.sdk_build_tools_version = 33.0.2
android.accept_sdk_license_agreement = True

android.archs = arm64-v8a, armeabi-v7a

p4a.bootstrap = sdl2
p4a.branch = master

[buildozer]
log_level = 2
warn_on_root = 1
