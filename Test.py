import openai
import os
import time
import streamlit as st
from dotenv import load_dotenv
import datetime

# 載入 API Key
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

# 檢查 API Key 是否載入
if not api_key:
    st.error("❌ 找不到 OPENAI_API_KEY，請檢查 .env 設定")
    st.stop()

# 創建 OpenAI 客戶端
client = openai.OpenAI(api_key=api_key)

def diagnose_computer_issue(issue_description, model_choice, max_retries=3):
    """ 使用 OpenAI API 診斷電腦硬體問題，並支援不同模型 """
    retries = 0
    start = datetime.datetime.now()

    # ✅ 建立進度條
    progress_text = "🧠 診斷中，請稍候..."
    progress_bar = st.progress(0, text=progress_text)

    while retries < max_retries:
        try:
            # 模擬進度條前段等待
            for percent in range(0, 30, 10):
                time.sleep(0.2)
                progress_bar.progress(percent, text=progress_text)

            # GPT API 呼叫
            response = client.chat.completions.create(
                model=model_choice,  # 使用者選擇的模型
                messages=[
                    {"role": "system", "content": "你是一名專業的電腦維修技術人員，請根據用戶描述的問題提供診斷建議。"},
                    {"role": "user", "content": f"我的電腦有問題，描述如下:\n{issue_description}"}
                ],
                max_tokens=700,
                # 如果想要回覆固定長度，可以設置這個參數
                # temperature=0.0,  # 設置為 0.0 可以獲得更一致的結果
                # 這裡設置為 0.7 以獲得更具創造性的回答
                temperature=0.7
            )

            # 模擬進度條完成階段
            for percent in range(30, 101, 20):
                time.sleep(0.1)
                progress_bar.progress(percent, text=progress_text)

            end = datetime.datetime.now()
            st.write(f"⚙️ GPT API 呼叫耗時: {(end - start).total_seconds():.2f} 秒")

            # 清除進度條
            progress_bar.empty()
            return response.choices[0].message.content

        except openai.RateLimitError:
            st.warning("⚠️ API 速率限制，等待 10 秒後重試...")
            time.sleep(10)
            retries += 1

    progress_bar.empty()
    return "❌ 無法診斷，請稍後再試。"

# Streamlit UI 設定
st.title("💻 電腦硬體診斷助手")
st.write("請輸入你的電腦問題，系統將幫你診斷可能的原因與解決方案。")

# **新增 GPT 模型選擇**
model_choice = st.radio("選擇 GPT 模型", ["gpt-3.5-turbo", "gpt-4-turbo", "gpt-4.1"], index=0)

# 使用者輸入問題
user_input = st.text_area("請描述你的電腦問題，例如『開機黑屏但風扇還在轉』")

# 按鈕觸發診斷
if st.button("開始診斷"):
    if user_input.strip():
        st.info(f"🔍 使用 `{model_choice}` 診斷中，請稍候...")
        diagnosis = diagnose_computer_issue(user_input, model_choice)
        st.success("✅ 診斷結果:")
        st.write(diagnosis)
    else:
        st.warning("⚠️ 請輸入你的電腦問題！")
