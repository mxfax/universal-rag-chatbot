import streamlit as st
import pypdf
import requests
from bs4 import BeautifulSoup
import time

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="Intelligence Studio",
    page_icon="",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- RESPONSIVE DARK MODE & MOBILE OVERRIDES ---
DARK_CSS = """
<style>
/* 1. Universal Layout & Typography Reset */
html, body, [data-testid="stAppViewContainer"], [data-testid="stHeader"] {
    background-color: #0c0c0e !important;
    color: #f5f5f7 !important;
    font-family: -apple-system, BlinkMacSystemFont, "SF Pro Text", "SF Pro Display", "Inter", sans-serif !important;
}

/* 2. Sidebar Glassmorphic Dark Frame */
section[data-testid="stSidebar"] {
    background-color: #141416 !important;
    border-right: 1px solid #242426 !important;
}

section[data-testid="stSidebar"] * {
    color: #f5f5f7 !important;
}

section[data-testid="stSidebar"] .stCaption,
section[data-testid="stSidebar"] small {
    color: #a1a1a6 !important;
}

/* 3. Inputs & Select Boxes */
div[data-baseweb="input"] > div,
div[data-baseweb="select"] > div {
    background-color: #1f1f23 !important;
    border: 1px solid #323236 !important;
    border-radius: 10px !important;
    color: #ffffff !important;
}

div[data-baseweb="input"] input {
    background-color: transparent !important;
    color: #ffffff !important;
    -webkit-text-fill-color: #ffffff !important;
}

div[data-baseweb="select"] * {
    color: #ffffff !important;
    -webkit-text-fill-color: #ffffff !important;
}

div[data-baseweb="select"] svg {
    fill: #ffffff !important;
}

/* 4. Dropdown Menus & Popover Lists */
ul[data-baseweb="menu"],
div[data-baseweb="popover"],
div[data-baseweb="popover"] > div {
    background-color: #1f1f23 !important;
    border: 1px solid #323236 !important;
    border-radius: 10px !important;
}

li[data-baseweb="menu-item"],
li[role="option"] {
    background-color: #1f1f23 !important;
    color: #f5f5f7 !important;
}

li[data-baseweb="menu-item"] * {
    color: #f5f5f7 !important;
    -webkit-text-fill-color: #f5f5f7 !important;
}

li[data-baseweb="menu-item"]:hover,
li[role="option"][aria-selected="true"],
li[role="option"]:hover {
    background-color: #2c2c30 !important;
}

/* 5. Expander & Tabs */
div[data-testid="stExpander"] {
    background-color: #1a1a1d !important;
    border: 1px solid #2c2c2e !important;
    border-radius: 12px !important;
    overflow: hidden;
}

div[data-testid="stExpander"] summary {
    background-color: #1a1a1d !important;
}

div[data-testid="stExpander"] summary p,
div[data-testid="stExpander"] summary span {
    color: #f5f5f7 !important;
    font-weight: 500 !important;
}

div[data-testid="stExpander"] summary svg {
    fill: #f5f5f7 !important;
    color: #f5f5f7 !important;
}

div[data-testid="stExpander"] div[data-testid="stExpanderDetails"] * {
    color: #f5f5f7 !important;
}

/* Segmented Tabs Styling */
div[data-baseweb="tab-list"] {
    background-color: #1a1a1d !important;
    padding: 3px !important;
    border-radius: 10px !important;
    gap: 4px !important;
    border: 1px solid #2c2c2e !important;
}

div[data-baseweb="tab"] {
    border-radius: 8px !important;
    background-color: transparent !important;
    border: none !important;
    color: #a1a1a6 !important;
    padding: 0.35rem 0.8rem !important;
    font-size: 0.82rem !important;
}

div[aria-selected="true"][data-baseweb="tab"] {
    background-color: #2c2c30 !important;
    color: #ffffff !important;
    font-weight: 600 !important;
}

/* 6. File Uploader */
div[data-testid="stFileUploader"] {
    background-color: transparent !important;
}

div[data-testid="stFileUploaderDropzone"] {
    background-color: #161619 !important;
    border: 1.5px dashed #323236 !important;
    border-radius: 12px !important;
}

div[data-testid="stFileUploaderDropzone"] * {
    color: #f5f5f7 !important;
}

div[data-testid="stFileUploaderDropzone"] svg {
    fill: #a1a1a6 !important;
    stroke: #a1a1a6 !important;
}

div[data-testid="stFileUploaderDropzone"] button {
    background-color: #26262a !important;
    border: 1px solid #3a3a3c !important;
    border-radius: 8px !important;
    box-shadow: none !important;
}

div[data-testid="stFileUploaderDropzone"] button * {
    color: #ffffff !important;
    font-weight: 500 !important;
}

/* 7. Strict Mode Toggle & Tooltip Icon */
div[data-testid="stToggle"] label p {
    color: #f5f5f7 !important;
    font-weight: 500 !important;
}

div[data-testid="stTooltipIcon"] svg {
    fill: #a1a1a6 !important;
    color: #a1a1a6 !important;
    opacity: 1 !important;
}

/* 8. Action Buttons */
div.stButton > button, div[data-testid="stDownloadButton"] > button {
    background-color: #0a84ff !important;
    border: none !important;
    border-radius: 980px !important;
    font-size: 0.85rem !important;
    font-weight: 500 !important;
    padding: 0.5rem 1.1rem !important;
    letter-spacing: -0.01em !important;
    transition: all 0.2s cubic-bezier(0.16, 1, 0.3, 1) !important;
    min-height: 42px !important; /* Mobile touch-target optimization */
}

div.stButton > button *, div[data-testid="stDownloadButton"] > button * {
    color: #ffffff !important;
}

div.stButton > button:hover, div[data-testid="stDownloadButton"] > button:hover {
    background-color: #0071e3 !important;
    transform: scale(1.01);
}

/* 9. Chat Workspace */
[data-testid="stChatMessage"] {
    background-color: #161619 !important;
    border-radius: 16px !important;
    border: 1px solid #26262a !important;
    box-shadow: 0 4px 14px rgba(0,0,0,0.5) !important;
    padding: 1rem 1.2rem !important;
    margin-bottom: 0.8rem !important;
}

[data-testid="stChatMessage"] * {
    color: #f5f5f7 !important;
}

div[data-testid="stChatInput"] {
    background-color: #161619 !important;
    border-radius: 980px !important;
    border: 1px solid #323236 !important;
    box-shadow: 0 4px 20px rgba(0,0,0,0.6) !important;
}

div[data-testid="stChatInput"] textarea {
    color: #ffffff !important;
}

/* 10. Hero Banner & Cards */
.hero-banner-container {
    position: relative;
    width: 100%;
    min-height: 190px;
    border-radius: 20px;
    background: 
        linear-gradient(135deg, rgba(12, 12, 14, 0.92) 0%, rgba(12, 12, 14, 0.5) 60%, rgba(10, 132, 255, 0.15) 100%),
        url('https://images.unsplash.com/photo-1618005182384-a83a8bd57fbe?auto=format&fit=crop&w=1600&q=80') center/cover no-repeat;
    border: 1px solid rgba(255, 255, 255, 0.08);
    box-shadow: 0 12px 36px rgba(0, 0, 0, 0.6);
    display: flex;
    flex-direction: column;
    justify-content: flex-end;
    padding: 1.6rem 1.8rem;
    margin-bottom: 1.2rem;
    overflow: hidden;
}

.hero-banner-container::after {
    content: '';
    position: absolute;
    inset: 0;
    backdrop-filter: blur(1.5px);
    z-index: 1;
}

.hero-content {
    position: relative;
    z-index: 2;
}

.hero-title {
    font-size: 2rem;
    font-weight: 700;
    letter-spacing: -0.04em;
    color: #ffffff;
    margin: 0;
    text-shadow: 0 2px 10px rgba(0,0,0,0.7);
}

.hero-subtitle {
    font-size: 0.92rem;
    font-weight: 400;
    color: #a1a1a6;
    margin-top: 0.35rem;
    letter-spacing: -0.01em;
}

.developer-badge {
    display: inline-block;
    padding: 0.25rem 0.8rem;
    background: rgba(10, 132, 255, 0.2);
    border: 1px solid rgba(100, 210, 255, 0.3);
    color: #64d2ff;
    font-size: 0.76rem;
    font-weight: 600;
    border-radius: 980px;
    letter-spacing: -0.01em;
    margin-top: 0.8rem;
    backdrop-filter: blur(12px);
}

.sidebar-heading {
    font-size: 0.72rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    color: #a1a1a6 !important;
    margin-top: 1.1rem;
    margin-bottom: 0.45rem;
}

hr {
    border-color: #242426 !important;
    margin: 1.1rem 0 !important;
}

/* ==========================================================================
   MOBILE RESPONSIVENESS OVERRIDES (< 768px)
   ========================================================================== */
@media (max-width: 768px) {
    /* 1. Force sidebar to stay open / slide out on mobile */
    section[data-testid="stSidebar"] {
        transform: translateX(0) !important;
        width: 86vw !important;
        max-width: 340px !important;
        z-index: 999999 !important;
    }
    
    /* 2. Compact Hero Banner */
    .hero-banner-container {
        padding: 1.2rem 1.2rem !important;
        min-height: 160px !important;
        border-radius: 16px !important;
    }

    .hero-title {
        font-size: 1.5rem !important;
    }

    .hero-subtitle {
        font-size: 0.85rem !important;
    }

    /* 3. Wrap metadata pill tags smoothly */
    .hero-content > div {
        display: flex !important;
        flex-wrap: wrap !important;
        gap: 0.4rem !important;
    }

    /* 4. Chat controls and columns full width */
    div[data-testid="column"] {
        width: 100% !important;
        flex: 1 1 100% !important;
        margin-bottom: 0.4rem !important;
    }

    /* 5. Chat message spacing */
    [data-testid="stChatMessage"] {
        padding: 0.85rem 1rem !important;
        border-radius: 14px !important;
    }
}
</style>
"""
st.markdown(DARK_CSS, unsafe_allow_html=True)

