# Student Information System

![CI](https://github.com/<your-username>/student-info-system/actions/workflows/ci.yml/badge.svg)

A cloud-ready, command-line Student Information System written in Python.
It supports full CRUD for student records, stores data in JSON, and is built
with a modular structure, externalised configuration, error handling and logging.

## Features
- **Add / View / Update / Delete** students (ID, name, age, email, course, phone), plus keyword search
- **JSON storage** with atomic writes (no half-written files)
- **Validation** (required fields, age range, email format, unique IDs)
- **Configuration** via `config/config.json`, overridable with environment variables
- **Rotating log file** (`logs/app.log`)
- **Unit tests** and a **GitHub Actions** CI pipeline

## Project Structure
```
student-info-system/
├── .github/workflows/ci.yml   # automated tests + lint
├── src/
│   ├── models/student.py      # Student model + validation
│   ├── services/student_service.py  # CRUD + JSON persistence
│   ├── utils/                 # config, logger, custom exceptions
│   └── main.py                # CLI entry point
├── data/students.json         # data store
├── config/config.json         # settings
├── logs/                      # runtime logs (git-ignored)
├── tests/                     # unit tests
├── requirements.txt
└── README.md
```

## Getting Started
Requires Python 3.9+.

```bash
git clone https://github.com/<your-username>/student-info-system.git
cd student-info-system
python -m src.main
```

## Configuration
| Setting     | config.json key | Environment variable |
|-------------|-----------------|----------------------|
| Data file   | `data_file`     | `SIS_DATA_FILE`      |
| Log file    | `log_file`      | `SIS_LOG_FILE`       |
| Log level   | `log_level`     | `SIS_LOG_LEVEL`      |

Example (e.g. a container or cloud VM using a mounted volume):
```bash
SIS_DATA_FILE=/mnt/data/students.json SIS_LOG_LEVEL=DEBUG python -m src.main
```

## Running Tests
```bash
pip install -r requirements.txt
python -m pytest -v
```

## Data Format
```json
{
  "student_id": "2024-001",
  "name": "Maria Santos",
  "age": 20,
  "email": "maria.santos@example.com",
  "course": "BS Computer Science",
  "phone": "09171234567"
}
```

## Cloud-Readiness Notes
- Configuration is separated from code and overridable by environment variables.
- Storage is isolated in `StudentService`, so JSON can later be swapped for a
  cloud database (e.g. DynamoDB, Firestore) without touching the CLI.
- Logging is structured and rotated, ready to ship to a log aggregator.

## Contributing
Fork, create a feature branch (`feature/<name>`), open a pull request.
CI must pass before merging.

## Author
<Your Name>
