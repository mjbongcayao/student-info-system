# Student Information System

A Python-based Student Information System developed for a cloud computing and GitHub integration activity.

## Features

- Add new student records
- View all student records
- Update student information
- Delete student records
- Search students by ID, name, course, or email
- JSON data persistence
- External JSON configuration
- Application logging
- Input validation
- Exception handling
- Unit tests
- GitHub-ready modular project structure

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
│   │   ├── logger.py
│   │   └── validation.py
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

## Requirements

- Python 3.9 or newer
- Git
- GitHub account
- VS Code or another Python-compatible editor

## How to Run

Open a terminal in the project folder.

```bash
python -m src.main
```

On some Windows installations, use:

```bash
py -m src.main
```

## Run Tests

```bash
python -m unittest discover -s tests -v
```

## Data Storage

Student records are stored locally in:

`data/students.json`

Application settings are stored in:

`config/config.json`

Application logs are written to:

`logs/app.log`

## GitHub Workflow

Create a repository named `student-info-system`, then connect the local project:

```bash
git init
git add .
git commit -m "Initial project structure"
git branch -M main
git remote add origin https://github.com/mjbongcayao/student-info-system.git
git push -u origin main
```

For feature branches:

```bash
git checkout -b feature/student-crud
git add .
git commit -m "Implement student CRUD operations"
git push -u origin feature/student-crud
```

Create a pull request on GitHub and merge the feature branch into `main`.

## Error Handling

The application handles invalid input, missing configuration files, invalid JSON data, file access errors, duplicate student IDs, student records that cannot be found, and unexpected runtime errors.

## Logging

Important application events and errors are recorded in `logs/app.log`.

Log files are ignored by Git through `.gitignore` so generated runtime logs do not need to be committed.

## Future Improvements

- Web-based user interface
- Database integration such as MySQL or Firebase
- User authentication
- Role-based access
- CSV/PDF export
- Cloud deployment
- REST API
