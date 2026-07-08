# AI Summary Workflow Studio

A containerized, high-throughput AI text processing and summarization pipeline. This application leverages **Groq's LPU hardware architecture** running **Llama 3.1** cloud models to generate dense, intelligent plain text summaries or beautifully formatted A4 PDF reports instantly.

The system features two access modes: an automated command-line execution interface built for DevOps/scripted pipelines, and an on-demand, interactive web dashboard.

## 🚀 Key Architectural Features
* **Dual-Interface System:** Supports high-velocity CLI commands (`--input`) or an elegant, live browser GUI.
* **Deterministic Layout Routing:** Programmatically parses intent layout keywords to prevent LLM formatting hallucinations.
* **Blistering Inference Speeds:** Integrated natively with the official `groq` Python SDK.
* **Isolated Environment Construction:** Fully containerized via Docker to standardize system pathings and eliminate cross-platform graphics crashes.
* **Dynamic Title Engine:** Intelligently extracts core subjects via LLM-driven response patterns.

---

## 🛠️ Installation & Setup

### 1. Prerequisites
Ensure you have the following installed on your host system:
* [Docker Desktop](https://www.docker.com/products/docker-desktop) (with WSL2 backend enabled)
* A valid **Groq API Key**

### 2. Configuration
Create a secure `.env` file in the root project folder to hold your access tokens (this file is excluded from git tracking automatically via `.gitignore`):

```env
GROQ_API_KEY=gsk_your_actual_groq_key_here
```

### 3. Build the Image
Compile the isolated container layer:

```bash
docker build -t ai-summarizer-workflow .
```

## 💻 How To Run

### Mode A: Web GUI Dashboard (Recommended)
Launch the responsive Streamlit layout on port 8501:

```bash
docker run --rm \
  --env-file .env \
  -p 8501:8501 \
  -v "$(pwd)/output:/workspace/output" \
  ai-summarizer-workflow
```

👉 Once running, open your browser and navigate to: http://localhost:8501

### Mode B: Automated CLI Pipeline
Execute a high-velocity processing job directly inside your terminal shell:

```bash
docker run --rm \
  --env-file .env \
  -v "$(pwd)/output:/workspace/output" \
  ai-summarizer-workflow \
  --input "summarize this in a pdf layout: [Paste your text payload here]"
```

## 📁 File Structure Layout

```
ai-summary-workflow/
├── app/
│   ├── __init__.py
│   ├── main.py          # CLI Workflow Routing Logic
│   ├── gui.py           # Streamlit Browser Architecture 
│   ├── llm_client.py    # Groq SDK Integration Layer
│   └── generator.py     # ReportLab PDF & TXT Compilation Engine
├── output/              # Local volume target directory for assets
├── Dockerfile           # Layer definitions for slim container virtualization
├── .dockerignore        # Context optimization filters
├── .gitignore           # Version control safeguards
└── requirements.txt     # Locked production python dependencies
```
