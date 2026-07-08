# app/llm_client.py
import os
from groq import Groq

def generate_summary(input_text: str) -> str:
    """
    Instructs Llama to generate a clean title and a concise summary block.
    """
    client = Groq()
    
    system_instruction = (
        "You are an expert content analyzer. Analyze the provided text and return your response in two distinct parts:\n"
        "1. A short, professional title based on the core subject matter (Start with 'TITLE: ')\n"
        "2. A comprehensive yet concise summary paragraph (Start with 'SUMMARY: ')\n\n"
        "Do not include any conversational filler, intros, or outros. Follow this format exactly:\n"
        "TITLE: [Your Generated Title Here]\n"
        "SUMMARY: [Your Summary Content Here]"
    )
    
    model_name = os.environ.get("GROQ_MODEL", "llama-3.1-8b-instant")

    response = client.chat.completions.create(
        model=model_name,
        messages=[
            {"role": "system", "content": system_instruction},
            {"role": "user", "content": f"Analyze this text:\n\n{input_text}"}
        ],
        temperature=0.3
    )
    
    return response.choices[0].message.content.strip()