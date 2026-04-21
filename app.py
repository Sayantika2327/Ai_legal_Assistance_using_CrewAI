import streamlit as st
from dotenv import load_dotenv
from crew import legal_assistant_crew
from groq import Groq
import os

load_dotenv()

st.set_page_config(page_title="AI Legal Assistant", page_icon="⚖️", layout="wide")

# ── Custom CSS ──────────────────────────────────────────────────────────────
st.markdown("""
<style>
    .chat-bubble-user {
        background: #1e40af;
        color: white;
        padding: 10px 14px;
        border-radius: 16px 16px 4px 16px;
        margin: 6px 0;
        max-width: 85%;
        margin-left: auto;
        font-size: 0.9rem;
    }
    .chat-bubble-bot {
        background: #f1f5f9;
        color: #1e293b;
        padding: 10px 14px;
        border-radius: 16px 16px 16px 4px;
        margin: 6px 0;
        max-width: 85%;
        font-size: 0.9rem;
    }
    .chat-container {
        height: 420px;
        overflow-y: auto;
        padding: 10px;
        border: 1px solid #e2e8f0;
        border-radius: 12px;
        background: #ffffff;
        margin-bottom: 10px;
    }
    .section-divider {
        border-top: 2px solid #e2e8f0;
        margin: 20px 0;
    }
</style>
""", unsafe_allow_html=True)

# ── Session state ───────────────────────────────────────────────────────────
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "legal_draft" not in st.session_state:
    st.session_state.legal_draft = None

# ── Layout: two columns ─────────────────────────────────────────────────────
left_col, right_col = st.columns([3, 2], gap="large")

# ════════════════════════════════════════════════════════════════════════════
# LEFT COLUMN — Legal Assistant
# ════════════════════════════════════════════════════════════════════════════
with left_col:
    st.title("⚖️ Personal AI Legal Assistant")
    st.markdown(
        "Enter a legal problem in plain English. This assistant will help you:\n"
        "- Understand the legal issue\n"
        "- Find applicable IPC sections\n"
        "- Retrieve matching precedent cases\n"
        "- Generate a formal legal document"
    )

    with st.form("legal_form"):
        user_input = st.text_area("📝 Describe your legal issue:", height=200)
        submitted = st.form_submit_button("🔍 Run Legal Assistant")

    if submitted:
        if not user_input.strip():
            st.warning("Please enter a legal issue to analyze.")
        else:
            with st.spinner("🔎 Analyzing your case and preparing legal output..."):
                result = legal_assistant_crew.kickoff(inputs={"user_input": user_input})

            draft_text = result if isinstance(result, str) else str(result)
            st.session_state.legal_draft = draft_text

            # Seed the chatbot with context about this draft
            st.session_state.chat_history = [
                {
                    "role": "system",
                    "content": (
                        "You are a knowledgeable Indian legal assistant. "
                        "A legal complaint draft has been generated for the user. "
                        "Here is the full draft:\n\n"
                        f"{draft_text}\n\n"
                        "Answer the user's questions about the IPC sections mentioned, "
                        "legal terms, next steps, or anything related to this draft. "
                        "Be clear, helpful, and accurate. Cite specific IPC sections when relevant."
                    )
                }
            ]
            st.success("✅ Legal Assistant completed the workflow!")

    if st.session_state.legal_draft:
        st.subheader("📄 Final Output")
        st.markdown(st.session_state.legal_draft)


# ════════════════════════════════════════════════════════════════════════════
# RIGHT COLUMN — Chatbot
# ════════════════════════════════════════════════════════════════════════════
with right_col:
    st.title("💬 Legal Chatbot")

    if not st.session_state.legal_draft:
        st.info("🔎 Run the Legal Assistant first to generate a draft. Then you can ask questions about it here.")
    else:
        st.caption("Ask anything about the IPC sections, legal terms, or next steps in your draft.")

        # ── Chat display ────────────────────────────────────────────────────
        chat_html = '<div class="chat-container" id="chat-box">'
        for msg in st.session_state.chat_history:
            if msg["role"] == "user":
                chat_html += f'<div class="chat-bubble-user">🧑 {msg["content"]}</div>'
            elif msg["role"] == "assistant":
                chat_html += f'<div class="chat-bubble-bot">⚖️ {msg["content"]}</div>'
        chat_html += "</div>"
        st.markdown(chat_html, unsafe_allow_html=True)

        # ── Input ───────────────────────────────────────────────────────────
        with st.form("chat_form", clear_on_submit=True):
            user_question = st.text_input(
                "Your question:",
                placeholder="e.g. What does IPC Section 454 mean?",
                label_visibility="collapsed"
            )
            send = st.form_submit_button("Send ➤")

        if send and user_question.strip():
            # Append user message
            st.session_state.chat_history.append({
                "role": "user",
                "content": user_question
            })

            # Call Groq
            try:
                client = Groq(api_key=os.getenv("GROQ_API_KEY"))
                response = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=st.session_state.chat_history,
                    temperature=0.4,
                    max_tokens=1024,
                )
                bot_reply = response.choices[0].message.content
            except Exception as e:
                bot_reply = f"⚠️ Error contacting Groq API: {str(e)}"

            st.session_state.chat_history.append({
                "role": "assistant",
                "content": bot_reply
            })
            st.rerun()

        # ── Clear chat button ───────────────────────────────────────────────
        if st.button("🗑️ Clear Chat"):
            # Keep system message, clear conversation
            st.session_state.chat_history = [st.session_state.chat_history[0]]
            st.rerun()