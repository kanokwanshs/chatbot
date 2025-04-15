import streamlit as st
import google.generativeai as genai
import html

# 🎨 CSS สไตล์แชท
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
        max-width: 90%;
        padding: 10px 15px;
        border-radius: 18px;
        line-height: 1;
        font-size: 14px;
        white-space: pre-wrap;
        word-wrap: break-word;
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
        font-size: 20px;
        margin: 0 8px;
    }
    .name {
        font-size: 10px;
        margin: 2px 0;
        font-weight: bold;
    }
    </style>
""", unsafe_allow_html=True)

# 🧍‍♀️ ตั้งชื่อกับอีโมจิ
USER_NAME = "คุณ"
USER_ICON = "🐵"
AI_NAME = "AI Sao San Suay"
AI_ICON = "🤖"

# 🧠 ตั้งค่าโมเดล Gemini
try:
    key = st.secrets['gemini_api_key']
    genai.configure(api_key=key)
    model = genai.GenerativeModel('gemini-2.0-flash-lite')

    # สร้าง Session ครั้งแรก
    if "chat" not in st.session_state:
        st.session_state.chat = model.start_chat(history=[])
        st.session_state.messages = []

    # หัวข้อ
    st.title("AI SAO SAN SUAY ✨💗")

    # ➕ แสดงประวัติการสนทนา (ยกเว้น 2 อันล่าสุดถ้ากำลังตอบ)
    for msg in st.session_state.messages[:-2] if len(st.session_state.messages) >= 2 else st.session_state.messages:
        align = "user" if msg["role"] == "user" else "ai"
        name = USER_NAME if align == "user" else AI_NAME
        icon = USER_ICON if align == "user" else AI_ICON
        safe_text = html.escape(msg["text"])

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

    # 📥 พิมพ์คำถามใหม่
    prompt = st.chat_input("พิมพ์ข้อความของคุณที่นี่...")

    if prompt:
        # แสดงข้อความผู้ใช้ทันที
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

        # เก็บลง session
        st.session_state.messages.append({"role": "user", "text": prompt})

        # ส่งให้ AI ตอบ
        response = st.session_state.chat.send_message(prompt)
        st.session_state.messages.append({"role": "ai", "text": response.text})

        # แสดงคำตอบ AI
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
