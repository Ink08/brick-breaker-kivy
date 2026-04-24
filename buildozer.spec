[app]
title = BrickBreaker
package.name = brickbreaker
package.domain = org.test

version = 1.0   # ✅ THIS LINE FIXES ERROR

source.dir = .
source.include_exts = py,png,jpg,kv,mp3,wav

requirements = python3,kivy

orientation = portrait
fullscreen = 1

android.api = 31
android.minapi = 21

android.permissions = INTERNET
