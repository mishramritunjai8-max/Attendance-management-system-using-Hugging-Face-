import json
from datetime import date, datetime
from pathlib import Path

from .config import STUDENTS_FILE, START_DATE, END_DATE


def load_data() -> dict:
    with STUDENTS_FILE.open("r", encoding="utf-8") as file:
        return json.load(file)


def save_data(data: dict) -> None:
    with STUDENTS_FILE.open("w", encoding="utf-8") as file:
        json.dump(data, file, indent=4)


def normalize_date(value: str) -> str:
    """Convert common date formats into YYYY-MM-DD."""
    value = value.strip()

    formats = [
        "%Y-%m-%d",
        "%d-%m-%Y",
        "%d/%m/%Y",
        "%d %B %Y",
        "%d %b %Y",
        "%B %d %Y",
        "%b %d %Y",
    ]

    for fmt in formats:
        try:
            parsed = datetime.strptime(value, fmt).date()
            return parsed.isoformat()
        except ValueError:
            continue

    # Also support dates such as "10 Oct" for this project's fixed year.
    for fmt in ("%d %B", "%d %b"):
        try:
            parsed = datetime.strptime(value, fmt)
            return parsed.replace(year=2026).date().isoformat()
        except ValueError:
            continue

    raise ValueError(
        "Invalid date. Use a date from 8 Oct 2026 to 14 Oct 2026."
    )


def validate_project_date(date_str: str) -> None:
    if not START_DATE <= date_str <= END_DATE:
        raise ValueError(
            f"Date must be between {START_DATE} and {END_DATE}."
        )


def find_student(data: dict, identifier: str) -> dict:
    identifier = identifier.strip().lower()

    for student in data["students"]:
        if (
            student["name"].lower() == identifier
            or student["roll_no"].lower() == identifier
        ):
            return student

    # Friendly partial-name match if it is unique.
    matches = [
        student for student in data["students"]
        if identifier in student["name"].lower()
    ]

    if len(matches) == 1:
        return matches[0]

    raise ValueError(f"Student '{identifier}' was not found.")


def recalculate_student(student: dict) -> None:
    total_days = len(student["attendance"])
    days_present = sum(
        1 for value in student["attendance"].values() if value is True
    )

    student["days_present"] = days_present
    student["total_days"] = total_days
    student["present_percentage"] = round(
        (days_present / total_days) * 100, 2
    ) if total_days else 0.0


def recalculate_all(data: dict) -> None:
    for student in data["students"]:
        recalculate_student(student)


def initialize_calculated_fields(data: dict) -> None:
    """Ensure the JSON always contains calculated fields."""
    changed = False

    for student in data["students"]:
        before = (
            student.get("days_present"),
            student.get("total_days"),
            student.get("present_percentage"),
        )
        recalculate_student(student)
        after = (
            student["days_present"],
            student["total_days"],
            student["present_percentage"],
        )
        if before != after:
            changed = True

    if changed:
        save_data(data)