# --- MULTI-PROVIDER CONFIGURATION ---
PROVIDER_CONFIG = {
    "Groq Cloud (Free Tier)": {
        "base_url": "https://api.groq.com/openai/v1",
        "type": "openai_compatible",
        "models": {
            "llama-3.3-70b-versatile": "Fast 70B reasoning model (~300+ tokens/sec).",
            "llama-3.1-8b-instant": "Ultra-low latency lightweight workhorse.",
            "qwen/qwen-2.5-32b": "High-precision multilingual reasoning model.",
            "deepseek-r1-distill-llama-70b": "Deep reasoning model for math, code, and logic."
        },
        "key_guide": """
        **How to get a Free Groq API Key:**
        1. Open [Groq Console](https://console.groq.com/).
        2. Sign up or log in (Google or GitHub).
        3. Navigate to **API Keys** on the left menu.
        4. Click **Create API Key**, copy the token (starts with `gsk_`), and paste below.
        *(No credit card required. Free tier includes up to 14,400 daily requests).*
        """
    },
    "OpenRouter (Free Models)": {
        "base_url": "https://openrouter.ai/api/v1",
        "type": "openai_compatible",
        "models": {
            "meta-llama/llama-3.3-70b-instruct:free": "Top-tier open-source 70B model with 128k context.",
            "deepseek/deepseek-r1:free": "Frontier reasoning model with step-by-step thinking.",
            "google/gemma-3-12b-it:free": "Google's balanced open model with high factual accuracy.",
            "qwen/qwen-2.5-7b-instruct:free": "Efficient multilingual conversational assistant."
        },
        "key_guide": """
        **How to get a Free OpenRouter API Key:**
        1. Visit [OpenRouter.ai](https://openrouter.ai/).
        2. Sign in with Google or GitHub.
        3. Go to **Keys** in the top navigation or settings.
        4. Click **Create Key**, give it a name, and copy the string (starts with `sk-or-`).
        *(Allows permanent access to all models ending with `:free` with zero balance needed).*
        """
    },
    "Cerebras (Free Tier)": {
        "base_url": "https://api.cerebras.ai/v1",
        "type": "openai_compatible",
        "models": {
            "llama3.3-70b": "High-speed inference on Wafer-Scale engine (~2,000 tokens/sec).",
            "llama3.1-8b": "Instant low-latency model for quick contextual extractions."
        },
        "key_guide": """
        **How to get a Free Cerebras API Key:**
        1. Navigate to [Cerebras Cloud](https://cloud.cerebras.ai/).
        2. Sign up with your developer account.
        3. Go to **API Keys** and select **Generate API Key**.
        4. Copy and paste your key below.
        """
    },
    "Mistral AI (Free Experimentation)": {
        "base_url": "https://api.mistral.ai/v1",
        "type": "openai_compatible",
        "models": {
            "mistral-small-latest": "Cost-effective, highly accurate model for RAG & summarization.",
            "codestral-latest": "Specialized coding and structured data reasoning model.",
            "mistral-large-latest": "Flagship model with strong multilingual reasoning."
        },
        "key_guide": """
        **How to get a Free Mistral API Key:**
        1. Go to [Mistral AI Console](https://console.mistral.ai/).
        2. Sign in and open **API Keys**.
        3. Create a free **Experimentation Tier** key and copy the token.
        """
    },
    "Google Gemini": {
        "type": "gemini",
        "models": {
            "gemini-2.5-flash": "Fast, high-tier multimodal performance.",
            "gemini-2.5-pro": "Advanced analytical reasoning for documents & code.",
            "gemini-2.5-flash-lite": "Ultra-low latency inference for quick tasks.",
            "gemini-2.0-flash": "Responsive multi-task foundation model."
        },
        "key_guide": """
        **How to get a Google Gemini API Key:**
        1. Open [Google AI Studio](https://aistudio.google.com/).
        2. Click **Get API Key** in the sidebar.
        3. Click **Create API Key** and paste below.
        """
    },
    "OpenAI": {
        "base_url": "https://api.openai.com/v1",
        "type": "openai_compatible",
        "models": {
            "gpt-4o": "Multimodal flagship model for complex document context.",
            "gpt-4o-mini": "Fast, lightweight model for high-speed indexing.",
            "o3-mini": "Advanced reasoning engine for math, logic, and coding."
        },
        "key_guide": """
        **How to get an OpenAI API Key:**
        1. Open the [OpenAI Platform](https://platform.openai.com/).
        2. Go to **Dashboard → API Keys**.
        3. Click **Create new secret key** *(requires billing setup)*.
        """
    },
    "Anthropic Claude": {
        "type": "anthropic",
        "models": {
            "claude-3-7-sonnet-20250219": "State-of-the-art hybrid reasoning model.",
            "claude-3-5-sonnet-20241022": "High intelligence with nuanced comprehension.",
            "claude-3-5-haiku-20241022": "Low latency with high factual accuracy."
        },
        "key_guide": """
        **How to get an Anthropic API Key:**
        1. Open the [Anthropic Console](https://console.anthropic.com/).
        2. Navigate to **API Keys** and generate a key *(requires prepaid credits)*.
        """
    }
}

