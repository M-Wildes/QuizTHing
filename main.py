import json
import os
import hashlib
from typing import Dict, Any, List, Optional

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget,
    QStackedWidget, QVBoxLayout, QHBoxLayout, QGridLayout,
    QLabel, QLineEdit, QPushButton, QRadioButton, QButtonGroup,
    QMessageBox, QProgressBar, QSizePolicy, QFrame
)

USERS_FILE = "users.json"
QUESTIONS_FILE = "questions.json"


# ----------------------------
# THEME (edit these colours)
# ----------------------------
THEME = {
    # Typography
    "font_size": "12px",
    "title_size": "22px",
    "tile_title_size": "16px",
    "radius": "10px",
    "tile_radius": "14px",

    # Core colors
    "window_bg": "#0F1115",
    "text": "#E9EDF1",
    "muted_text": "#A7B0BA",
    "border": "#2A2F38",

    # Inputs
    "input_bg": "#151923",

    # Buttons
    "button_bg": "#1A1F2A",
    "button_text": "#E9EDF1",
    "button_hover_bg": "#202738",
    "button_pressed_bg": "#151B27",

    # Accent (primary action)
    "accent": "#4C8DFF",
    "accent_hover": "#3B7CFF",
    "accent_text": "#0B1020",

    # Danger
    "danger": "#FF4D4D",
    "danger_hover": "#FF3A3A",
    "danger_text": "#140A0A",

    # Tiles
    "tile_bg": "#141925",
    "tile_border": "#2A2F38",

    # Progress
    "progress_bg": "#141925",
}

THEME_LIGHT = {
    "font_size": "12px",
    "title_size": "22px",
    "tile_title_size": "16px",
    "radius": "10px",
    "tile_radius": "14px",

    "window_bg": "#F6F7F9",
    "text": "#111318",
    "muted_text": "#5B6470",
    "border": "#D5DAE2",

    "input_bg": "#FFFFFF",

    "button_bg": "#FFFFFF",
    "button_text": "#111318",
    "button_hover_bg": "#EEF1F6",
    "button_pressed_bg": "#E6EAF1",

    "accent": "#2563EB",
    "accent_hover": "#1D4ED8",
    "accent_text": "#FFFFFF",

    "danger": "#DC2626",
    "danger_hover": "#B91C1C",
    "danger_text": "#FFFFFF",

    "tile_bg": "#FFFFFF",
    "tile_border": "#D5DAE2",

    "progress_bg": "#FFFFFF",
}


def app_stylesheet(theme: dict) -> str:
    def T(key: str) -> str:
        if key not in theme:
            raise KeyError(f"Missing theme key: {key}")
        return theme[key]

    return f"""
    /* ========== GLOBAL ========== */
    QMainWindow {{
        background: {T("window_bg")};
    }}

    QWidget {{
        color: {T("text")};
        font-size: {T("font_size")};
    }}

    QLabel#Title {{
        font-size: {T("title_size")};
        font-weight: 700;
        color: {T("text")};
    }}

    QLabel#Subtitle, QLabel#Muted {{
        color: {T("muted_text")};
    }}

    /* ========== INPUTS ========== */
    QLineEdit {{
        background: {T("input_bg")};
        color: {T("text")};
        border: 1px solid {T("border")};
        border-radius: {T("radius")};
        padding: 10px 12px;
        selection-background-color: {T("accent")};
        selection-color: {T("accent_text")};
    }}

    QLineEdit:focus {{
        border: 1px solid {T("accent")};
    }}

    /* ========== BUTTONS ========== */
    QPushButton {{
        background: {T("button_bg")};
        color: {T("button_text")};
        border: 1px solid {T("border")};
        border-radius: {T("radius")};
        padding: 10px 14px;
    }}

    QPushButton:hover {{
        background: {T("button_hover_bg")};
    }}

    QPushButton:pressed {{
        background: {T("button_pressed_bg")};
    }}

    QPushButton#Primary {{
        background: {T("accent")};
        color: {T("accent_text")};
        border: 1px solid {T("accent")};
        font-weight: 600;
    }}

    QPushButton#Primary:hover {{
        background: {T("accent_hover")};
        border: 1px solid {T("accent_hover")};
    }}

    QPushButton#Danger {{
        background: {T("danger")};
        color: {T("danger_text")};
        border: 1px solid {T("danger")};
        font-weight: 600;
    }}

    QPushButton#Danger:hover {{
        background: {T("danger_hover")};
        border: 1px solid {T("danger_hover")};
    }}

    /* ========== “TILE” CARDS ========== */
    QFrame#Tile {{
        background: {T("tile_bg")};
        border: 1px solid {T("tile_border")};
        border-radius: {T("tile_radius")};
    }}

    QLabel#TileTitle {{
        font-size: {T("tile_title_size")};
        font-weight: 700;
        color: {T("text")};
    }}

    QLabel#TileSub {{
        color: {T("muted_text")};
    }}

    /* ========== RADIO BUTTONS ========== */
    QRadioButton {{
        spacing: 10px;
        padding: 6px 4px;
        color: {T("text")};
    }}

    /* ========== PROGRESS BAR ========== */
    QProgressBar {{
        background: {T("progress_bg")};
        border: 1px solid {T("border")};
        border-radius: 6px;
        height: 12px;
        text-align: center;
        color: {T("muted_text")};
    }}

    QProgressBar::chunk {{
        background: {T("accent")};
        border-radius: 6px;
    }}
    """


