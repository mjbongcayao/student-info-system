"""Student model with built-in validation."""
import re
from dataclasses import dataclass, asdict

from src.utils.exceptions import ValidationError

_EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")
_PHONE_RE = re.compile(r"^\+?[\d\s\-]{7,15}$")


@dataclass
class Student:
    """Represents a single student record."""

    student_id: str
    name: str
    age: int
    email: str
    course: str
    phone: str = ""

    def __post_init__(self):
        self.validate()

    def validate(self) -> None:
        """Raise ValidationError if any field is invalid."""
        self.student_id = str(self.student_id).strip()
        self.name = str(self.name).strip()
        self.email = str(self.email).strip()
        self.course = str(self.course).strip()
        self.phone = str(self.phone).strip()

        if not self.student_id:
            raise ValidationError("Student ID is required.")
        if not self.name:
            raise ValidationError("Name is required.")
        try:
            self.age = int(self.age)
        except (TypeError, ValueError):
            raise ValidationError("Age must be a whole number.")
        if not 10 <= self.age <= 100:
            raise ValidationError("Age must be between 10 and 100.")
        if not _EMAIL_RE.match(self.email):
            raise ValidationError(f"Invalid email address: '{self.email}'.")
        if not self.course:
            raise ValidationError("Course is required.")
        if self.phone and not _PHONE_RE.match(self.phone):
            raise ValidationError(f"Invalid phone number: '{self.phone}'.")

    def to_dict(self) -> dict:
        """Serialize to a JSON-friendly dict."""
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict) -> "Student":
        """Build a Student from a dict (e.g. loaded from JSON)."""
        try:
            return cls(
                student_id=data["student_id"],
                name=data["name"],
                age=data["age"],
                email=data["email"],
                course=data["course"],
                phone=data.get("phone", ""),
            )
        except KeyError as exc:
            raise ValidationError(f"Missing field in student data: {exc}") from exc

    def __str__(self) -> str:
        return (f"{self.student_id} | {self.name} | Age: {self.age} | "
                f"{self.course} | {self.email} | {self.phone}")