# --- KEY VERIFICATION LOGIC ---
def verify_api_key(provider, api_key, model_name=None):
    try:
        p_data = PROVIDER_CONFIG[provider]
        p_type = p_data.get("type")

        if p_type == "gemini":
            import google.generativeai as genai
            genai.configure(api_key=api_key)
            next(iter(genai.list_models()), None)
            return True, "API Key authenticated."

        elif p_type == "anthropic":
            import anthropic
            client = anthropic.Anthropic(api_key=api_key)
            client.messages.create(
                model=model_name or "claude-3-5-haiku-20241022",
                max_tokens=1,
                messages=[{"role": "user", "content": "ping"}]
            )
            return True, "API Key authenticated."

        elif p_type == "openai_compatible":
            from openai import OpenAI
            client = OpenAI(api_key=api_key, base_url=p_data.get("base_url"))
            client.models.list()
            return True, "API Key authenticated."

    except Exception:
        return False, "The API key is invalid."

# --- HELPER: WEB SCRAPING ---
def get_url_content(url):
    try:
        response = requests.get(url, timeout=10)
        soup = BeautifulSoup(response.content, 'html.parser')
        for script in soup(["script", "style"]):
            script.extract()
        text = soup.get_text()
        lines = (line.strip() for line in text.splitlines())
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        return '\n'.join(chunk for chunk in chunks if chunk)
    except Exception as e:
        st.error(f"Error loading URL: {e}")
        return ""

