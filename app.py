import streamlit as st
import google.generativeai as genai

# Add custom CSS for chat alignment
st.markdown("""
    <style>
    .chat-message.user {
        text-align: right;
    }
    .chat-message.assistant {
        text-align: left;
    }
    .chat-bubble {
        display: inline-block;
        padding: 10px 15px;
        border-radius: 15px;
        margin: 5px 0;
        max-width: 75%;
    }
    .chat-message.user .chat-bubble {
        background-color: #DCF8C6;
        color: black;
    }
    .chat-message.assistant .chat-bubble {
        background-color: #F1F0F0;
        color: black;
    }
    </style>
""", unsafe_allow_html=True)

try:
    key = st.secrets['gemini_api_key']
    genai.configure(api_key=key)
    model = genai.GenerativeModel('gemini-2.0-flash-lite')

    if "chat" not in st.session_state:
        st.session_state.chat = model.start_chat(history=[])

    st.title('AI SAO SAN SUAY✨💗')

    def role_to_streamlit(role: str) -> str:
        return 'assistant' if role == 'model' else role

    for message in st.session_state.chat.history:
        role = role_to_streamlit(message.role)
        with st.chat_message(role):
            st.markdown(
                f'<div class="chat-bubble">{message.parts[0].text}</div>',
                unsafe_allow_html=True
            )

    if prompt := st.chat_input("Text Here"):
        with st.chat_message('user'):
            st.markdown(
                f'<div class="chat-bubble">{prompt}</div>',
                unsafe_allow_html=True
            )
        response = st.session_state.chat.send_message(prompt)
        with st.chat_message('assistant'):
            st.markdown(
                f'<div class="chat-bubble">{response.text}</div>',
                unsafe_allow_html=True
            )

except Exception as e:
    st.error(f'An error occurred: {e}')
