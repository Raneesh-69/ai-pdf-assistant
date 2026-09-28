import os
import streamlit as st

from groq import Groq
from pypdf import PdfReader


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="AI PDF Assistant",
    page_icon="📄",
    layout="wide"
)


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown(
    """
    <style>

    /* Main content */
    .main {
        padding-top: 1rem;
    }

    /* Chat messages */
    .stChatMessage {
        border-radius: 12px;
        padding: 10px;
    }

    /* Sidebar divider */
    .sidebar-divider {
        margin-top: 15px;
        margin-bottom: 15px;
        border: none;
        border-top: 1px solid rgba(128,128,128,0.25);
    }

    /* Download buttons */
    div.stDownloadButton > button {
        border-radius: 10px;
        font-weight: 600;
        transition: all 0.2s ease;
    }

    div.stDownloadButton > button:hover {
        transform: translateY(-2px);
    }

    /* Profile card */
    .profile-card {
        background: #29446d;
        border-radius: 20px;
        padding: 25px;
        border: 1px solid rgba(255,255,255,.15);
        margin-top: 20px;
    }

    .profile-name {
        color: white;
        font-size: 24px;
        font-weight: 700;
        margin-bottom: 10px;
    }

    .profile-role {
        color: #dbeafe;
        font-size: 16px;
    }

    .portfolio {
        background: #155e75;
        color: white;
        padding: 14px;
        border-radius: 12px;
        text-align: center;
        font-weight: bold;
        margin-top: 20px;
    }

    /* Footer */
    .footer {
        position: fixed;
        bottom: 20px;
        left: 50%;
        transform: translateX(-50%);
        color: #6B7280;
        font-size: 15px;
        z-index: 999;
    }

    .footer b {
        color: #2563EB;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# GROQ CLIENT
# ============================================================

try:

    # Streamlit Cloud
    if "GROQ_API_KEY" in st.secrets:
        groq_api_key = st.secrets["GROQ_API_KEY"]

    # Local fallback
    else:
        groq_api_key = os.getenv("GROQ_API_KEY")

    if not groq_api_key:
        st.error(
            "❌ GROQ_API_KEY not found. "
            "Add your Groq API key to Streamlit Secrets."
        )
        st.stop()

    client = Groq(
        api_key=groq_api_key
    )

except Exception as e:

    st.error(
        f"❌ Could not initialize Groq client: {e}"
    )

    st.stop()


# ============================================================
# MODEL
# ============================================================

MODEL_NAME = "openai/gpt-oss-120b"


# ============================================================
# SESSION STATE
# ============================================================

if "messages" not in st.session_state:
    st.session_state.messages = []

if "document_text" not in st.session_state:
    st.session_state.document_text = ""

if "document_name" not in st.session_state:
    st.session_state.document_name = ""


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    # --------------------------------------------------------
    # PROFILE IMAGE
    # --------------------------------------------------------

    profile_image = "assets/expert.webp"

    if os.path.exists(profile_image):

        st.image(
            profile_image,
            width=90
        )


    # --------------------------------------------------------
    # TITLE
    # --------------------------------------------------------

    st.markdown("## 📄 AI PDF Assistant")

    st.markdown("---")


    # --------------------------------------------------------
    # PDF UPLOAD
    # --------------------------------------------------------

    uploaded_file = st.file_uploader(
        "Upload PDF",
        type=["pdf"]
    )


    if uploaded_file:

        try:

            reader = PdfReader(uploaded_file)

            text = ""

            for page in reader.pages:

                page_text = page.extract_text()

                if page_text:
                    text += page_text + "\n"


            # ------------------------------------------------
            # LIMIT DOCUMENT SIZE
            # ------------------------------------------------

            text = text[:12000]


            # ------------------------------------------------
            # SAVE DOCUMENT
            # ------------------------------------------------

            st.session_state.document_text = text

            st.session_state.document_name = uploaded_file.name


            st.success(
                "PDF Loaded Successfully"
            )

            st.caption(
                uploaded_file.name
            )

            st.caption(
                f"{len(reader.pages)} page(s)"
            )


        except Exception as e:

            st.error(
                f"❌ Could not read PDF: {e}"
            )


    # --------------------------------------------------------
    # SUMMARY BUTTON
    # --------------------------------------------------------

    st.markdown("---")

    if st.button(
        "📋 Generate Summary",
        use_container_width=True
    ):

        if st.session_state.document_text:

            with st.spinner(
                "Analyzing document..."
            ):

                try:

                    summary_response = client.chat.completions.create(

                        model=MODEL_NAME,

                        messages=[
                            {
                                "role": "system",

                                "content": """
You are an expert document summarizer.

Summarize the provided PDF clearly and accurately.

Use:
- A short overview
- Important topics
- Key points
- Important conclusions

Do not invent information that is not present
in the document.
"""
                            },

                            {
                                "role": "user",

                                "content": (
                                    "Document:\n\n"
                                    + st.session_state.document_text
                                )
                            }
                        ],

                        temperature=0.3,

                        max_tokens=1500
                    )


                    summary = (
                        summary_response
                        .choices[0]
                        .message
                        .content
                    )


                    st.session_state.messages.append(
                        {
                            "role": "assistant",

                            "content":
                                "## 📋 Document Summary\n\n"
                                + summary
                        }
                    )


                    st.rerun()


                except Exception as e:

                    st.error(
                        f"❌ Groq API Error: {e}"
                    )

        else:

            st.warning(
                "Upload a PDF first."
            )


    # --------------------------------------------------------
    # NEW CHAT
    # --------------------------------------------------------

    if st.button(
        "➕ New Chat",
        use_container_width=True
    ):

        st.session_state.messages = []

        st.rerun()


    # ========================================================
    # DOWNLOADABLE RESOURCES
    # ========================================================

    st.markdown("---")

    st.markdown(
        "### 📚 Download Resources"
    )


    pdf_files = [

        (
            "AI PDF Assistant Overview",
            "assets/pdfs/AI_PDF_Assistant_Overview.pdf"
        ),

        (
            "Machine Learning Basics",
            "assets/pdfs/Machine_Learning_Basics.pdf"
        ),

        (
            "XGBoost Fraud Detection",
            "assets/pdfs/XGBoost_Fraud_Detection.pdf"
        ),

        (
            "NLP & LLM Applications",
            "assets/pdfs/NLP_and_LLM_Applications.pdf"
        ),

        (
            "Full-Stack AI Application Guide",
            "assets/pdfs/Full_Stack_AI_Application_Guide.pdf"
        )
    ]


    for name, path in pdf_files:

        if os.path.exists(path):

            with open(
                path,
                "rb"
            ) as pdf_file:

                st.download_button(

                    label=f"📄 {name}",

                    data=pdf_file,

                    file_name=os.path.basename(path),

                    mime="application/pdf",

                    use_container_width=True
                )

        else:

            st.caption(
                f"⚠️ {name} unavailable"
            )


    # ========================================================
    # GROQ INFORMATION
    # ========================================================

    st.markdown("---")

    st.caption(
        "Powered by Groq • GPT-OSS 120B"
    )


    # ========================================================
    # PROFILE CARD
    # ========================================================
    st.markdown(
    """
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
""",
    unsafe_allow_html=True
)
# ============================================================
# MAIN HEADER
# ============================================================

st.markdown(
    """
    <h1 style="text-align:center;">
        📄 AI PDF Assistant
    </h1>
    """,
    unsafe_allow_html=True
)

st.caption(
    "Upload a PDF and ask questions about it"
)


# ============================================================
# WELCOME SCREEN
# ============================================================

if (
    len(st.session_state.messages) == 0
    and st.session_state.document_text == ""
):

    st.info(
        "👈 Upload a PDF from the sidebar to begin."
    )

    col1, col2 = st.columns(2)


    with col1:

        st.markdown(
            """
            ### Examples

            - Summarize this document
            - Explain chapter 2
            - Extract key points
            """
        )


    with col2:

        st.markdown(
            """
            ### More Examples

            - Generate interview questions
            - Create quiz questions
            - Explain difficult concepts
            """
        )


# ============================================================
# DISPLAY CHAT HISTORY
# ============================================================

for message in st.session_state.messages:

    with st.chat_message(
        message["role"]
    ):

        st.markdown(
            message["content"]
        )


# ============================================================
# USER INPUT
# ============================================================

prompt = st.chat_input(
    "Ask questions about the uploaded PDF..."
)


# ============================================================
# CHAT
# ============================================================

if prompt:

    # --------------------------------------------------------
    # CHECK PDF
    # --------------------------------------------------------

    if not st.session_state.document_text:

        st.warning(
            "⚠️ Please upload a PDF first."
        )

        st.stop()


    # --------------------------------------------------------
    # SAVE USER MESSAGE
    # --------------------------------------------------------

    st.session_state.messages.append(
        {
            "role": "user",
            "content": prompt
        }
    )


    # --------------------------------------------------------
    # DISPLAY USER MESSAGE
    # --------------------------------------------------------

    with st.chat_message("user"):

        st.markdown(prompt)


    # --------------------------------------------------------
    # ASSISTANT
    # --------------------------------------------------------

    with st.chat_message("assistant"):

        with st.spinner(
            "Thinking..."
        ):

            try:

                # ============================================
                # SYSTEM PROMPT
                # ============================================

                messages = [

                    {
                        "role": "system",

                        "content": f"""
You are an AI PDF Assistant.

Your task is to answer questions using ONLY
the information contained in the uploaded document.

If the answer cannot be found in the document,
respond exactly:

"I could not find that information in the document."

Do not make up information.

Be clear, concise, and helpful.

Uploaded document:

{st.session_state.document_text}
"""
                    }
                ]


                # ============================================
                # CONVERSATION HISTORY
                # ============================================

                for msg in st.session_state.messages:

                    messages.append(
                        {
                            "role": msg["role"],

                            "content": msg["content"]
                        }
                    )


                # ============================================
                # GROQ REQUEST
                # ============================================

                response = client.chat.completions.create(

                    model=MODEL_NAME,

                    messages=messages,

                    temperature=0.5,

                    max_tokens=1024
                )


                # ============================================
                # GET ANSWER
                # ============================================

                answer = (
                    response
                    .choices[0]
                    .message
                    .content
                )


                # ============================================
                # DISPLAY ANSWER
                # ============================================

                st.markdown(answer)


                # ============================================
                # SAVE ANSWER
                # ============================================

                st.session_state.messages.append(
                    {
                        "role": "assistant",

                        "content": answer
                    }
                )


            except Exception as e:

                st.error(
                    f"❌ Error communicating with Groq:\n\n{e}"
                )


# ============================================================
# FOOTER
# ============================================================
st.markdown(
    """
<div class="footer">
    Made with ❤️ by <b>Raneesh</b>
</div>
""",
    unsafe_allow_html=True
)