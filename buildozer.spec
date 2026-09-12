[app]
title = Pipe Fixer Puzzle
package.name = pipefixerpuzzle
package.domain = com.shteditor
source.dir =.
source.include_exts = py,png,jpg,json
source.include_patterns = assets/*,*.py
version = 1.5
requirements = python3,pygame,requests,pyjnius,android,openssl,certifi
orientation = portrait
android.permissions = INTERNET,ACCESS_NETWORK_STATE
android.api = 33
android.minapi = 21
android.ndk = 25b
android.accept_sdk_license_agreement = True
android.archs = arm64-v8a, armeabi-v7a
p4a.bootstrap = sdl2
[buildozer]
log_level = 2