# Initialize session states
if "auth_status" not in st.session_state:
    st.session_state.auth_status = None
if "auth_message" not in st.session_state:
    st.session_state.auth_message = ""
if "messages" not in st.session_state:
    st.session_state.messages = []
if "context_sources" not in st.session_state:
    st.session_state.context_sources = []

# --- SIDEBAR: SYSTEM CONTROLS ---
with st.sidebar:
    st.markdown('<div class="sidebar-heading">Model Engine</div>', unsafe_allow_html=True)
    
    selected_provider = st.selectbox(
        "Provider",
        options=list(PROVIDER_CONFIG.keys()),
        label_visibility="collapsed"
    )
    provider_info = PROVIDER_CONFIG[selected_provider]

    selected_model = st.selectbox(
        "Model",
        options=list(provider_info["models"].keys()),
        label_visibility="collapsed"
    )
    st.caption(provider_info["models"][selected_model])

    with st.expander("🔑 How to obtain API Key"):
        st.markdown(provider_info["key_guide"])

    user_api_key = st.text_input(
        f"{selected_provider} Key",
        type="password",
        placeholder="Enter API Key…",
        help="🔒 In-memory only · Never stored or logged"
    )

    # Verification LED Button
    if st.session_state.auth_status == "valid":
        btn_indicator = "🟢 Verify Key"
    elif st.session_state.auth_status == "invalid":
        btn_indicator = "🔴 Verify Key"
    else:
        btn_indicator = "⚪ Verify Key"

    if st.button(btn_indicator, use_container_width=True):
        if not user_api_key.strip():
            st.session_state.auth_status = "invalid"
            st.session_state.auth_message = "The API key is invalid."
        else:
            with st.spinner("Authenticating…"):
                is_valid, msg = verify_api_key(selected_provider, user_api_key.strip(), selected_model)
                if is_valid:
                    st.session_state.auth_status = "valid"
                    st.session_state.auth_message = msg
                else:
                    st.session_state.auth_status = "invalid"
                    st.session_state.auth_message = "The API key is invalid."
        st.rerun()

    if st.session_state.auth_status == "valid":
        st.success(st.session_state.auth_message)
    elif st.session_state.auth_status == "invalid":
        st.error(st.session_state.auth_message)

    st.markdown("---")

    # Knowledge Base Segmented Ingestion
    st.markdown('<div class="sidebar-heading">Knowledge Grounding</div>', unsafe_allow_html=True)
    
    # Active Context Status Card
    if st.session_state.get('context_text'):
        st.markdown(
            f"""
            <div style="background: rgba(48, 209, 88, 0.08); border: 1px solid rgba(48, 209, 88, 0.2); border-radius: 12px; padding: 0.75rem 0.9rem; margin-bottom: 0.8rem;">
                <div style="color: #30d158; font-size: 0.78rem; font-weight: 600;">● Active Knowledge Grounding</div>
                <div style="color: #a1a1a6; font-size: 0.72rem; margin-top: 3px;">{len(st.session_state['context_text']):,} characters loaded ({len(st.session_state.context_sources)} sources)</div>
            </div>
            """,
            unsafe_allow_html=True
        )
        if st.button("✕ Detach Context", use_container_width=True):
            st.session_state.pop('context_text', None)
            st.session_state.context_sources = []
            st.rerun()
    
    tab_doc, tab_web = st.tabs(["📄 Document", "🌐 URL"])
    
    with tab_doc:
        uploaded_file = st.file_uploader("Upload PDF Document", type="pdf", label_visibility="collapsed")
    with tab_web:
        url_input = st.text_input("Source URL", placeholder="https://example.com/docs", label_visibility="collapsed")

    if st.button("Index Source", use_container_width=True):
        combined_text = st.session_state.get('context_text', "")
        new_sources = list(st.session_state.context_sources)
        
        if uploaded_file:
            reader = pypdf.PdfReader(uploaded_file)
            pdf_text = "".join([page.extract_text() or "" for page in reader.pages])
            if pdf_text:
                combined_text += f"\n\n--- PDF SOURCE: {uploaded_file.name} ---\n{pdf_text}"
                new_sources.append(f"📄 {uploaded_file.name} ({len(reader.pages)}p)")
                st.success(f"Indexed {len(reader.pages)} pages.")

        if url_input:
            url_text = get_url_content(url_input)
            if url_text:
                combined_text += f"\n\n--- WEB SOURCE: {url_input} ---\n{url_text}"
                new_sources.append(f"🌐 {url_input}")
                st.success("Indexed URL.")

        if combined_text:
            st.session_state['context_text'] = combined_text
            st.session_state.context_sources = new_sources
            st.rerun()
        else:
            st.warning("No text extracted from provided inputs.")

    st.markdown("---")
    strict_mode = st.toggle("Strict Context Only", value=True, help="Limit model outputs strictly to your ingested documents/URLs.")

