import streamlit as st
from groq import Groq
from pypdf import PdfReader

# ==================================
# PAGE CONFIG
# ==================================

st.set_page_config(
    page_title="AI PDF Assistant",
    page_icon="📄",
    layout="wide"
)

# ==================================
# CUSTOM CSS
# ==================================

st.markdown("""
<style>

.main {
    padding-top: 1rem;
}

.stChatMessage {
    border-radius: 12px;
    padding: 10px;
}

</style>
""", unsafe_allow_html=True)

# ==================================
# GROQ CLIENT
# ==================================

client = Groq(
    api_key=st.secrets["GROQ_API_KEY"]
)

# ==================================
# SESSION STATE
# ==================================

if "messages" not in st.session_state:
    st.session_state.messages = []

if "document_text" not in st.session_state:
    st.session_state.document_text = ""

# ==================================
# SIDEBAR
# ==================================

with st.sidebar:

    try:
        st.image(r"C:\Users\PITAMBER\OneDrive\STUDY\Main Projects\ChatGPT-Clone\assets\expert.webp", width=90)
    except:
        pass

    st.markdown("## 📄 AI PDF Assistant")

    st.markdown("---")

    uploaded_file = st.file_uploader(
        "Upload PDF",
        type=["pdf"]
    )

    if uploaded_file:

        reader = PdfReader(uploaded_file)

        text = ""

        for page in reader.pages:
            page_text = page.extract_text()

            if page_text:
                text += page_text

        # Limit document size
        text = text[:12000]

        st.session_state.document_text = text

        st.success("PDF Loaded Successfully")

        st.caption(uploaded_file.name)

    st.markdown("---")

    if st.button("📋 Generate Summary", use_container_width=True):

        if st.session_state.document_text:

            with st.spinner("Analyzing document..."):

                summary_response = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[
                        {
                            "role": "system",
                            "content":
                            f"""
                            Summarize this document clearly.

                            Document:
                            {st.session_state.document_text}
                            """
                        }
                    ]
                )

                st.session_state.messages.append(
                    {
                        "role": "assistant",
                        "content":
                        "## 📋 Document Summary\n\n"
                        + summary_response.choices[0].message.content
                    }
                )

                st.rerun()

        else:
            st.warning("Upload a PDF first.")

    if st.button("➕ New Chat", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

    st.markdown("---")

    st.caption("Powered by Groq • Llama 3.3")

# ==================================
# HEADER
# ==================================

st.markdown(
    """
    <h1 style='text-align:center'>
    📄 AI PDF Assistant
    </h1>
    """,
    unsafe_allow_html=True
)

st.caption("Upload a PDF and ask questions about it")

# ==================================
# WELCOME SCREEN
# ==================================

if (
    len(st.session_state.messages) == 0
    and st.session_state.document_text == ""
):

    st.info("👈 Upload a PDF from the sidebar to begin.")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
        ### Examples

        - Summarize this document
        - Explain chapter 2
        - Extract key points
        """)

    with col2:
        st.markdown("""
        ### More Examples

        - Generate interview questions
        - Create quiz questions
        - Explain difficult concepts
        """)

# ==================================
# DISPLAY CHAT HISTORY
# ==================================

for message in st.session_state.messages:

    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# ==================================
# USER INPUT
# ==================================

prompt = st.chat_input(
    "Ask questions about the uploaded PDF..."
)

# ==================================
# CHAT
# ==================================

if prompt:

    st.session_state.messages.append(
        {
            "role": "user",
            "content": prompt
        }
    )

    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):

        with st.spinner("Thinking..."):

            try:

                messages = []

                if st.session_state.document_text:

                    messages.append(
                        {
                            "role": "system",
                            "content":
                            f"""
                            You are an AI PDF Assistant.

                            Answer questions using ONLY
                            the uploaded document.

                            If the answer is not found,
                            say:

                            "I could not find that information in the document."

                            Document:
                            {st.session_state.document_text}
                            """
                        }
                    )

                for msg in st.session_state.messages:
                    messages.append(
                        {
                            "role": msg["role"],
                            "content": msg["content"]
                        }
                    )

                response = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=messages,
                    temperature=0.5,
                    max_tokens=1024
                )

                answer = response.choices[0].message.content

                st.markdown(answer)

                st.session_state.messages.append(
                    {
                        "role": "assistant",
                        "content": answer
                    }
                )

            except Exception as e:

                st.error(f"Error: {e}")
st.sidebar.markdown("""
<style>

.profile-card{
    background:#29446d;
    border-radius:20px;
    padding:25px;
    border:1px solid rgba(255,255,255,.15);
    margin-top:20px;
}

.profile-name{
    color:white;
    font-size:24px;
    font-weight:700;
    margin-bottom:10px;
}

.profile-role{
    color:#dbeafe;
    font-size:16px;
}

.portfolio{
    background:#155e75;
    color:white;
    padding:14px;
    border-radius:12px;
    text-align:center;
    font-weight:bold;
    margin-top:20px;
}

.footer{
    position:fixed;
    bottom:20px;
    left:50%;
    transform:translateX(-50%);
    color:#6B7280;
    font-size:15px;
    z-index:999;
}

.footer b{
    color:#2563EB;
}

</style>

<div class="profile-card">

<div class="profile-name">
🧑‍💻 Pitamber Raneesh Joga
</div>

<div class="profile-role">
AI & Machine Learning Student
</div>

</div>

<div class="portfolio">
⭐ Portfolio Project
</div>

""", unsafe_allow_html=True)


st.markdown("""
<div class="footer">
Made with ❤️ by <b>Raneesh</b>
</div>
""", unsafe_allow_html=True)