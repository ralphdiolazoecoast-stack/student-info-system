from datetime import datetime
import uuid


class Student:
    """Student model used by the Student Information System."""

    def __init__(self, student_id, name, email, course, year_level, gpa=0.0,
                 created_at=None, updated_at=None):
        self.student_id = student_id or str(uuid.uuid4())[:8]
        self.name = name
        self.email = email
        self.course = course
        self.year_level = year_level
        self.gpa = float(gpa)
        self.created_at = created_at or datetime.now().isoformat()
        self.updated_at = updated_at or self.created_at

    def to_dict(self):
        return {
            "student_id": self.student_id,
            "name": self.name,
            "email": self.email,
            "course": self.course,
            "year_level": self.year_level,
            "gpa": self.gpa,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            student_id=data.get("student_id"),
            name=data["name"],
            email=data["email"],
            course=data["course"],
            year_level=data["year_level"],
            gpa=data.get("gpa", 0.0),
            created_at=data.get("created_at"),
            updated_at=data.get("updated_at")
        )

    def __str__(self):
        return (
            f"ID: {self.student_id} | Name: {self.name} | "
            f"Email: {self.email} | Course: {self.course} | "
            f"Year: {self.year_level} | GPA: {self.gpa:.2f}"
        )
