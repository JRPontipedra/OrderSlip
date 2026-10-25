ORDER SLIP MAKER - Kivy/Python starter project

Features:
- No unit price or price fields
- Order type selector: Retail or Wais Misis
- Notes / Extra Text input
- Add/remove item rows with Quantity and Article/Description
- Export order slip as PNG
- Main input and export work offline
- Buildozer config included for Android APK build

Windows test:
  python -m pip install -r requirements.txt
  python main.py

Output on Windows:
  %USERPROFILE%\OrderSlipExports

Android APK:
Build using Linux/WSL2 with Buildozer. Install/configure Buildozer and Android SDK/NDK, then:
  buildozer android debug

Important:
This is a starter source project, not a ready-built APK. Buildozer needs a supported Linux/WSL environment and internet for initial Android build dependencies. Android sharing to Messenger needs a FileProvider/content URI integration for modern Android; the included share button currently reports this limitation rather than pretending sharing is fully configured. Exported image is saved to app-private storage on Android.


Gallery save update:
- Exported PNG files are saved to /storage/emulated/0/Pictures/OrderSlipMaker on Android when shared storage access is available.
- Open Gallery/Photos and look for the OrderSlipMaker album/folder. If it does not appear immediately, close/reopen Gallery or check the Pictures folder in the file manager.
- On Android, allow Pydroid 3 access to photos/media or files when prompted. Newer Android versions may restrict direct folder access; the code falls back to app-private storage if saving to Pictures fails.
