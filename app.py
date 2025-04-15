import streamlit as st

st.markdown("""
    <style>
    .chat-row { display: flex; align-items: flex-start; margin-bottom: 10px; }
    .chat-row.user { justify-content: flex-end; }
    .chat-row.ai { justify-content: flex-start; }
    .chat-bubble { max-width: 80%; padding: 8px 12px; border-radius: 18px; line-height: 1.3; font-size: 14px; white-space: pre-wrap; word-wrap: break-word; }
    .chat-bubble.user { background-color: #C2F4C6; color: black; border-bottom-right-radius: 0px; margin-right: 4px; }
    .chat-bubble.ai { background-color: #F0F0F0; color: black; border-bottom-left-radius: 0px; margin-left: 4px; }
    .profile-icon { font-size: 22px; margin: 0 6px; }
    .name { font-size: 11px; margin: 2px 0; font-weight: bold; }
    </style>
""", unsafe_allow_html=True)

USER_NAME = "คุณ"
USER_ICON = "🐵"
AI_NAME = "AI"
AI_ICON = "🤖"

if "test_messages" not in st.session_state:
    st.session_state.test_messages = []

st.title("Minimal Chat Test")

for msg in st.session_state.test_messages:
    align = "user" if msg["role"] == "user" else "ai"
    name = USER_NAME if align == "user" else AI_NAME
    icon = USER_ICON if align == "user" else AI_ICON
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

prompt = st.chat_input("พิมพ์ข้อความทดสอบ...")
if prompt:
    st.session_state.test_messages.append({"role": "user", "text": prompt})
    st.markdown(f"""
    <div class="chat-row user">
        <div>
            <div class="name">{USER_NAME}</div>
            <div class="chat-bubble user">{prompt}</div>
        </div>
        <div class="profile-icon">{USER_ICON}</div>
    </div>
    """, unsafe_allow_html=True)
    st.session_state.test_messages.append({"role": "ai", "text": f"AI ตอบว่า: {prompt} เช่นกัน!"})
    st.markdown(f"""
    <div class="chat-row ai">
        <div class="profile-icon">{AI_ICON}</div>
        <div>
            <div class="name">{AI_NAME}</div>
            <div class="chat-bubble ai">AI ตอบว่า: {prompt} เช่นกัน!</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
