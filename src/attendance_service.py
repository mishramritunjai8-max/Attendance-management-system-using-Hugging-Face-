from .calculator import all_student_percentages, class_attendance_average
from .data_manager import (
    find_student,
    normalize_date,
    recalculate_all,
    save_data,
    validate_project_date,
)


def process_action(data: dict, command: dict) -> dict:
    action = command["action"]
    student_identifier = command.get("student")
    date_value = command.get("date")

    if action == "class_average":
        recalculate_all(data)
        return {
            "status": "success",
            "action": action,
            "class_attendance_average": class_attendance_average(data),
            "students": all_student_percentages(data),
        }

    if action == "all_percentages":
        recalculate_all(data)
        return {
            "status": "success",
            "action": action,
            "students": all_student_percentages(data),
            "class_attendance_average": class_attendance_average(data),
        }

    if action == "student_percentage":
        student = find_student(data, student_identifier)
        recalculate_all(data)
        return {
            "status": "success",
            "action": action,
            "student": {
                "name": student["name"],
                "roll_no": student["roll_no"],
                "days_present": student["days_present"],
                "total_days": student["total_days"],
                "present_percentage": student["present_percentage"],
            },
        }

    if action in {
        "check_attendance",
        "mark_attendance",
        "remove_attendance",
    }:
        if not student_identifier:
            raise ValueError("A student name or roll number is required.")

        if not date_value:
            raise ValueError("A date is required for this action.")

        normalized_date = normalize_date(date_value)
        validate_project_date(normalized_date)

        student = find_student(data, student_identifier)

        if normalized_date not in student["attendance"]:
            raise ValueError(
                f"No attendance record exists for {normalized_date}."
            )

        if action == "check_attendance":
            present = student["attendance"][normalized_date]

            return {
                "status": "success",
                "action": action,
                "student": student["name"],
                "roll_no": student["roll_no"],
                "date": normalized_date,
                "present": present,
            }

        if action == "mark_attendance":
            student["attendance"][normalized_date] = True
            message = "Attendance marked as present."

        else:
            student["attendance"][normalized_date] = False
            message = "Attendance removed/marked absent."

        recalculate_all(data)
        save_data(data)

        updated_student = find_student(data, student["roll_no"])

        return {
            "status": "success",
            "action": action,
            "message": message,
            "student": updated_student["name"],
            "roll_no": updated_student["roll_no"],
            "date": normalized_date,
            "present": updated_student["attendance"][normalized_date],
            "days_present": updated_student["days_present"],
            "total_days": updated_student["total_days"],
            "present_percentage": updated_student["present_percentage"],
        }

    raise ValueError(f"Unsupported action: {action}")
