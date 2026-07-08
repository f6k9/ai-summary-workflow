# app/gui.py
import sys
import os
# Force Python to include the root /workspace directory in its search path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import streamlit as st
import os
from app.llm_client import generate_summary
from app.generator import create_txt, create_pdf

st.set_page_config(page_title="AI Workflow Studio", layout="centered")

st.title("🤖 AI Workflow Summarizer")
st.write("Enter your routing instructions and text context below.")

# Capture User Input
user_input = st.text_area("Your Request & Payload:", height=250, placeholder="e.g., summarize this in a pdf... [paste text here]")

if st.button("Execute Pipeline", type="primary"):
    if not user_input.strip():
        st.error("Input area cannot be left empty!")
    else:
        with st.spinner("Processing text through Llama (Groq LPU)..."):
            payload_lower = user_input.lower()
            if "pdf" in payload_lower:
                chosen_format = "pdf"
            else:
                chosen_format = "txt"
            
            try:
                summary_content = generate_summary(input_text=user_input)
                
                output_dir = "/workspace/output"
                os.makedirs(output_dir, exist_ok=True)
                
                if chosen_format == "pdf":
                    output_path = os.path.join(output_dir, "summarize.pdf")
                    create_pdf(content=summary_content, output_path=output_path)
                    st.success("🎉 Successfully rendered A4 Document layout: `output/summarize.pdf`")
                else:
                    output_path = os.path.join(output_dir, "summarize.txt")
                    create_txt(content=summary_content, output_path=output_path)
                    st.success("🎉 Successfully saved text file: `output/summarize.txt`")
                    
                st.info("### Summary Preview")
                st.write(summary_content)
                
            except Exception as e:
                st.error(f"Pipeline execution error: {e}")