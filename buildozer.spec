[app]

# (str) Title of your application
title = Pipe Fixer

# (str) Package name
package.name = pipefixer

# (str) Package domain (needed for android packaging)
package.domain = com.sharafat

# (str) Source code where the main.py live
source.dir = .

# (list) Source files to include (leave empty to include all the files)
source.include_exts = py,png,jpg,jpeg,ttf,otf,wav,mp3,ogg,json

# (list) List of directory to include (leave empty to include all the files)
source.include_dirs = assets

# (str) Application versioning
version = 1.0.0

# (list) Application requirements
# Pygame, Pyjnius, OpenSSL, Network libraries, aur Core Android runtime
requirements = python3,pygame,pyjnius,android,openssl,requests,urllib3,certifi,charset_normalizer,idna

# (list) Permissions
android.permissions = INTERNET, ACCESS_NETWORK_STATE

# (str) Bootstrap for PyGame games
p4a.bootstrap = sdl2

# -----------------------------------------------------------------------------
# Android specific configuration
# -----------------------------------------------------------------------------

# (int) Target Android API
android.api = 33

# (int) Minimum API supported
android.minapi = 21

# (str) Android NDK version
android.ndk = 25.1.8937393

# (list) Supported Architectures
android.archs = arm64-v8a

# (list) Gradle dependencies for Google AdMob SDK
# Ye line AdMob Java SDK ko APK ke sath bundle karti hai (Crash hone se bachane ke liye)
android.gradle_dependencies = com.google.android.gms:play-services-ads:22.6.0

# (list) Application Meta-data for Google AdMob App ID
# Test App ID (Production me ise apne real AdMob App ID se badlein: ca-app-pub-xxxxxxxx~xxxxxxxx)
android.meta_data = com.google.android.gms.ads.APPLICATION_ID=ca-app-pub-3940256099942544~3347511713

# (bool) Copy external libraries into APK
android.copy_libs = 1

# (bool) Enable AndroidX support
android.enable_androidx = True

# (list) Keep classes for ProGuard / Minification
android.extra_manifest_application = <meta-data android:name="com.google.android.gms.version" android:value="@integer/google_play_services_version" />

# -----------------------------------------------------------------------------
# Buildozer Global Options
# -----------------------------------------------------------------------------

[buildozer]

# (int) Log level (0 = error only, 1 = info, 2 = debug (with command output))
log_level = 2

# (int) Display warning if buildozer is run as root (0 = disable, 1 = enable)
warn_on_root = 1

