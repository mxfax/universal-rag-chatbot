# Universal Intelligence Studio

A sleek, Apple-inspired **Retrieval-Augmented Generation (RAG)** assistant built with Python and Streamlit. Ground frontier and open-source models with your custom documents and live web URLs under strict context-verification guardrails.

**Designed & Developed by Max**

---

## ✨ Features

- **Multi-Engine Routing:** Switch seamlessly between top commercial and open-source providers:
  - **Free-Tier Models:** Groq Cloud (Llama 3.3 70B, DeepSeek R1 Distill, Qwen 2.5), OpenRouter (Free models), Cerebras, and Mistral AI (Experimentation).
  - **Commercial Flagships:** Google Gemini (2.5 Flash, 2.5 Pro), OpenAI (GPT-4o, o3-mini), Anthropic Claude (3.7 Sonnet, 3.5 Sonnet, 3.5 Haiku).
- **Multi-Source Ingestion:** Ingest context from **PDF documents** or **live website URLs** (with HTML/script cleaning).
- **Strict Context Guardrail:** Hard-enforced toggle ensuring models answer strictly using provided documents without hallucinations.
- **Zero-Retention Privacy:** Bring-Your-Own-Key (BYOK) architecture. Keys and documents are kept exclusively in temporary session memory and never stored or logged.
- **Apple-Inspired Dark UI:** Native typography, frosted glassmorphic sidebars, interactive status indicators, and responsive mobile layout.
- **Research Utilities:** Instant chat export (`.md`), quick conversation wiping, and context starter prompts (*Summarize*, *Key Takeaways*, *Gaps*).

---

## 🛠️ Quick Start

### 1. Clone the Repository
```bash
git clone [https://github.com/mxfax/universal-rag-chatbot.git](https://github.com/mxfax/universal-rag-chatbot.git)
cd universal-rag-chatbot
