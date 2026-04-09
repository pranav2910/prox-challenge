# 🤖 Vulcan OmniPro 220
### Multimodal AI Agent — MVP

> Ingest complex documents, build a local knowledge graph, and chat with your data through a clean web interface.

---

## ✨ Features

- 📄 **Document Ingestion** — Parse and process PDFs and other source files into a structured knowledge base
- 🧠 **Local Knowledge Graph** — Stores extracted knowledge in a lightweight `knowledge.json` store
- 💬 **Interactive Chat Interface** — Streamlit-powered frontend for conversing with your AI agent
- ⚡ **Multimodal Support** — Handles text, documents, and extracted visual assets
- 🔐 **Secure by Default** — API keys and sensitive files are kept out of version control

---

## 📂 Project Structure

```text
prox-challenge/
├── __pycache__/            # Compiled Python bytecode
├── extracted_assets/       # Assets extracted during document ingestion
├── files/                  # Source documents for the agent to process
├── .env                    # Environment variables (git-ignored)
├── .env.example            # Template for required environment variables
├── .gitignore              # Git ignore rules
├── agent.py                # Core LLM and AI agent logic
├── app.py                  # Streamlit web frontend
├── ingest.py               # Data parsing and knowledge base population script
├── knowledge.json          # Local knowledge store
├── product.webp            # UI branding asset
├── product-inside.webp     # UI branding asset
├── README.md               # Project documentation
└── requirements.txt        # Python dependencies
```

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Frontend | Streamlit |
| Backend | Python 3.12 |
| Document Processing | PyMuPDF, PyArrow |
| AI / LLM | Custom Agent (`agent.py`) |
| Config Management | python-dotenv |

---

## ⚙️ Installation & Setup

### 1. Clone the Repository

```bash
git clone https://github.com/pranav2910/prox-challenge.git
cd prox-challenge
```

### 2. Create a Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate      # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

```bash
cp .env.example .env
```

Open `.env` and fill in your credentials (e.g. your OpenAI API key). This file is git-ignored and will never be committed.

---

## 🚀 Usage

### Step 1 — Ingest Your Documents (skip this step if you are testing this prtotype for Vulcan OmniPro 220 (because both extracted files and json are already included) )

Place your source files inside the `files/` directory, then run:

```bash
python ingest.py
```

This will:
- Parse and process all documents in `files/`
- Extract assets into `extracted_assets/`
- Populate `knowledge.json` with structured knowledge

### Step 2 — Launch the App

```bash
streamlit run app.py
```

The app will open automatically in your browser at **`http://localhost:8501`**.

---

## 🔒 Security

- **Never** commit your `.env` file or hardcode API keys in source code
- The `venv/`, `extracted_assets/`, and `files/` directories are git-ignored to keep the repo lightweight and secure
- Rotate any keys that are accidentally exposed immediately

---

