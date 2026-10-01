import os
import streamlit as st
from groq import Groq
from dotenv import load_dotenv

# Load local environment variables from .env if present
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="Jargon Buster",
    page_icon="🔍",
    layout="centered",
    initial_sidebar_state="expanded"
)

# Custom Styling
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', sans-serif;
    }
    
    .hero-container {
        text-align: center;
        padding: 1.5rem 0 2rem 0;
    }
    
    .hero-title {
        font-size: 2.5rem;
        font-weight: 800;
        background: linear-gradient(135deg, #FF6B6B 0%, #FF8E53 50%, #FFA07A 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.5rem;
    }
    
    .hero-subtitle {
        font-size: 1.1rem;
        color: #6c757d;
        margin-bottom: 1.5rem;
    }
    
    .result-card {
        background: rgba(255, 142, 83, 0.06);
        border: 1px solid rgba(255, 142, 83, 0.25);
        border-radius: 12px;
        padding: 1.5rem;
        margin-top: 1.5rem;
    }
    
    .result-badge {
        display: inline-block;
        background: #FF6B6B;
        color: white;
        font-size: 0.75rem;
        font-weight: 700;
        padding: 0.25rem 0.6rem;
        border-radius: 9999px;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        margin-bottom: 1rem;
    }
    
    .bullet-item {
        margin-bottom: 1rem;
        font-size: 1.05rem;
        line-height: 1.6;
    }
    
    .footer-note {
        text-align: center;
        color: #9e9e9e;
        font-size: 0.85rem;
        margin-top: 3rem;
    }
</style>
""", unsafe_allow_html=True)

# Sidebar for configuration
with st.sidebar:
    st.header("⚙️ Configuration")
    
    env_api_key = os.getenv("GROQ_API_KEY", "")
    api_key_input = st.text_input(
        "Groq API Key",
        value=env_api_key,
        type="password",
        help="Enter your Groq API Key. Get one for free at console.groq.com/keys"
    )
    
    # Selected Model
    model_options = [
        "llama-3.3-70b-versatile",
        "openai/gpt-oss-120b",
        "qwen/qwen3.8-27b",
        "openai/gpt-oss-20b"
    ]
    selected_model = st.selectbox(
        "Select Model",
        options=model_options,
        index=0,
        help="llama-3.3-70b-versatile is the default. If your Groq key has access to different models, you can switch here."
    )
    st.caption("⚡ High-speed inference via Groq.")
    
    st.divider()
    st.markdown("### 💡 Quick Samples")
    sample_options = {
        "Custom Input": "",
        "Kubernetes & Orchestration": (
            "Kubernetes orchestrates containerized workloads across heterogeneous clusters using declarative manifests, "
            "implementing control loops via kube-controller-manager to reconcile the observed cluster state with the "
            "desired state, alongside etcd for distributed, linearizable state persistence and consensus."
        ),
        "Quantum Computing": (
            "Superconducting qubits utilize Josephson junctions operating in cryogenic regimes to sustain quantum superposition "
            "and entanglement, mitigating decoherence and bit-flip phase noise via surface-code quantum error correction schemes."
        ),
        "Microservices & Event-Driven": (
            "The distributed architecture implements event sourcing with CQRS, utilizing Apache Kafka partitioned topic logs for "
            "idempotent consumer group offset management and eventual consistency across isolated polyglot persistence layers."
        )
    }
    
    selected_sample = st.selectbox("Load sample jargon text:", list(sample_options.keys()))

# Main Content
st.markdown("""
<div class="hero-container">
    <div class="hero-title">💡 Jargon Buster</div>
    <div class="hero-subtitle">Transform convoluted technical mumbo-jumbo into 3 crisp, plain-English bullet points.</div>
</div>
""", unsafe_allow_html=True)

# Input text determination
initial_text = sample_options[selected_sample] if selected_sample != "Custom Input" else ""

user_input = st.text_area(
    "Paste your complex, technical text below:",
    value=initial_text,
    height=160,
    placeholder="e.g., 'The distributed consensus algorithm leverages Raft state machines with heartbeats to maintain atomic broadcast...'"
)

col1, col2 = st.columns([1, 4])
with col1:
    bust_button = st.button("🚀 Bust Jargon", type="primary", use_container_width=True)

if bust_button:
    groq_api_key = api_key_input.strip() or os.getenv("GROQ_API_KEY", "").strip()

    if not groq_api_key:
        st.error("🔑 Please provide a Groq API Key in the sidebar or via the `GROQ_API_KEY` environment variable.")
    elif not user_input.strip():
        st.warning("⚠️ Please provide some technical text to analyze.")
    else:
        with st.spinner("Analyzing jargon and translating to plain English..."):
            try:
                client = Groq(api_key=groq_api_key)
                
                system_prompt = (
                    "You are 'Jargon Buster', an expert at distilling hyper-technical and convoluted prose "
                    "into crystal-clear, plain-English summaries that anyone can understand.\n\n"
                    "Rules:\n"
                    "1. Provide a simplified plain-English summary in EXACTLY 3 bullet points.\n"
                    "2. Avoid using technical jargon in the explanation; if a key term must be mentioned, define it simply.\n"
                    "3. Each bullet point should start with a bold title/theme followed by an explanation.\n"
                    "4. Do NOT output any intro or outro text. Output only the 3 bullet points."
                )
                
                chat_completion = client.chat.completions.create(
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {
                            "role": "user",
                            "content": f"Simplify this technical text into exactly 3 plain-English bullet points:\n\n{user_input.strip()}"
                        }
                    ],
                    model=selected_model,
                    temperature=0.3,
                    max_tokens=500
                )
                
                result_text = chat_completion.choices[0].message.content.strip()
                
                st.markdown("""
                <div class="result-card">
                    <span class="result-badge">Plain English Summary</span>
                """, unsafe_allow_html=True)
                
                st.markdown(result_text)
                st.markdown("</div>", unsafe_allow_html=True)
                
            except Exception as e:
                err_msg = str(e)
                st.error(f"❌ Groq API Error: {err_msg}")
                if "model_not_found" in err_msg or "does not exist" in err_msg:
                    st.info(
                        f"💡 **Tip:** `{selected_model}` might not be provisioned for your Groq tier or region. "
                        "Try selecting another model in the sidebar, such as `openai/gpt-oss-120b` or `qwen/qwen3.8-27b`."
                    )

st.markdown(f"""
<div class="footer-note">
    Powered by <strong>{selected_model}</strong> on <strong>Groq</strong>
</div>
""", unsafe_allow_html=True)