# --- MAIN WORKSPACE HERO BANNER ---
st.markdown(
    """
    <div class="hero-banner-container">
        <div class="hero-content">
            <div class="hero-title">Universal Intelligence</div>
            <div class="hero-subtitle">High-Precision Retrieval-Augmented Generation & Multi-Model Engine</div>
            <p style="color: #d1d1d6; font-size: 0.95rem; margin-top: 0.8rem; max-width: 850px; line-height: 1.55;">
                Ingest custom PDFs or live website URLs into temporary session memory, then query them with strict fact-checking enabled across leading frontier and open-source models.
            </p>
            <div style="display: flex; gap: 0.5rem; flex-wrap: wrap; margin-top: 0.85rem; align-items: center;">
                <span style="background: rgba(48, 209, 88, 0.12); color: #30d158; border: 1px solid rgba(48, 209, 88, 0.28); padding: 0.28rem 0.75rem; border-radius: 980px; font-size: 0.76rem; font-weight: 500;">
                    🛡️ In-Memory Only · Zero Retention
                </span>
                <span style="background: rgba(255, 255, 255, 0.08); padding: 0.28rem 0.75rem; border-radius: 980px; font-size: 0.76rem; border: 1px solid rgba(255, 255, 255, 0.12); color: #f5f5f7;">
                    ⚡ Multi-Provider Routing
                </span>
                <span style="background: rgba(255, 255, 255, 0.08); padding: 0.28rem 0.75rem; border-radius: 980px; font-size: 0.76rem; border: 1px solid rgba(255, 255, 255, 0.12); color: #f5f5f7;">
                    📄 PDF & Web Ingestion
                </span>
            </div>
            <div><span class="developer-badge">Designed & Developed by Max</span></div>
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

if not user_api_key:
    st.info(f"👈 Please authenticate your {selected_provider} API key in the sidebar to begin.")
    st.stop()

# --- CHAT UTILITIES BAR ---
col_ctrl1, col_ctrl2 = st.columns([6, 2])
with col_ctrl2:
    btn_col1, btn_col2 = st.columns(2)
    with btn_col1:
        if st.session_state.messages:
            if st.button("🗑️ Clear", help="Wipe chat history", use_container_width=True):
                st.session_state.messages = []
                st.rerun()
    with btn_col2:
        if st.session_state.messages:
            chat_export = "\n\n".join([f"### {m['role'].capitalize()}\n{m['content']}" for m in st.session_state.messages])
            st.download_button("💾 Export", data=chat_export, file_name="research-notes.md", mime="text/markdown", use_container_width=True)

# Render Chat History
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- QUICK PROMPT STARTER CHIPS ---
active_prompt = None
if not st.session_state.messages and st.session_state.get('context_text'):
    st.markdown("<div style='font-size: 0.8rem; color: #a1a1a6; margin-top: 1rem; margin-bottom: 0.4rem;'>Suggested Starters</div>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    if c1.button("📋 Summarize Document", use_container_width=True):
        active_prompt = "Provide a structured executive summary of the loaded context."
    if c2.button("🔑 Key Takeaways", use_container_width=True):
        active_prompt = "Extract the top 5 key takeaways and critical data points from the context."
    if c3.button("❓ Action Items & Gaps", use_container_width=True):
        active_prompt = "Analyze the provided text and identify action items or critical knowledge gaps."

# Check for regular chat input or starter chip trigger
if prompt_input := st.chat_input("Ask anything about your context or general knowledge..."):
    active_prompt = prompt_input

# --- STREAMING GENERATION HANDLERS ---
def stream_gemini(model_name, api_key, system_prompt, user_prompt):
    import google.generativeai as genai
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel(model_name, system_instruction=system_prompt)
    response = model.generate_content(user_prompt, stream=True)
    for chunk in response:
        if chunk.text:
            yield chunk.text

def stream_openai_compatible(model_name, api_key, base_url, system_prompt, user_prompt):
    from openai import OpenAI
    client = OpenAI(api_key=api_key, base_url=base_url)
    formatted_messages = [{"role": "system", "content": system_prompt}]
    for msg in st.session_state.messages[:-1]:
        formatted_messages.append({"role": msg["role"], "content": msg["content"]})
    formatted_messages.append({"role": "user", "content": user_prompt})

    stream = client.chat.completions.create(
        model=model_name,
        messages=formatted_messages,
        stream=True
    )
    for chunk in stream:
        if chunk.choices and chunk.choices[0].delta.content:
            yield chunk.choices[0].delta.content

def stream_claude(model_name, api_key, system_prompt, user_prompt):
    import anthropic
    client = anthropic.Anthropic(api_key=api_key)
    formatted_messages = []
    for msg in st.session_state.messages[:-1]:
        formatted_messages.append({"role": msg["role"], "content": msg["content"]})
    formatted_messages.append({"role": "user", "content": user_prompt})

    with client.messages.stream(
        model=model_name,
        system=system_prompt,
        messages=formatted_messages,
        max_tokens=4096
    ) as stream:
        for text in stream.text_stream:
            yield text

# --- CONVERSATION PIPELINE ---
if active_prompt:
    with st.chat_message("user"):
        st.markdown(active_prompt)
    st.session_state.messages.append({"role": "user", "content": active_prompt})

    # Hard guard: Stop immediately if strict mode is active with no context loaded
    if strict_mode and not st.session_state.get('context_text'):
        refusal_msg = "⚠️ **Strict Mode Active**: No documents or URLs have been indexed. Please upload a PDF or index a website source in the sidebar before asking questions."
        with st.chat_message("assistant"):
            st.markdown(refusal_msg)
        st.session_state.messages.append({"role": "assistant", "content": refusal_msg})
        st.stop()

    # System instruction formatting
    if strict_mode:
        base_instruction = (
            "You are a strict, factual assistant. Answer ONLY using the facts directly stated in the provided context below. "
            "If the answer cannot be found in the context, respond strictly with: 'I cannot find that information in the provided documents.' "
            "Do NOT use pre-trained knowledge, assumptions, or external information under any circumstance."
        )
    else:
        base_instruction = (
            "You are a helpful assistant. Prioritize the provided context, "
            "but leverage general knowledge where supplementary explanation helps."
        )

    system_instruction = f"{base_instruction}\n\nCONTEXT:\n{st.session_state['context_text']}" if st.session_state.get('context_text') else base_instruction

    with st.chat_message("assistant"):
        try:
            p_data = PROVIDER_CONFIG[selected_provider]
            p_type = p_data.get("type")

            if p_type == "gemini":
                generator = stream_gemini(selected_model, user_api_key, system_instruction, active_prompt)
            elif p_type == "anthropic":
                generator = stream_claude(selected_model, user_api_key, system_instruction, active_prompt)
            elif p_type == "openai_compatible":
                generator = stream_openai_compatible(selected_model, user_api_key, p_data.get("base_url"), system_instruction, active_prompt)

            full_response = st.write_stream(generator)
            st.session_state.messages.append({"role": "assistant", "content": full_response})

        except Exception as e:
            st.error(f"Execution Error: {e}")