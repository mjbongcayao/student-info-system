"""Student service: CRUD operations backed by a JSON file."""
import json
import logging
import os
import tempfile
from pathlib import Path
from typing import Dict, List

from src.models.student import Student
from src.utils.exceptions import (
    DuplicateStudentError,
    StorageError,
    StudentNotFoundError,
    ValidationError,
)

logger = logging.getLogger("sis.service")


class StudentService:
    """Business logic for managing students and persisting them to JSON."""

    def __init__(self, data_file: str):
        self.data_file = Path(data_file)
        self._students: Dict[str, Student] = {}
        self._load()

    # ---------- persistence ----------
    def _load(self) -> None:
        """Load students from disk. A missing file means an empty database."""
        if not self.data_file.exists():
            logger.info("Data file %s not found; starting empty.", self.data_file)
            return
        try:
            with open(self.data_file, "r", encoding="utf-8") as fh:
                raw = json.load(fh)
            for item in raw:
                student = Student.from_dict(item)
                self._students[student.student_id] = student
            logger.info("Loaded %d students.", len(self._students))
        except json.JSONDecodeError as exc:
            logger.error("Corrupt data file: %s", exc)
            raise StorageError(f"Data file is not valid JSON: {exc}") from exc
        except (OSError, ValidationError) as exc:
            logger.error("Failed to load data: %s", exc)
            raise StorageError(f"Could not load data: {exc}") from exc

    def _save(self) -> None:
        """Write atomically (temp file + rename) so a crash can't corrupt data."""
        try:
            self.data_file.parent.mkdir(parents=True, exist_ok=True)
            fd, tmp_path = tempfile.mkstemp(dir=self.data_file.parent, suffix=".tmp")
            with os.fdopen(fd, "w", encoding="utf-8") as fh:
                json.dump([s.to_dict() for s in self._students.values()],
                          fh, indent=2)
            os.replace(tmp_path, self.data_file)
        except OSError as exc:
            logger.error("Failed to save data: %s", exc)
            raise StorageError(f"Could not save data: {exc}") from exc

    # ---------- CRUD ----------
    def add_student(self, student_id, name, age, email, course, phone="") -> Student:
        """Create and store a new student."""
        student = Student(student_id, name, age, email, course, phone)
        if student.student_id in self._students:
            raise DuplicateStudentError(
                f"Student ID '{student.student_id}' already exists.")
        self._students[student.student_id] = student
        self._save()
        logger.info("Added student %s", student.student_id)
        return student

    def get_student(self, student_id: str) -> Student:
        """Return one student by ID."""
        try:
            return self._students[str(student_id).strip()]
        except KeyError:
            raise StudentNotFoundError(f"No student with ID '{student_id}'.")

    def list_students(self) -> List[Student]:
        """Return all students sorted by ID."""
        return sorted(self._students.values(), key=lambda s: s.student_id)

    def search_students(self, keyword: str) -> List[Student]:
        """Case-insensitive search across name, course and email."""
        kw = keyword.lower().strip()
        return [s for s in self.list_students()
                if kw in s.name.lower() or kw in s.course.lower()
                or kw in s.email.lower() or kw in s.phone]

    def update_student(self, student_id: str, **changes) -> Student:
        """Update any of: name, age, email, course, phone. Blank/None values are ignored."""
        current = self.get_student(student_id)
        allowed = {"name", "age", "email", "course", "phone"}
        unknown = set(changes) - allowed
        if unknown:
            raise ValidationError(f"Cannot update field(s): {', '.join(unknown)}")
        data = current.to_dict()
        data.update({k: v for k, v in changes.items() if v not in (None, "")})
        updated = Student.from_dict(data)  # re-validates
        self._students[updated.student_id] = updated
        self._save()
        logger.info("Updated student %s", updated.student_id)
        return updated

    def delete_student(self, student_id: str) -> None:
        """Remove a student."""
        student = self.get_student(student_id)
        del self._students[student.student_id]
        self._save()
        logger.info("Deleted student %s", student.student_id)
