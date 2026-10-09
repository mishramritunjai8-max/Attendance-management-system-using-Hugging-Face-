import os
from dotenv import load_dotenv
from huggingface_hub import InferenceClient
from pathlib import Path

ROOT = Path(__file__).resolve().parent
load_dotenv(ROOT / ".env")
token = os.getenv("HF_TOKEN")
model = os.getenv("HF_MODEL", "Qwen/Qwen2.5-7B-Instruct-1M")

if not token or token == "hf_paste_your_token_here":
    raise SystemExit("HF_TOKEN is missing. Add your token to the .env file in this folder.")

print("HF token loaded: yes (hidden)")
print(f"Model configured: {model}")
print("Testing Hugging Face Inference Providers...")

try:
    client = InferenceClient(api_key=token, provider="auto")
    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": "Reply with exactly: Hugging Face connection successful."}],
        temperature=0,
        max_tokens=50,
    )
    print("Model response:")
    print(response.choices[0].message.content)
except Exception as exc:
    print("\nHugging Face request failed:")
    print(f"{type(exc).__name__}: {exc}")
    print("\nIf the error says model_not_supported, choose a model with an enabled Inference Provider.")
    print("If it says insufficient credits, changing the token/model will not create free credits for that account.")
    raise SystemExit(1)
