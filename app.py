import streamlit as st
import google.generativeai as genai

# นี่คือ CSS ที่ช่วยจัดตำแหน่งให้เหมือนแชทจริง
st.markdown("""
    <style>
    .chat-row {
        display: flex;
        align-items: flex-start;
        margin-bottom: 12px;
    }
    .chat-row.user {
        justify-content: flex-end;
    }
    .chat-row.ai {
        justify-content: flex-start;
    }
    .chat-bubble {
        max-width: 70%;
        padding: 10px 15px;
        border-radius: 18px;
        line-height: 1.4;
        font-size: 15px;
    }
    .chat-bubble.user {
        background-color: #C2F4C6;
        color: black;
        border-bottom-right-radius: 0px;
    }
    .chat-bubble.ai {
        background-color: #F0F0F0;
        color: black;
        border-bottom-left-radius: 0px;
    }
    .profile-icon {
        font-size: 28px;
        margin: 0 8px;
    }
    .name {
        font-size: 12px;
        margin: 2px 0;
        font-weight: bold;
    }
    </style>
""", unsafe_allow_html=True)

# ตั้งชื่อ + อีโมจิ
USER_NAME = "คุณ"
USER_ICON = "🐵"
AI_NAME = "AI Sao San Suay"
AI_ICON = "🤖"

# เริ่มใช้งานโมเดล
try:
    key = st.secrets['gemini_api_key']
    genai.configure(api_key=key)
    model = genai.GenerativeModel('gemini-2.0-flash-lite')

    if "chat" not in st.session_state:
        st.session_state.chat = model.start_chat(history=[])
        st.session_state.messages = []

    st.title("AI SAO SAN SUAY ✨💗")

    # แสดงแชทย้อนหลัง
    for msg in st.session_state.messages:
        if msg["role"] == "user":
            icon = USER_ICON
            name = USER_NAME
            align = "user"
        else:
            icon = AI_ICON
            name = AI_NAME
            align = "ai"

        st.markdown(f"""
        <div class="chat-row {align}">
            {'<div class="profile-icon">' + icon + '</div>' if align == 'ai' else ''}
            <div>
                <div class="name">{name}</div>
                <div class="chat-bubble {align}">{msg['text']}</div>
            </div>
            {'<div class="profile-icon">' + icon + '</div>' if align == 'user' else ''}
        </div>
        """, unsafe_allow_html=True)

    # รับข้อความใหม่
    prompt = st.chat_input("พิมพ์ข้อความของคุณที่นี่...")

    if prompt:
        # เพิ่มข้อความผู้ใช้
        st.session_state.messages.append({"role": "user", "text": prompt})

        # ส่งให้โมเดลตอบ
        response = st.session_state.chat.send_message(prompt)

        # เพิ่มข้อความ AI
        st.session_state.messages.append({"role": "ai", "text": response.text})

        # รีเฟรชหน้าจอเพื่อโชว์ข้อความล่าสุด
        st.experimental_rerun()

except Exception as e:
    st.error(f"เกิดข้อผิดพลาด: {e}")
