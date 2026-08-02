[app]

# (str) Title of your application
title = FixIt Assistant

# (str) Package name
package.name = fixitassistant

# (str) Package domain (vendor)
package.domain = com.rohit

# (str) Source code where the main.py live
source.dir = .

# (list) Source files to include
source.include_exts = py,png,jpg,kv,atlas,wav,mp3

# (str) Application version
version = 1.0.0

# (list) Application requirements
# Fixed: Added plyer and PIL/Pillow for image processing and hardware controls
requirements = hostpython3==3.11.0,python3==3.11.0,kivy==2.3.0,kivymd==1.2.0,requests,urllib3,certifi,charset-normalizer,idna,plyer,pillow

# (str) Icon of the application
icon.filename = logo.png

# (list) Supported orientations
orientation = portrait

# (bool) Indicate if the application should be fullscreen or not
fullscreen = 0

# (list) Permissions (Camera, Mic, Storage & Internet)
android.permissions = INTERNET,CAMERA,RECORD_AUDIO,READ_MEDIA_IMAGES,READ_EXTERNAL_STORAGE,WRITE_EXTERNAL_STORAGE

# (int) Target Android API
android.api = 33

# (int) Minimum API supported
android.minapi = 21

# (str) Android NDK version
android.ndk = 25b

# (list) Supported Architectures (Enables APK to work smoothly on all modern smartphones)
android.archs = arm64-v8a, armeabi-v7a

# (bool) Accept Android SDK Licenses automatically
android.accept_sdk_license = True

[buildozer]
log_level = 2
warn_on_root = 1