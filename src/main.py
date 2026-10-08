"""Command-line entry point.  Run from the project root:

    python -m src.main
"""
import logging
import sys

from src.services.student_service import StudentService
from src.utils.config import load_config
from src.utils.exceptions import SISError
from src.utils.logger import setup_logging

logger = logging.getLogger("sis.main")

MENU = """
=== {title} ===
1. Add student
2. View students
3. Update student
4. Delete student
5. Search students
6. Exit
"""


def prompt(label: str) -> str:
    return input(f"{label}: ").strip()


def show(students) -> None:
    print("\n--- Student Records ---")
    if not students:
        print("No records found.")
        return
    for s in students:
        print(s)


def handle_add(service: StudentService) -> None:
    s = service.add_student(prompt("Student ID"), prompt("Name"),
                            prompt("Age"), prompt("Email"),
                            prompt("Course"), prompt("Phone"))
    print(f"Added: {s}")


def handle_update(service: StudentService) -> None:
    sid = prompt("Student ID to update")
    print("Leave a field blank to keep its current value.")
    s = service.update_student(sid, name=prompt("New name"),
                               age=prompt("New age"),
                               email=prompt("New email"),
                               course=prompt("New course"),
                               phone=prompt("New phone"))
    print(f"Updated: {s}")


def handle_delete(service: StudentService) -> None:
    sid = prompt("Student ID to delete")
    if prompt(f"Really delete {sid}? (y/N)").lower() == "y":
        service.delete_student(sid)
        print("Deleted.")
    else:
        print("Cancelled.")


def run() -> int:
    config = load_config()
    setup_logging(config["log_file"], config["log_level"])
    try:
        service = StudentService(config["data_file"])
    except SISError as exc:
        print(f"Startup error: {exc}")
        return 1

    actions = {
        "1": handle_add,
        "2": lambda svc: show(svc.list_students()),
        "3": handle_update,
        "4": handle_delete,
        "5": lambda svc: show(svc.search_students(prompt("Keyword"))),
    }

    logger.info("Application started.")
    while True:
        print(MENU.format(title=config["app_name"]))
        choice = prompt("Choose an option")
        if choice == "6":
            logger.info("Application exited.")
            print("Goodbye!")
            return 0
        action = actions.get(choice)
        if action is None:
            print("Invalid option, try again.")
            continue
        try:
            action(service)
        except SISError as exc:          # expected, user-facing errors
            logger.warning("Operation failed: %s", exc)
            print(f"Error: {exc}")
        except (KeyboardInterrupt, EOFError):
            print("\nGoodbye!")
            return 0
        except Exception:                # unexpected: log full traceback
            logger.exception("Unexpected error")
            print("An unexpected error occurred. See the log for details.")


if __name__ == "__main__":
    sys.exit(run())
