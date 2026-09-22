[app]

# Application metadata
title = Pipe Fixer Puzzle
package.name = pipefixerpuzzle
package.domain = com.sharafat
version = 1.0.0

# Source and bundled assets
source.dir = .
source.include_exts = py,png,jpg,jpeg,ttf,wav,ogg,mp3,json

# Python-for-Android dependencies
requirements = python3,pygame,pyjnius,android,requests,urllib3,certifi,charset-normalizer,idna

# Android configuration
orientation = portrait
fullscreen = 1
android.permissions = INTERNET,ACCESS_NETWORK_STATE
android.api = 35
android.minapi = 23
android.ndk = 27c
android.gradle_dependencies = com.google.android.gms:play-services-ads:22.6.0
android.archs = arm64-v8a
android.androidx = True
android.private_storage = True

[buildozer]
log_level = 2
warn_on_root = 1
