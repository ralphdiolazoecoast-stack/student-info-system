import tempfile
import unittest
from pathlib import Path

from src.models.student import Student
from src.services.student_service import StudentService


class TestStudentService(unittest.TestCase):

    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.data_file = Path(self.temp_dir.name) / "students.json"
        self.service = StudentService(self.data_file)

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_create_and_read(self):
        student = Student("", "Test Student", "test@example.com", "BSIT", "2nd Year", 1.75)
        self.service.add_student(student.to_dict())

        result = self.service.get_student(student.student_id)

        self.assertIsNotNone(result)
        self.assertEqual(result.name, "Test Student")

    def test_update(self):
        student = Student("", "Old Name", "old@example.com", "BSIT", "1st Year", 2.0)
        self.service.add_student(student.to_dict())

        result = self.service.update_student(
            student.student_id,
            {"name": "New Name", "gpa": 1.5}
        )

        self.assertIsNotNone(result)
        self.assertEqual(result.name, "New Name")
        self.assertEqual(result.gpa, 1.5)

    def test_delete(self):
        student = Student("", "Delete Me", "delete@example.com", "BSIT", "1st Year", 2.0)
        self.service.add_student(student.to_dict())

        self.assertTrue(self.service.delete_student(student.student_id))
        self.assertIsNone(self.service.get_student(student.student_id))


if __name__ == "__main__":
    unittest.main()
