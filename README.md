# 💡 Jargon Buster

A clean, modern single-file Streamlit application that transforms complex, convoluted technical prose into simplified plain-English summaries in **exactly 3 bullet points**, powered by Groq's high-speed inference running **`llama-3.3-70b-versatile`**.

---

## 🚀 Quick Start

### 1. Activate the Virtual Environment

**Windows (PowerShell):**
```powershell
.\.venv\Scripts\Activate.ps1
```

**Windows (Command Prompt):**
```cmd
.venv\Scripts\activate.bat
```

**macOS / Linux:**
```bash
source .venv/bin/activate
```

---

### 2. Configure Your Groq API Key

Get a free API key from [Groq Console](https://console.groq.com/keys).

You can either:
- Enter it directly into the sidebar text field in the app UI, OR
- Create a `.env` file in the project root:
  ```env
  GROQ_API_KEY=gsk_your_actual_key_here
  ```

---

### 3. Run the App

```bash
streamlit run app.py
```
Or directly using the virtual environment python:
```powershell
.\.venv\Scripts\streamlit.exe run app.py
```

---

## 🛠 Tech Stack

- **Framework**: Streamlit
- **LLM Engine**: Groq Cloud API
- **Model**: `llama-3.3-70b-versatile`
- **Configuration**: `python-dotenv`
