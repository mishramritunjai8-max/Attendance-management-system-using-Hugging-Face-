import json

from src.config import LAST_RESPONSE_FILE
from src.data_manager import load_data, initialize_calculated_fields
from src.hf_client import parse_command
from src.attendance_service import process_action


def write_last_response(response: dict) -> None:
    LAST_RESPONSE_FILE.parent.mkdir(parents=True, exist_ok=True)

    with LAST_RESPONSE_FILE.open("w", encoding="utf-8") as file:
        json.dump(response, file, indent=4)


def main() -> None:
    print("=" * 60)
    print("AI ATTENDANCE MANAGEMENT SYSTEM")
    print("=" * 60)
    print("Attendance data: json/students.json")
    print("Type 'help' for examples or 'exit' to quit.")
    print()

    data = load_data()
    initialize_calculated_fields(data)

    while True:
        try:
            user_text = input("Attendance AI > ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\nExiting...")
            break

        if not user_text:
            continue

        if user_text.lower() in {"exit", "quit"}:
            print("Goodbye!")
            break

        if user_text.lower() == "help":
            print(
                """
Examples:
  Was Aarav Sharma present on 10 Oct 2026?
  Was roll 101 present on 8 Oct 2026?
  Mark Priya Verma present on 9 Oct 2026
  Remove Rahul Kumar attendance on 11 Oct 2026
  What is Aarav Sharma's attendance percentage?
  Show all attendance percentages
  What is the class attendance average?
"""
            )
            continue

        try:
            # 1. Hugging Face interprets the natural-language command.
            ai_command = parse_command(user_text)

            # 2. Python validates and performs the real operation.
            response = process_action(data, ai_command)

            # 3. Every final response is stored as JSON.
            write_last_response(response)

            # Reload so future commands always use the latest file contents.
            data = load_data()

            print(json.dumps(response, indent=4))

        except Exception as exc:
            response = {
                "status": "error",
                "error": str(exc),
            }
            write_last_response(response)
            print(json.dumps(response, indent=4))


if __name__ == "__main__":
    main()
