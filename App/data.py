import json
import os
import base64
import secrets
import hashlib
from typing import Any, Dict, List, Tuple

USERS_FILE = "users.json"
QUESTIONS_FILE = "questions.json"
SETTINGS_FILE = "settings.json"

DEFAULT_SETTINGS = {
    "theme": "dark",          # "dark" or "light"
    "window_width": 1100,
    "window_height": 680,
}


def load_json(path: str, default: Any) -> Any:
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return default


def save_json(path: str, data: Any) -> None:
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)


def ensure_questions_file() -> None:
    if os.path.exists(QUESTIONS_FILE):
        return
    save_json(
        QUESTIONS_FILE,
        {
            "Math": [
                {"q": "2 + 2 = ?", "choices": ["3", "4", "5", "22"], "answer": 1},
                {"q": "12 / 3 = ?", "choices": ["3", "4", "5", "6"], "answer": 1},
            ],
            "Science": [
                {"q": "Water freezes at what temperature (°C)?", "choices": ["0", "100", "-10", "50"], "answer": 0},
                {"q": "Which planet is known as the Red Planet?", "choices": ["Earth", "Mars", "Jupiter", "Venus"], "answer": 1},
            ],
            "History": [
                {"q": "The Roman Empire was centered around which city?", "choices": ["Athens", "Rome", "Paris", "Cairo"], "answer": 1},
            ],
        },
    )


def load_settings() -> Dict[str, Any]:
    s = load_json(SETTINGS_FILE, DEFAULT_SETTINGS.copy())
    for k, v in DEFAULT_SETTINGS.items():
        s.setdefault(k, v)
    return s


def save_settings(s: Dict[str, Any]) -> None:
    save_json(SETTINGS_FILE, s)


def normalize_users(users: Dict[str, Any]) -> Dict[str, Any]:
    fixed: Dict[str, Any] = {}
    for u, rec in (users or {}).items():
        if isinstance(rec, str):
            fixed[u] = {"pw_hash": rec, "scores": {}}
        elif isinstance(rec, dict):
            fixed[u] = {
                "pw_hash": rec.get("pw_hash", ""),
                "scores": rec.get("scores", {}) if isinstance(rec.get("scores", {}), dict) else {},
            }
    return fixed


def load_users() -> Dict[str, Any]:
    users = normalize_users(load_json(USERS_FILE, {}))
    save_json(USERS_FILE, users)
    return users


def save_users(users: Dict[str, Any]) -> None:
    save_json(USERS_FILE, users)


def load_questions() -> Dict[str, Any]:
    return load_json(QUESTIONS_FILE, {})


# Better than sha256(password) with no salt.
# Stored format: base64(salt + derived_key)
def hash_password(password: str) -> str:
    salt = secrets.token_bytes(16)
    dk = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, 200_000)
    return base64.b64encode(salt + dk).decode("utf-8")


def verify_password(password: str, stored: str) -> bool:
    try:
        raw = base64.b64decode(stored.encode("utf-8"))
        salt, dk = raw[:16], raw[16:]
        dk2 = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, 200_000)
        return dk2 == dk
    except Exception:
        return False
