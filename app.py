import streamlit as st
import google.generativeai as genai
import logging

# 🛠️ ตั้งค่า Logging (สำหรับ Debugging)
logging.basicConfig(level=logging.INFO)  # หรือระดับอื่นเช่น DEBUG, WARNING, ERROR

# 🎨 CSS สำหรับมือถือ (จากโค้ดเดิม)
st.markdown("""
    <style>
    .chat-row {
        display: flex;
        align-items: flex-start;
        margin-bottom: 10px;
    }
    .chat-row.user {
        justify-content: flex-end;
    }
    .chat-row.ai {
        justify-content: flex-start;
    }
    .chat-bubble {
        max-width: 80%;
        padding: 8px 12px;
        border-radius: 18px;
        line-height: 1.3;
        font-size: 14px;
        white-space: pre-wrap;
        word-wrap: break-word;
    }
    .chat-bubble.user {
        background-color: #C2F4C6;
        color: black;
        border-bottom-right-radius: 0px;
        margin-right: 4px;
    }
    .chat-bubble.ai {
        background-color: #F0F0F0;
        color: black;
        border-bottom-left-radius: 0px;
        margin-left: 4px;
    }
    .profile-icon {
        font-size: 22px;
        margin: 0 6px;
    }
    .name {
        font-size: 11px;
        margin: 2px 0;
        font-weight: bold;
    }
    </style>
""", unsafe_allow_html=True)

# 💬 ข้อมูลผู้พูด
USER_NAME = "คุณ"
USER_ICON = "🐵"
AI_NAME = "AI Sao San Suay"
AI_ICON = "🤖"

# ⚙️ เริ่มการตั้งค่า
try:
    # 🔑 ดึง API key จาก Secrets (สำคัญ!)
    key = st.secrets['gemini_api_key']
    genai.configure(api_key=key)
    model = genai.GenerativeModel('gemini-2.0-flash-lite')

    # 🔄 เริ่ม Chat Session (ถ้ายังไม่มี)
    if "chat" not in st.session_state:
        st.session_state.chat = model.start_chat(history=[])
        st.session_state.messages = []  # เก็บประวัติแชท

    # 🖼️ แสดง Title
    st.title("AI SAO SAN SUAY ✨💗")

    # 📜 แสดงประวัติการสนทนา (แสดงทุกข้อความที่เคยแชท)
    for msg in st.session_state.messages:
        align = "user" if msg["role"] == "user" else "ai"
        name = USER_NAME if align == "user" else AI_NAME
        icon = USER_ICON if align == "user" else AI_ICON
        # แสดงข้อความโดยใช้ st.markdown()
        st.markdown(f"""
        <div class="chat-row {align}">
            {'<div class="profile-icon">' + icon + '</div>' if align == 'ai' else ''}
            <div>
                <div class="name">{name}</div>
                <div class="chat-bubble {align}">{msg["text"]}</div>
            </div>
            {'<div class="profile-icon">' + icon + '</div>' if align == 'user' else ''}
        </div>
        """, unsafe_allow_html=True)

    # ✍️ พิมพ์คำถามใหม่
    prompt = st.chat_input("พิมพ์ข้อความของคุณที่นี่...")

    if prompt:
        # 👤 แสดง prompt ทันที (ข้อความผู้ใช้)
        st.markdown(f"""
        <div class="chat-row user">
            <div>
                <div class="name">{USER_NAME}</div>
                <div class="chat-bubble user">{prompt}</div>
            </div>
            <div class="profile-icon">{USER_ICON}</div>
        </div>
        """, unsafe_allow_html=True)

        # 💾 บันทึกข้อความผู้ใช้ลง session_state
        st.session_state.messages.append({"role": "user", "text": prompt})

        try:
            # 🤖 ส่งให้ AI
            response = st.session_state.chat.send_message(prompt)
            reply_text = response.text
            # 💾 บันทึกคำตอบ AI ลง session_state
            st.session_state.messages.append({"role": "ai", "text": reply_text})

            # 💬 แสดงคำตอบ AI
            st.markdown(f"""
            <div class="chat-row ai">
                <div class="profile-icon">{AI_ICON}</div>
                <div>
                    <div class="name">{AI_NAME}</div>
                    <div class="chat-bubble ai">{reply_text}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)

        except Exception as ai_error:
            # 🚨 จัดการ Error จาก Gemini API
            logging.error(f"Gemini API Error: {ai_error}")
            st.error(f"เกิดข้อผิดพลาดในการตอบกลับจาก AI: {ai_error}") # แสดง error ให้ user เห็น

except Exception as e:
    # 🚨 จัดการ Error ทั่วไป
    logging.exception(f"An unexpected error occurred: {e}")  # Log error อย่างละเอียด
    st.error(f"เกิดข้อผิดพลาด: {e}") # แสดง error ให้ user เห็น
