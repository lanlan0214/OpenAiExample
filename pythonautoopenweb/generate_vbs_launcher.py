import os

# 取得 auto.exe 的絕對路徑
exe_path = os.path.abspath("auto.exe")

# vbs 檔內容
vbs_content = f'''Set WshShell = CreateObject("WScript.Shell")
WshShell.Run chr(34) & "{exe_path}" & chr(34), 0
'''

# 輸出 vbs 到目前資料夾
with open("auto_launcher.vbs", "w", encoding="utf-8") as f:
    f.write(vbs_content)

print("✅ 已建立 auto_launcher.vbs，內容如下：")
print(vbs_content)
