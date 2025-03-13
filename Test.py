import openai
import os
import time
import streamlit as st
from dotenv import load_dotenv

# 載入 API Key
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

# 檢查 API Key 是否載入
if not api_key:
    st.error("❌ 找不到 OPENAI_API_KEY，請檢查 .env 設定")
    st.stop()

# 創建 OpenAI 客戶端
client = openai.OpenAI(api_key=api_key)

def diagnose_computer_issue(issue_description, max_retries=3):
    """ 使用 OpenAI API 診斷電腦硬體問題 """
    retries = 0
    while retries < max_retries:
        try:
            response = client.chat.completions.create(
                # # 最便宜
                model="gpt-3.5-turbo", 
                # 使用 GPT-4 模型
                # model="gpt-4-turbo",  
                messages=[
                    {"role": "system", "content": "你是一名專業的電腦維修技術人員，請根據用戶描述的問題提供診斷建議。"},
                    {"role": "user", "content": f"我的電腦有問題，描述如下:\n{issue_description}"}
                ],
                max_tokens=600,  # 限制 Token 避免被濫用
                temperature=0.7  # 讓回應有點隨機性，但不會過於發散
            )
            return response.choices[0].message.content
        except openai.RateLimitError:
            st.warning("⚠️ API 速率限制，等待 10 秒後重試...")
            time.sleep(10)  # 等待 10 秒後重試
            retries += 1
    return "❌ 無法診斷，請稍後再試。"

# Streamlit UI 設定
st.title("💻 電腦硬體診斷助手")
st.write("請輸入你的電腦問題，系統將幫你診斷可能的原因與解決方案。")

# 使用者輸入問題
user_input = st.text_area("請描述你的電腦問題，例如『開機黑屏但風扇還在轉』")

# 按鈕觸發診斷
if st.button("開始診斷"):
    if user_input.strip():  # 確保使用者有輸入
        st.info("🔍 診斷中，請稍候...")
        diagnosis = diagnose_computer_issue(user_input)
        st.success("✅ 診斷結果:")
        st.write(diagnosis)
    else:
        st.warning("⚠️ 請輸入你的電腦問題！")