# ----------------------------
# Data helpers
# ----------------------------
def sha256(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def load_json(path: str, default):
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return default


def save_json(path: str, data) -> None:
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)


def ensure_questions_file() -> None:
    if not os.path.exists(QUESTIONS_FILE):
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
            },
        )


def normalize_users(users: Dict[str, Any]) -> Dict[str, Any]:
    """
    Supports old format: {"alice": "hash"}
    New format: {"alice": {"pw_hash": "...", "scores": {...}}}
    """
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


SUBJECT_ICONS = {
    "Math": "➗",
    "Science": "🧪",
    "History": "🏛️",
    "English": "📚",
    "Geography": "🗺️",
}


# ----------------------------
# UI Pages
# ----------------------------
class LoginPage(QWidget):
    def __init__(self, app: "MainWindow"):
        super().__init__()
        self.app = app

        root = QVBoxLayout(self)
        root.setSpacing(12)

        title = QLabel("Quiz Game")
        title.setObjectName("Title")

        subtitle = QLabel("Log in or create an account to save your best scores.")
        subtitle.setObjectName("Subtitle")
        subtitle.setWordWrap(True)

        root.addWidget(title)
        root.addWidget(subtitle)

        mode_row = QHBoxLayout()
        self.rb_login = QRadioButton("Login")
        self.rb_create = QRadioButton("Create account")
        self.rb_login.setChecked(True)
        mode_row.addWidget(self.rb_login)
        mode_row.addWidget(self.rb_create)
        mode_row.addStretch(1)
        root.addLayout(mode_row)

        self.user = QLineEdit()
        self.user.setPlaceholderText("Username")

        self.pw = QLineEdit()
        self.pw.setPlaceholderText("Password")
        self.pw.setEchoMode(QLineEdit.Password)

        root.addWidget(self.user)
        root.addWidget(self.pw)

        self.status = QLabel("")
        self.status.setObjectName("Muted")
        self.status.setWordWrap(True)
        root.addWidget(self.status)

        btn_row = QHBoxLayout()
        self.btn_go = QPushButton("Continue")
        self.btn_go.setObjectName("Primary")
        self.btn_go.clicked.connect(self.submit)
        btn_row.addWidget(self.btn_go)
        btn_row.addStretch(1)
        root.addLayout(btn_row)

        root.addStretch(1)

    def set_status(self, msg: str):
        self.status.setText(msg)

    def submit(self):
        u = self.user.text().strip()
        p = self.pw.text()

        if not u or not p:
            self.set_status("Enter a username and password.")
            return

        hp = sha256(p)

        if self.rb_create.isChecked():
            if u in self.app.users:
                self.set_status("That username already exists.")
                return

            self.app.users[u] = {"pw_hash": hp, "scores": {}}
            self.app.save_users()
            self.set_status("Account created. Now log in.")
            self.rb_login.setChecked(True)
            self.pw.clear()
            self.user.setFocus()
            return

        rec = self.app.users.get(u)
        if not isinstance(rec, dict) or rec.get("pw_hash") != hp:
            self.set_status("Wrong username or password.")
            return

        self.set_status("")
        self.pw.clear()
        self.app.current_user = u
        self.app.show_hub()


