import os
import tempfile
import unittest

from src.services.student_service import StudentService
from src.utils.exceptions import (DuplicateStudentError, StorageError,
                                  StudentNotFoundError, ValidationError)


class StudentServiceTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.path = os.path.join(self.tmp.name, "students.json")
        self.svc = StudentService(self.path)

    def tearDown(self):
        self.tmp.cleanup()

    def _add(self, sid="1"):
        return self.svc.add_student(sid, "Ana Reyes", 20, "ana@x.com", "BSCS", "09171234567")

    def test_add_and_get(self):
        self._add()
        self.assertEqual(self.svc.get_student("1").name, "Ana Reyes")

    def test_persistence(self):
        self._add()
        reloaded = StudentService(self.path)
        self.assertEqual(len(reloaded.list_students()), 1)

    def test_duplicate_rejected(self):
        self._add()
        with self.assertRaises(DuplicateStudentError):
            self._add()

    def test_invalid_email_and_age(self):
        with self.assertRaises(ValidationError):
            self.svc.add_student("2", "B", 20, "bad-email", "X")
        with self.assertRaises(ValidationError):
            self.svc.add_student("2", "B", "abc", "b@x.com", "X")

    def test_update_ignores_blank(self):
        self._add()
        s = self.svc.update_student("1", name="New Name", age="")
        self.assertEqual((s.name, s.age), ("New Name", 20))

    def test_phone_saved_and_validated(self):
        self._add()
        self.assertEqual(self.svc.get_student("1").phone, "09171234567")
        with self.assertRaises(ValidationError):
            self.svc.add_student("2", "B", 20, "b@x.com", "X", "abc")

    def test_update_missing(self):
        with self.assertRaises(StudentNotFoundError):
            self.svc.update_student("nope", name="x")

    def test_delete(self):
        self._add()
        self.svc.delete_student("1")
        with self.assertRaises(StudentNotFoundError):
            self.svc.get_student("1")

    def test_search(self):
        self._add()
        self.assertEqual(len(self.svc.search_students("reyes")), 1)
        self.assertEqual(len(self.svc.search_students("zzz")), 0)

    def test_corrupt_file(self):
        with open(self.path, "w") as fh:
            fh.write("{not json")
        with self.assertRaises(StorageError):
            StudentService(self.path)


if __name__ == "__main__":
    unittest.main()
