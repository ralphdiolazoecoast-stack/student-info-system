import json
import csv
from datetime import datetime
from pathlib import Path

from src.models.student import Student
from src.utils.logger import logger


class StudentService:
    """Provides CRUD operations and JSON persistence for students."""

    def __init__(self, data_file="data/students.json"):
        self.data_file = Path(data_file)
        self._ensure_data_file()

    def _ensure_data_file(self):
        self.data_file.parent.mkdir(parents=True, exist_ok=True)
        if not self.data_file.exists():
            self._save_students([])

    def _load_students(self):
        try:
            with open(self.data_file, "r", encoding="utf-8") as file:
                data = json.load(file)
                return [Student.from_dict(item) for item in data]
        except (FileNotFoundError, json.JSONDecodeError, KeyError, TypeError) as error:
            logger.error("Error loading students: %s", error)
            return []

    def _save_students(self, students):
        try:
            with open(self.data_file, "w", encoding="utf-8") as file:
                json.dump(
                    [student.to_dict() for student in students],
                    file,
                    indent=4
                )
        except OSError as error:
            logger.error("Error saving students: %s", error)
            raise

    def add_student(self, student_data):
        students = self._load_students()

        student_id = student_data.get("student_id") or str(__import__("uuid").uuid4())[:8]
        if any(student.student_id == student_id for student in students):
            raise ValueError("Student ID already exists.")

        student_data["student_id"] = student_id
        student = Student(**student_data)
        students.append(student)
        self._save_students(students)
        logger.info("Added student %s", student.student_id)
        return student

    def get_all_students(self):
        return self._load_students()

    def get_student(self, student_id):
        students = self._load_students()
        for student in students:
            if student.student_id.lower() == student_id.lower():
                return student
        return None

    def update_student(self, student_id, update_data):
        students = self._load_students()

        for student in students:
            if student.student_id.lower() == student_id.lower():
                for field in ["name", "email", "course", "year_level", "gpa"]:
                    if field in update_data and update_data[field] not in ("", None):
                        if field == "gpa":
                            student.gpa = float(update_data[field])
                        else:
                            setattr(student, field, update_data[field])

                student.updated_at = datetime.now().isoformat()
                self._save_students(students)
                logger.info("Updated student %s", student_id)
                return student

        return None

    def delete_student(self, student_id):
        students = self._load_students()
        original_count = len(students)

        students = [
            student for student in students
            if student.student_id.lower() != student_id.lower()
        ]

        if len(students) == original_count:
            return False

        self._save_students(students)
        logger.info("Deleted student %s", student_id)
        return True

    def search_students(self, keyword):
        keyword = keyword.lower()
        return [
            student for student in self._load_students()
            if keyword in student.student_id.lower()
            or keyword in student.name.lower()
            or keyword in student.email.lower()
            or keyword in student.course.lower()
        ]

    def export_csv(self, output_file="data/students_export.csv"):
        students = self._load_students()

        with open(output_file, "w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(
                file,
                fieldnames=[
                    "student_id", "name", "email", "course",
                    "year_level", "gpa", "created_at", "updated_at"
                ]
            )
            writer.writeheader()
            for student in students:
                writer.writerow(student.to_dict())

        logger.info("Exported students to %s", output_file)
        return output_file