class HubPage(QWidget):
    def __init__(self, app: "MainWindow"):
        super().__init__()
        self.app = app

        root = QVBoxLayout(self)
        root.setSpacing(12)

        top = QHBoxLayout()
        title = QLabel("Choose a subject")
        title.setObjectName("Title")
        title.setStyleSheet("font-size: 18px;")  # safe: size only, colour comes from stylesheet
        top.addWidget(title)
        top.addStretch(1)

        self.btn_logout = QPushButton("Logout")
        self.btn_logout.setObjectName("Danger")
        self.btn_logout.clicked.connect(self.app.logout)
        top.addWidget(self.btn_logout)
        root.addLayout(top)

        self.lbl_user = QLabel("")
        self.lbl_user.setObjectName("Muted")
        root.addWidget(self.lbl_user)

        self.grid = QGridLayout()
        self.grid.setHorizontalSpacing(12)
        self.grid.setVerticalSpacing(12)
        root.addLayout(self.grid)

        footer = QLabel(f"Edit questions in: {QUESTIONS_FILE}")
        footer.setObjectName("Muted")
        root.addWidget(footer)

        root.addStretch(1)

    def refresh(self):
        while self.grid.count():
            item = self.grid.takeAt(0)
            w = item.widget()
            if w:
                w.deleteLater()

        self.lbl_user.setText(f"Signed in as: {self.app.current_user}")

        subjects = list(self.app.qbank.keys())
        if not subjects:
            self.grid.addWidget(self._info_tile("No subjects found", f"Add some to {QUESTIONS_FILE}."), 0, 0)
            return

        scores = self.app.users.get(self.app.current_user, {}).get("scores", {})

        cols = 3
        r = c = 0
        for subject in subjects:
            icon = SUBJECT_ICONS.get(subject, "📝")
            best = scores.get(subject, 0)
            tile = self._subject_tile(subject, f"{icon}  {subject}", f"Best score: {best}")
            self.grid.addWidget(tile, r, c)

            c += 1
            if c >= cols:
                c = 0
                r += 1

    def _info_tile(self, title: str, body: str) -> QWidget:
        frame = QFrame()
        frame.setObjectName("Tile")
        lay = QVBoxLayout(frame)
        lay.setSpacing(6)

        t = QLabel(title)
        t.setObjectName("TileTitle")

        b = QLabel(body)
        b.setObjectName("TileSub")
        b.setWordWrap(True)

        lay.addWidget(t)
        lay.addWidget(b)
        return frame

    def _subject_tile(self, subject: str, title: str, subtitle: str) -> QWidget:
        frame = QFrame()
        frame.setObjectName("Tile")
        frame.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        lay = QVBoxLayout(frame)
        lay.setSpacing(8)

        lbl1 = QLabel(title)
        lbl1.setObjectName("TileTitle")

        lbl2 = QLabel(subtitle)
        lbl2.setObjectName("TileSub")

        btn = QPushButton("Start Quiz")
        btn.setObjectName("Primary")
        btn.clicked.connect(lambda: self.app.start_quiz(subject))

        lay.addWidget(lbl1)
        lay.addWidget(lbl2)
        lay.addStretch(1)
        lay.addWidget(btn)

        return frame


