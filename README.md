# Student Information System

A modular Python Student Information System created for the Cloud Computing and GitHub Integration examination.

## Features

### Student Data Management
- Create/add student records
- Read/view student records
- Update student information
- Delete student records
- Search student records
- Persistent JSON storage
- CSV export

### Cloud-Ready Architecture
- Modular code structure
- External configuration file
- Error and exception handling
- Logging system
- Separate model, service, utility, and application layers

### Testing
- Unit tests for create/read, update, and delete operations

## Technologies

- Python 3
- JSON
- CSV
- Git
- GitHub
- Visual Studio Code

## Project Structure

```text
student-info-system/
├── src/
│   ├── models/
│   │   └── student.py
│   ├── services/
│   │   └── student_service.py
│   ├── utils/
│   │   ├── config.py
│   │   └── logger.py
│   └── main.py
├── data/
│   └── students.json
├── config/
│   └── config.json
├── logs/
├── tests/
│   └── test_student_service.py
├── README.md
├── requirements.txt
└── .gitignore
```

## How to Run

Open the project folder in VS Code and run:

```bash
python -m src.main
```

## How to Run Unit Tests

```bash
python -m unittest discover -s tests
```

## Data Persistence

Student records are stored in:

`data/students.json`

## Logging

Application events are stored in:

`logs/app.log`

## GitHub Repository

https://github.com/ralphdiolazocoast-stack/student-info-system
## Testing Completed

The Student Information System was tested for the following functions:

- Add Student
- View All Students
- View Student by ID
- Update Student
- Delete Student
- Search Student
- Export Students to CSV

