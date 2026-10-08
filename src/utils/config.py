"""Configuration management.

Values come from config/config.json and can be overridden by environment
variables (12-factor style), which makes the app easy to run in containers
or cloud platforms without editing files.

Environment variables:
    SIS_DATA_FILE, SIS_LOG_FILE, SIS_LOG_LEVEL
"""
import json
import os
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_CONFIG_PATH = PROJECT_ROOT / "config" / "config.json"

DEFAULTS = {
    "data_file": "data/students.json",
    "log_file": "logs/app.log",
    "log_level": "INFO",
    "app_name": "Student Information System",
}

ENV_OVERRIDES = {
    "SIS_DATA_FILE": "data_file",
    "SIS_LOG_FILE": "log_file",
    "SIS_LOG_LEVEL": "log_level",
}


def _resolve(path_str: str) -> str:
    """Make relative paths relative to the project root."""
    p = Path(path_str)
    return str(p if p.is_absolute() else PROJECT_ROOT / p)


def load_config(path=DEFAULT_CONFIG_PATH) -> dict:
    """Load configuration: defaults < config file < environment variables."""
    config = dict(DEFAULTS)
    try:
        with open(path, "r", encoding="utf-8") as fh:
            config.update(json.load(fh))
    except FileNotFoundError:
        pass  # fall back to defaults
    except json.JSONDecodeError as exc:
        raise ValueError(f"Invalid JSON in config file {path}: {exc}") from exc

    for env_name, key in ENV_OVERRIDES.items():
        if os.environ.get(env_name):
            config[key] = os.environ[env_name]

    config["data_file"] = _resolve(config["data_file"])
    config["log_file"] = _resolve(config["log_file"])
    return config
