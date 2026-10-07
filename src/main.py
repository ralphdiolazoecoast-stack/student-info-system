from pathlib import Path

from src.services.student_service import StudentService
from src.utils.config import load_config
from src.utils.logger import logger


def display_menu():
    print("\n" + "=" * 55)
    print("              STUDENT INFORMATION SYSTEM")
    print("=" * 55)
    print("1. Add Student")
    print("2. View All Students")
    print("3. View Student by ID")
    print("4. Update Student")
    print("5. Delete Student")
    print("6. Search Student")
    print("7. Export Students to CSV")
    print("8. Exit")


def get_gpa():
    while True:
        try:
            gpa = float(input("GPA (0.00 - 4.00): "))
            if 0.0 <= gpa <= 4.0:
                return gpa
            print("GPA must be between 0.00 and 4.00.")
        except ValueError:
            print("Please enter a valid GPA.")


def add_student(service):
    print("\n--- Add New Student ---")
    student_id = input("Student ID (leave blank for automatic ID): ").strip()
    name = input("Name: ").strip()
    email = input("Email: ").strip()
    course = input("Course: ").strip()
    year_level = input("Year Level: ").strip()
    gpa = get_gpa()

    if not all([name, email, course, year_level]):
        print("Name, email, course, and year level are required.")
        return

    try:
        student = service.add_student({
            "student_id": student_id,
            "name": name,
            "email": email,
            "course": course,
            "year_level": year_level,
            "gpa": gpa
        })
        print(f"Student added successfully! ID: {student.student_id}")
    except (ValueError, OSError) as error:
        print(f"Error: {error}")
        logger.error("Error adding student: %s", error)


def view_all_students(service):
    print("\n--- All Students ---")
    students = service.get_all_students()

    if not students:
        print("No students found.")
        return

    for student in students:
        print(student)


def view_student(service):
    student_id = input("Enter Student ID: ").strip()
    student = service.get_student(student_id)

    if student:
        print("\nStudent Details:")
        print(student)
        print(f"Created: {student.created_at}")
        print(f"Updated: {student.updated_at}")
    else:
        print("Student not found.")


def update_student(service):
    student_id = input("Enter Student ID to update: ").strip()
    student = service.get_student(student_id)

    if not student:
        print("Student not found.")
        return

    print("Press Enter to keep the current value.")
    name = input(f"Name [{student.name}]: ").strip()
    email = input(f"Email [{student.email}]: ").strip()
    course = input(f"Course [{student.course}]: ").strip()
    year_level = input(f"Year Level [{student.year_level}]: ").strip()
    gpa_input = input(f"GPA [{student.gpa:.2f}]: ").strip()

    update_data = {
        "name": name or student.name,
        "email": email or student.email,
        "course": course or student.course,
        "year_level": year_level or student.year_level,
        "gpa": student.gpa if not gpa_input else gpa_input
    }

    try:
        updated = service.update_student(student_id, update_data)
        if updated:
            print("Student updated successfully.")
        else:
            print("Student not found.")
    except ValueError:
        print("Invalid GPA. Please enter a number from 0.00 to 4.00.")


def delete_student(service):
    student_id = input("Enter Student ID to delete: ").strip()
    student = service.get_student(student_id)

    if not student:
        print("Student not found.")
        return

    print(f"Student: {student.name}")
    confirm = input("Are you sure you want to delete this student? (y/n): ").strip().lower()

    if confirm == "y":
        if service.delete_student(student_id):
            print("Student deleted successfully.")
    else:
        print("Delete cancelled.")


def search_student(service):
    keyword = input("Enter ID, name, email, or course: ").strip()
    results = service.search_students(keyword)

    if not results:
        print("No matching students found.")
        return

    print("\n--- Search Results ---")
    for student in results:
        print(student)


def export_students(service):
    output = Path("data") / "students_export.csv"
    service.export_csv(output)
    print(f"Students exported successfully to: {output}")


def main():
    config = load_config()
    service = StudentService(config["data_file"])

    while True:
        display_menu()
        choice = input("Enter your choice (1-8): ").strip()

        try:
            if choice == "1":
                add_student(service)
            elif choice == "2":
                view_all_students(service)
            elif choice == "3":
                view_student(service)
            elif choice == "4":
                update_student(service)
            elif choice == "5":
                delete_student(service)
            elif choice == "6":
                search_student(service)
            elif choice == "7":
                export_students(service)
            elif choice == "8":
                print("Goodbye!")
                break
            else:
                print("Invalid choice. Please choose 1-8.")
        except Exception as error:
            logger.exception("Unexpected application error")
            print(f"Unexpected error: {error}")


if __name__ == "__main__":
    main()
