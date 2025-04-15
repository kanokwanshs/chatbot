import streamlit as st
import google.generativeai as genai
import html

# CSS แชทน่ารัก ๆ
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
        white-space: pre-wrap;
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

# ข้อมูลผู้พูด
USER_NAME = "คุณ"
USER_ICON = "🐵"
AI_NAME = "AI Sao San Suay"
AI_ICON = "🤖"

# เริ่มการตั้งค่า
try:
    key = st.secrets['gemini_api_key']
    genai.configure(api_key=key)
    model = genai.GenerativeModel('gemini-2.0-flash-lite')

    if "chat" not in st.session_state:
        st.session_state.chat = model.start_chat(history=[])
        st.session_state.messages = []

    st.title("AI SAO SAN SUAY ✨💗")

    # รับข้อความใหม่
    prompt = st.chat_input("พิมพ์ข้อความของคุณที่นี่...")

    if prompt:
        # แสดงข้อความของผู้ใช้ "ทันที"
        safe_prompt = html.escape(prompt)
        st.markdown(f"""
        <div class="chat-row user">
            <div>
                <div class="name">{USER_NAME}</div>
                <div class="chat-bubble user">{safe_prompt}</div>
            </div>
            <div class="profile-icon">{USER_ICON}</div>
        </div>
        """, unsafe_allow_html=True)

        # เก็บใน memory
        st.session_state.messages.append({"role": "user", "text": prompt})

        # ส่งให้โมเดลตอบ
        response = st.session_state.chat.send_message(prompt)

        # เก็บข้อความตอบกลับ
        st.session_state.messages.append({"role": "ai", "text": response.text})

    # แสดงประวัติ (ยกเว้นข้อความล่าสุด เพราะโชว์ไปแล้ว)
    for msg in st.session_state.messages[:-2 if prompt else None]:
        if msg["role"] == "user":
            icon = USER_ICON
            name = USER_NAME
            align = "user"
        else:
            icon = AI_ICON
            name = AI_NAME
            align = "ai"

        safe_text = html.escape(msg['text'])

        st.markdown(f"""
        <div class="chat-row {align}">
            {'<div class="profile-icon">' + icon + '</div>' if align == 'ai' else ''}
            <div>
                <div class="name">{name}</div>
                <div class="chat-bubble {align}">{safe_text}</div>
            </div>
            {'<div class="profile-icon">' + icon + '</div>' if align == 'user' else ''}
        </div>
        """, unsafe_allow_html=True)

    # ถ้าเพิ่งพิมพ์มา ให้แสดงคำตอบของ AI ต่อท้าย
    if prompt:
        safe_reply = html.escape(response.text)
        st.markdown(f"""
        <div class="chat-row ai">
            <div class="profile-icon">{AI_ICON}</div>
            <div>
                <div class="name">{AI_NAME}</div>
                <div class="chat-bubble ai">{safe_reply}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

except Exception as e:
    st.error(f"เกิดข้อผิดพลาด: {e}")
