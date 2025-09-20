
# CURA – AI Medical Chatbot 🩺🤖

CURA is an **AI-powered medical chatbot** that uses **Retrieval-Augmented Generation (RAG)** to deliver accurate, context-aware healthcare Q&A.  
It integrates **Flask**, **LangChain**, **HuggingFace embeddings**, **Pinecone** (vector search), and **Google Gemini** as the LLM.

> ⚠️ **Disclaimer:** This project is for research/education. It **does not** provide medical advice.

---

## ✨ Features
- **RAG pipeline:** retrieves relevant chunks from your medical PDFs, then generates an answer with the LLM.
- **Semantic search:** Pinecone vector index over your documents for fast similarity lookup.
- **Clean API + Web UI:** Flask routes with a simple HTML/CSS front end.
- **Modular design:** prompt templates and retriever/LLM chains for easy extension.

---

## 🗂️ Project Structure
```

DATA/                      # Knowledge base + cached artifacts (embeddings, chunks, etc.)
research/
└── trials.ipynb         # Experiments / notes
src/
├── **init**.py
├── helper.py            # PDF loading, splitting, embeddings utils
└── prompt.py            # System prompt + template(s)
static/
└── style.css
templates/
└── index.html           # Simple UI
app.py                     # Flask app wiring RAG: retriever + LLM
store\_index.py             # Ingest PDFs -> embeddings -> Pinecone index
requirements.txt           # Python deps
dockerfile                 # Container build
app.yaml                   # (Optional) App Engine config
setup.py                   # Package metadata
template.sh                # Helper script(s)
.gcloudignore / .gitignore
README.md

````

---

## 🧰 Tech Stack
- **Backend:** Flask, Gunicorn  
- **LLM & Orchestration:** Google Gemini (via `langchain-google-genai`), LangChain  
- **Vector DB:** Pinecone (serverless)  
- **Embeddings:** HuggingFace (384-dim sentence embeddings)  
- **Frontend:** HTML + CSS (Jinja templates)  
- **Ops:** Docker, (optionally) Google Cloud Run / App Engine

---

## ⚙️ Prerequisites
- Python 3.10+ (3.11 recommended)  
- Pinecone account & API key  
- Google Generative AI API key (Gemini)

---

## 🔐 Environment Variables
Create a `.env` file in the project root:
```bash
PINECONE_API_KEY=your_pinecone_api_key
GOOGLE_API_KEY=your_google_api_key
````

---

## 🚀 Quickstart (Local)

1. **Create & activate venv**

```bash
python -m venv venv
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate
```

2. **Install dependencies**

```bash
pip install -r requirements.txt
```

3. **Add your PDFs**

* Drop your medical PDFs into `DATA/` (or keep existing ones).

4. **Build / refresh the vector index**

```bash
python store_index.py
```

This loads PDFs, splits text, creates 384-dim embeddings, and writes to a Pinecone index (default: `cura-chatbot`).

5. **Run the app**

```bash
python app.py
# or production-style:
gunicorn -b 0.0.0.0:8080 app:app
```

Visit: `http://localhost:8080`

---

## 🧠 How it Works (RAG)

1. **Ingestion**: Load PDFs → split into chunks → embed with HuggingFace → upsert to Pinecone.
2. **Retrieval**: For each query, fetch top-k similar chunks from Pinecone.
3. **Generation**: Feed retrieved context + prompt to Gemini via LangChain; return an answer.

---

## 🛣️ API (minimal)

* `GET /` → returns the chat UI.
* `POST /get` (form field `msg`) → returns the model answer string.

Example (cURL):

```bash
curl -X POST -F "msg=What are symptoms of anemia?" http://localhost:8080/get
```

---

## 🐳 Docker

Build & run locally:

```bash
docker build -t cura-chatbot .
docker run -p 8080:8080 --env-file .env cura-chatbot
```

---

## ☁️ Deploy (Google Cloud Run)

```bash
gcloud auth login
gcloud config set project YOUR_PROJECT_ID
gcloud run deploy cura-chatbot \
  --source . \
  --region asia-south1 \
  --allow-unauthenticated
```

**Env vars on Cloud Run:**

```bash
gcloud run services update cura-chatbot \
  --set-env-vars "PINECONE_API_KEY=xxxxx,GOOGLE_API_KEY=yyyyy"
```

> Alternatively, use **App Engine** (ensure `app.yaml` defines a Python runtime and entrypoint).

---

## 🧪 Tips & Troubleshooting

* **Index name mismatch**: Keep the same index name in `store_index.py` and `app.py` (default: `cura-chatbot`).
* **Dimensionality**: Embedding dimension must match the Pinecone index (here **384**).
* **Quota/auth**: Ensure both API keys are present and valid in `.env` or platform env vars.
* **CORS/UI**: The included UI posts form data to `/get`. Adjust templates as needed.

---

## 📜 License

See **LICENSE** in this repository.

---

## 👤 Author

**Jatin Bagga**
📧 [aloc1345@gmail.com](mailto:aloc1345@gmail.com)

**Chhavi Tokhi**
📧 [ctokhi_be22@thapar.edu](mailto:ctokhi_be22@thapar.edu)
