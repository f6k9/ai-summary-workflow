# app/main.py
import os
import sys
import argparse
from app.llm_client import generate_summary
from app.generator import create_txt, create_pdf

def main():
    # 1. Take a single unified input string
    parser = argparse.ArgumentParser(description="AI Workflow Container (Single Input Mode)")
    parser.add_argument(
        "--input", 
        type=str, 
        required=True, 
        help="The entire user request (e.g., 'Summarize this in a pdf... [your text here]')"
    )
    args = parser.parse_args()

    # Configure Ollama Network Layer for Docker
    if "OLLAMA_HOST" not in os.environ:
        os.environ["OLLAMA_HOST"] = "http://host.docker.internal:11434"

    # 2. Python scans the entire input text for the formatting intent
    user_payload = args.input.lower()
    
    if "pdf" in user_payload:
        chosen_format = "pdf"
    elif "txt" in user_payload or "text" in user_payload:
        chosen_format = "txt"
    else:
        print("[WARN] No explicit format detected in your text. Defaulting to plain text.")
        chosen_format = "txt"

    print(f"[INFO] Python detected requested format: {chosen_format.upper()}")

    try:
        # 3. Pass the entire text directly to Llama
        print("[INFO] Sending text block to Llama for summarization...")
        summary_content = generate_summary(input_text=args.input)
        
        # Setup workspace output directory
        output_dir = "/workspace/output"
        os.makedirs(output_dir, exist_ok=True)

        # 4. Route payload straight to chosen Python generator modules
        if chosen_format == "pdf":
            output_path = os.path.join(output_dir, "summarize.pdf")
            print(f"[SUCCESS] Rendering clean A4 Document layout at: {output_path}")
            create_pdf(content=summary_content, output_path=output_path)
        else:
            output_path = os.path.join(output_dir, "summarize.txt")
            print(f"[SUCCESS] Saving text file at: {output_path}")
            create_txt(content=summary_content, output_path=output_path)

    except Exception as e:
        print(f"[FATAL ERROR] Pipeline execution halted: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()