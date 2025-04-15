import streamlit as st
import google.generativeai as genai

# Custom CSS for better chat styling
st.markdown("""
    <style>
    .chat-container {
        display: flex;
        margin: 10px 0;
    }
    .chat-container.user {
        justify-content: flex-end;
    }
    .chat-container.assistant {
        justify-content: flex-start;
    }
    .chat-bubble {
        padding: 10px 15px;
        border-radius: 18px;
        max-width: 75%;
        word-wrap: break-word;
    }
    .user .chat-bubble {
        background-color: #C2F4C6;
        color: black;
        border-bottom-right-radius: 2px;
    }
    .assistant .chat-bubble {
        background-color: #F0F0F0;
        color: black;
        border-bottom-left-radius: 2px;
    }
    .profile-pic {
        width: 40px;
        height: 40px;
        border-radius: 50%;
        object-fit: cover;
        margin: 0 10px;
    }
    .chat-name {
        font-size: 13px;
        margin: 2px 0;
        font-weight: bold;
    }
    </style>
""", unsafe_allow_html=True)

# URLs to profile pictures (can replace with your own image URLs)
user_img_url = "https://i.imgur.com/8Km9tLL.png"  # you can change this to your own image
ai_img_url = "https://i.imgur.com/Vz7jE0O.png"     # AI cute pic

try:
    key = st.secrets['gemini_api_key']
    genai.configure(api_key=key)
    model = genai.GenerativeModel('gemini-2.0-flash-lite')

    if "chat" not in st.session_state:
        st.session_state.chat = model.start_chat(history=[])

    st.title('AI SAO SAN SUAY✨💗')

    def display_message(role, name, avatar, text):
        alignment = 'user' if role == 'user' else 'assistant'
        st.markdown(f"""
            <div class="chat-container {alignment}">
                {"<img src='" + avatar + "' class='profile-pic' />" if alignment == 'assistant' else ""}
                <div>
                    <div class="chat-name">{name}</div>
                    <div class="chat-bubble">{text}</div>
                </div>
                {"<img src='" + avatar + "' class='profile-pic' />" if alignment == 'user' else ""}
            </div>
        """, unsafe_allow_html=True)

    # Display previous chat history
    for msg in st.session_state.chat.history:
        role = 'user' if msg.role == 'user' else 'assistant'
        name = "คุณ" if role == 'user' else "AI Sao San Suay ✨"
        avatar = user_img_url if role == 'user' else ai_img_url
        display_message(role, name, avatar, msg.parts[0].text)

    # Chat input
    if prompt := st.chat_input("พิมพ์ข้อความที่นี่..."):
        # Show user message
        display_message('user', "คุณ", user_img_url, prompt)
        # Get AI response
        response = st.session_state.chat.send_message(prompt)
        # Show AI message
        display_message('assistant', "AI Sao San Suay ✨", ai_img_url, response.text)

except Exception as e:
    st.error(f'เกิดข้อผิดพลาดจ้า: {e}')

