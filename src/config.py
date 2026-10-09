from pathlib import Path
import os
from dotenv import load_dotenv

ROOT_DIR = Path(__file__).resolve().parent.parent
JSON_DIR = ROOT_DIR / "json"
OUTPUT_DIR = ROOT_DIR / "outputs"

STUDENTS_FILE = JSON_DIR / "students.json"
LAST_RESPONSE_FILE = OUTPUT_DIR / "last_response.json"

load_dotenv(ROOT_DIR / ".env")

HF_TOKEN = os.getenv("HF_TOKEN")
HF_MODEL = os.getenv("HF_MODEL", "openai/gpt-oss-20b")

START_DATE = "2026-10-08"
END_DATE = "2026-10-14"
