import streamlit as st
import google.generativeai as genai
import pypdf
import requests
from bs4 import BeautifulSoup
import time
from google.api_core import exceptions
# --- CONFIGURATION ---

API_KEY = "AIzaSyDV1kwK0KcBOnInOpdOwutuSAuqMgLq82E"
genai.configure(api_key=API_KEY)
MODEL_NAME = 'gemini-2.5-flash-lite'

st.set_page_config(page_title="MaxFax RAG AI Assistant", layout="wide")

# --- HELPER FUNCTIONS ---
def get_url_content(url):
    """Visits a URL and returns the clean text (no HTML code)."""
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Remove javascript and css so the AI doesn't get confused
        for script in soup(["script", "style"]):
            script.extract()
            
        # Get text and clean up white space
        text = soup.get_text()
        # Compress multiple newlines into one
        lines = (line.strip() for line in text.splitlines())
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        clean_text = '\n'.join(chunk for chunk in chunks if chunk)
        
        return clean_text
    except Exception as e:
        st.error(f"Error reading URL: {e}")
        return ""

# --- SIDEBAR: KNOWLEDGE BASE ---
with st.sidebar:
    st.title("🧠 Knowledge Base")
    st.caption("Upload a PDF or paste a URL to teach your bot.")
    
    # Input 1: PDF
    uploaded_file = st.file_uploader("Upload PDF", type="pdf")
    
    # Input 2: URL
    url_input = st.text_input("Or paste a website URL:")
    
    # Load Button
    if st.button("Load Data"):
        combined_text = ""
        
        # Process PDF
        if uploaded_file:
            reader = pypdf.PdfReader(uploaded_file)
            for page in reader.pages:
                combined_text += page.extract_text() or ""
            st.success(f"loaded PDF ({len(reader.pages)} pages)")

        # Process URL
        if url_input:
            url_text = get_url_content(url_input)
            if url_text:
                combined_text += f"\n\n--- CONTENT FROM URL: {url_input} ---\n{url_text}"
                st.success(f"Loaded Website ({len(url_text)} characters)")

        # Save to memory
        if combined_text:
            st.session_state['context_text'] = combined_text
            st.success("Brain Updated! Ready to chat.")
        else:
            st.warning("No text found in your inputs.")

    st.divider()
    
    # Input 3: Strict Mode Toggle
    strict_mode = st.checkbox("Strict Mode", value=True, 
                             help="If checked, AI will ONLY answer using your documents. If unchecked, it uses general knowledge too.")

# --- MAIN CHAT INTERFACE ---
st.title("Universal AI Assistant by Max (RAG) 🤖")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- CHAT LOGIC ---
if prompt := st.chat_input("Ask me anything..."):
    # 1. Display user message
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    # 2. Build the "System Instruction" (The Rules)
    # This determines if the bot is "Strict" or "Helpful"
    if strict_mode:
        base_instruction = (
            "You are a strict assistant. Answer ONLY using the provided context. "
            "If the answer is not in the context, say 'I cannot find that information in the documents.' "
            "Do not use outside knowledge."
        )
    else:
        base_instruction = (
            "You are a helpful assistant. Use the provided context to answer if possible, "
            "but you may use your general knowledge if the context is missing info."
        )

    # Attach the data (if any)
    if st.session_state.get('context_text'):
        system_instruction = f"{base_instruction}\n\nCONTEXT:\n{st.session_state['context_text']}"
    else:
        system_instruction = "You are a helpful assistant." if not strict_mode else "You are in strict mode but no documents are loaded. Refuse to answer factual questions."

    # 3. Create the Model
    model = genai.GenerativeModel(MODEL_NAME, system_instruction=system_instruction)

 # 4. Generate Response
    with st.chat_message("assistant"):
        try:
            # Wrap the call in a try block
            response_stream = model.generate_content(prompt, stream=True)
            
            # --- JSON FIXER HELPER ---
            def stream_parser(stream):
                for chunk in stream:
                    try:
                        text_content = chunk.text
                        if text_content:
                            yield text_content
                    except ValueError:
                        pass
            
            full_response = st.write_stream(stream_parser(response_stream))
            
            # Save response to history only if successful
            st.session_state.messages.append({"role": "assistant", "content": full_response})

        except exceptions.ResourceExhausted:
            st.error("⚠️ Rate limit reached! The free tier allows 15 requests per minute. Please wait about 15 seconds and try again.")
            time.sleep(15) # Pause execution to prevent the user from spamming
        except Exception as e:
            st.error(f"An unexpected error occurred: {e}")