class QuizPage(QWidget):
    def __init__(self, app: "MainWindow"):
        super().__init__()
        self.app = app

        self.subject: str = ""
        self.questions: List[Dict[str, Any]] = []
        self.index: int = 0
        self.score: int = 0

        root = QVBoxLayout(self)
        root.setSpacing(12)

        top = QHBoxLayout()

        self.btn_back = QPushButton("← Subjects")
        self.btn_back.clicked.connect(self.app.show_hub)
        top.addWidget(self.btn_back)

        top.addStretch(1)

        self.lbl_title = QLabel("")
        self.lbl_title.setObjectName("TileTitle")
        top.addWidget(self.lbl_title)

        root.addLayout(top)

        self.progress = QProgressBar()
        root.addWidget(self.progress)

        self.lbl_q = QLabel("")
        self.lbl_q.setWordWrap(True)
        self.lbl_q.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        self.lbl_q.setStyleSheet("font-size: 14px;")  # size only
        root.addWidget(self.lbl_q)

        self.choice_group = QButtonGroup(self)
        self.choice_group.setExclusive(True)

        self.choices_box = QVBoxLayout()
        self.choices_box.setSpacing(4)
        root.addLayout(self.choices_box)

        bottom = QHBoxLayout()

        self.btn_submit = QPushButton("Submit")
        self.btn_submit.setObjectName("Primary")
        self.btn_submit.clicked.connect(self.submit)
        bottom.addWidget(self.btn_submit)

        bottom.addStretch(1)

        self.lbl_feedback = QLabel("")
        self.lbl_feedback.setObjectName("Muted")
        bottom.addWidget(self.lbl_feedback)

        root.addLayout(bottom)
        root.addStretch(1)

    def load_subject(self, subject: str, questions: List[Dict[str, Any]]):
        self.subject = subject
        self.questions = questions
        self.index = 0
        self.score = 0
        self.lbl_feedback.setText("")
        self.render()

    def _clear_choices(self):
        # Remove old radio buttons cleanly
        while self.choices_box.count():
            item = self.choices_box.takeAt(0)
            w = item.widget()
            if w:
                self.choice_group.removeButton(w)
                w.deleteLater()

    def render(self):
        total = len(self.questions)
        self.lbl_title.setText(f"{self.subject} ({self.index + 1}/{total})")
        self.progress.setMaximum(total)
        self.progress.setValue(self.index)

        q = self.questions[self.index]
        self.lbl_q.setText(q["q"])
        self.lbl_feedback.setText("")

        self._clear_choices()

        for i, text in enumerate(q["choices"]):
            rb = QRadioButton(text)
            self.choice_group.addButton(rb, i)
            self.choices_box.addWidget(rb)

    def submit(self):
        selected_id = self.choice_group.checkedId()
        if selected_id == -1:
            self.lbl_feedback.setText("Pick an answer.")
            return

        q = self.questions[self.index]
        correct = int(q["answer"])

        if selected_id == correct:
            self.score += 1
            self.lbl_feedback.setText("Correct ✅")
        else:
            self.lbl_feedback.setText(f"Wrong. Correct: {q['choices'][correct]}")

        self.index += 1
        if self.index >= len(self.questions):
            self.finish()
        else:
            self.render()

    def finish(self):
        total = len(self.questions)
        subject = self.subject

        user = self.app.users.setdefault(self.app.current_user, {"pw_hash": "", "scores": {}})
        scores = user.setdefault("scores", {})
        best = scores.get(subject, 0)

        if self.score > best:
            scores[subject] = self.score
            self.app.save_users()

        QMessageBox.information(
            self,
            "Finished",
            f"Score: {self.score}/{total}\nBest: {scores.get(subject, self.score)}"
        )
        self.app.show_hub()


# ----------------------------
# Main Window
# ----------------------------
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        ensure_questions_file()

        self.users: Dict[str, Any] = normalize_users(load_json(USERS_FILE, {}))
        save_json(USERS_FILE, self.users)

        self.qbank: Dict[str, Any] = load_json(QUESTIONS_FILE, {})
        self.current_user: Optional[str] = None

        self.setWindowTitle("Quiz Game")
        self.setMinimumSize(860, 540)

        self.stack = QStackedWidget()
        self.setCentralWidget(self.stack)

        self.login_page = LoginPage(self)
        self.hub_page = HubPage(self)
        self.quiz_page = QuizPage(self)

        self.stack.addWidget(self.login_page)  # 0
        self.stack.addWidget(self.hub_page)    # 1
        self.stack.addWidget(self.quiz_page)   # 2

        self.show_login()

    def save_users(self):
        save_json(USERS_FILE, self.users)

    def show_login(self):
        self.current_user = None
        self.stack.setCurrentIndex(0)

    def show_hub(self):
        self.hub_page.refresh()
        self.stack.setCurrentIndex(1)

    def start_quiz(self, subject: str):
        questions = self.qbank.get(subject, [])
        if not questions:
            QMessageBox.warning(self, "No questions", f"No questions for '{subject}'. Add them in {QUESTIONS_FILE}.")
            return
        self.quiz_page.load_subject(subject, questions)
        self.stack.setCurrentIndex(2)

    def logout(self):
        self.show_login()


def main():
    app = QApplication([])

    # Pick one:
    app.setStyleSheet(app_stylesheet(THEME))
    # app.setStyleSheet(app_stylesheet(THEME_LIGHT))

    win = MainWindow()
    win.show()
    app.exec()


if __name__ == "__main__":
    main()