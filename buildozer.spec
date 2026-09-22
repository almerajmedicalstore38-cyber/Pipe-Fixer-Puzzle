[app]

# (str) Title of your application
title = Pipe Fixer Puzzle

# (str) Package name
package.name = pipefixerpuzzle

# (str) Package domain (needed for android/ios packaging)
package.domain = com.app.pipefixer

# (str) Source code where the main.py live
source.dir = .

# (list) Source files to include (leave empty to include all the files)
source.include_exts = py,png,jpg,jpeg,ttf,wav,ogg,mp3,json

# (str) Application versioning
version = 1.0.0

# (list) Application requirements
# Python 3.11 lock kiya gaya hai taaki longintrepr.h ka error na aaye
requirements = python3==3.11.5,hostpython3==3.11.5,pygame,pyjnius,android,openssl,requests,urllib3,certifi,charset-normalizer,idna

# (str) Custom source folders for requirements
# (list) Garden requirements

# (str) Presplash of the application
# presplash.filename = %(source.dir)s/data/presplash.png

# (str) Icon of the application
# icon.filename = %(source.dir)s/data/icon.png

# (list) Supported orientations
orientation = portrait

# (bool) Indicate if the application should be fullscreen or not
fullscreen = 1

# (list) Permissions
android.permissions = INTERNET,ACCESS_NETWORK_STATE

# (int) Target Android API, should be as high as possible.
android.api = 33

# (int) Minimum API required
android.minapi = 21

# (int) Android SDK version to use
android.sdk = 33

# (str) Android NDK version to use
android.ndk = 25b

# (bool) Use --private data storage (True) or --dir public storage (False)
android.private_storage = True

# (list) List of Java .jar files to add to the libs
# android.add_jars = foo.jar,bar.jar

# (list) Gradle dependencies to add
android.gradle_dependencies = com.google.android.gms:play-services-ads:22.6.0

# (list) Android AAR dependencies to add
# android.add_aars =

# (list) Java classes to add (e.g. com.models.Test)
# android.add_src =

# (str) python-for-android git clone directory (if empty, it will be automatically cloned from github)
# p4a.source_dir =

# (list) The Android architectures to build for
android.archs = arm64-v8a

# (bool) Enable AndroidX support. Required for AdMob and modern libraries.
android.androidx = True

# (str) Android entry point, default is ok for Kivy/Pygame
# android.entrypoint = org.kivy.android.PythonActivity

[buildozer]

# (int) Log level (0 = error only, 1 = info, 2 = debug (with command output))
log_level = 2

# (int) Display warning if buildozer is run as root (0 = error, 1 = warning)
warn_on_root = 1
