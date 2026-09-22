[app]

# Application Info
title = Pipe Fixer
package.name = pipefixer
package.domain = com.sharafat
source.dir = .
source.include_exts = py,png,jpg,jpeg,ttf,otf,wav,mp3,ogg,json
source.include_dirs = assets
version = 1.0.0

# Requirements & Bootstraps (Fixed line below)
requirements = python3,pygame,pyjnius,openssl,requests,urllib3,certifi,charset_normalizer,idna
p4a.bootstrap = sdl2

# Permissions
android.permissions = INTERNET, ACCESS_NETWORK_STATE

# Android API & NDK Configuration
android.api = 33
android.minapi = 21
android.ndk = 25b
android.archs = arm64-v8a

# AdMob SDK Integration
android.gradle_dependencies = com.google.android.gms:play-services-ads:22.6.0
android.meta_data = com.google.android.gms.ads.APPLICATION_ID=ca-app-pub-3940256099942544~3347511713

# Android Settings
android.copy_libs = 1
android.enable_androidx = True

[buildozer]
log_level = 2
warn_on_root = 1
