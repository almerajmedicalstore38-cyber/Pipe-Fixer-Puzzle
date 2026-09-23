[app]

title = Pipe Fixer Puzzle
package.name = pipefixerpuzzle
package.domain = com.sharafat
version = 1.0.0

source.dir = .
source.include_exts = py,png,jpg,jpeg,ttf,wav,ogg,mp3,json
source.exclude_dirs = tests, bin, venv, .buildozer

requirements = python3==3.11.5,hostpython3==3.11.5,kivy,pygame-bootstrap,pyjnius,android,requests

orientation = portrait
fullscreen = 1
android.permissions = INTERNET,ACCESS_NETWORK_STATE
android.api = 33
android.minapi = 21
android.ndk_api = 21
android.ndk = 25b
android.gradle_dependencies = com.google.android.gms:play-services-ads:22.6.0
android.archs = arm64-v8a
android.allow_backup = True
android.private_storage = True

# C99 compiler warnings aur grp error bypass karne ke liye
android.extra_p4a_args = --cflags="-Wno-implicit-function-declaration"

[buildozer]
log_level = 1
warn_on_root = 1
