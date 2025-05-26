import os
import time
import subprocess
import ctypes
from pywinauto.application import Application

# 隱藏滑鼠游標
ctypes.windll.user32.ShowCursor(False)

# 要開啟的網址
url = "https://smartgoplusu.hpicorp.com.tw/tv"

# 嘗試的 Chrome 安裝路徑
possible_paths = [
    r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"
]

# 自動尋找 chrome.exe
chrome_path = None
for path in possible_paths:
    if os.path.exists(path):
        chrome_path = f'"{path}"'
        break

if chrome_path is None:
    print("❌ 找不到 Chrome 安裝路徑")
    exit(1)

# 啟動 Chrome
print("🚀 啟動 Chrome 中...")
command = f'{chrome_path} --start-fullscreen {url}'
subprocess.Popen(command, shell=True)

# 等待 Chrome 開啟
time.sleep(6)

# 嘗試連接並全螢幕
try:
    print("🔍 嘗試連接 Chrome 視窗...")
    app = Application(backend="uia").connect(title_re=".*Chrome.*", timeout=10)
    chrome_window = app.window(title_re=".*Chrome.*")

    chrome_window.set_focus()
    time.sleep(1)
    chrome_window.type_keys("{F11}")
    print("✅ 已送出 F11 進入全螢幕模式")
    time.sleep(1)

    print("🔁 第二次送出 F11")
    chrome_window.type_keys("{F11}")

except Exception as e:
    print("⚠️ 找不到 Chrome 視窗或全螢幕切換失敗：", e)
