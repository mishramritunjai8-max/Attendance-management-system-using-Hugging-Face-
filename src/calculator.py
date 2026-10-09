def student_percentage(student: dict) -> float:
    total = len(student["attendance"])
    present = sum(1 for value in student["attendance"].values() if value is True)
    return round((present / total) * 100, 2) if total else 0.0


def all_student_percentages(data: dict) -> list[dict]:
    result = []

    for student in data["students"]:
        percentage = student_percentage(student)
        result.append(
            {
                "name": student["name"],
                "roll_no": student["roll_no"],
                "days_present": sum(
                    1 for value in student["attendance"].values() if value is True
                ),
                "total_days": len(student["attendance"]),
                "present_percentage": percentage,
            }
        )

    return result


def class_attendance_average(data: dict) -> float:
    percentages = [
        item["present_percentage"]
        for item in all_student_percentages(data)
    ]

    return round(sum(percentages) / len(percentages), 2) if percentages else 0.0
