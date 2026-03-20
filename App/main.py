import json
import os
import hashlib
from enum import Enum
from typing import Dict, Any, List, Optional

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget,
    QStackedWidget, QVBoxLayout, QHBoxLayout, QGridLayout, QFormLayout,
    QLabel, QLineEdit, QPushButton, QRadioButton, QButtonGroup,
    QMessageBox, QProgressBar, QSizePolicy, QFrame, QInputDialog
)

USERS_FILE = "users.json"
QUESTIONS_FILE = "questions.json"
SETTINGS_FILE = "settings.json"
LEADERBOARDS_FILE = "leaderboards.json"

DEFAULT_SETTINGS = {
    "theme": "dark",          # "dark" or "light"
    "window_width": 1100,
    "window_height": 680,
}

SUBJECT_ICONS = {
    "Math": "➗",
    "Science": "🧪",
    "History": "🏛️",
    "English": "📚",
    "Geography": "🗺️",
}

# ----------------------------
# THEME (edit these colours)
# ----------------------------
THEME = {
    "font_size": "12px",
    "title_size": "22px",
    "tile_title_size": "16px",
    "radius": "10px",
    "tile_radius": "14px",

    "window_bg": "#0F1115",
    "sidebar_bg": "#0B0D12",
    "text": "#E9EDF1",
    "muted_text": "#A7B0BA",
    "border": "#2A2F38",

    "input_bg": "#151923",

    "button_bg": "#1A1F2A",
    "button_text": "#E9EDF1",
    "button_hover_bg": "#202738",
    "button_pressed_bg": "#151B27",

    "accent": "#8CB6FF",
    "accent_hover": "#3B7CFF",
    "accent_text": "#0B1020",

    "danger": "#FF4D4D",
    "danger_hover": "#FF3A3A",
    "danger_text": "#140A0A",

    "tile_bg": "#141925",
    "tile_border": "#2A2F38",

    "progress_bg": "#141925",

    # sidebar overrides
    "sidebar_text": "#E9EDF1",
    "sidebar_muted_text": "#A7B0BA",
}

THEME_LIGHT = {
    "font_size": "12px",
    "title_size": "22px",
    "tile_title_size": "16px",
    "radius": "10px",
    "tile_radius": "14px",

    "window_bg": "#F4F6FB",
    "sidebar_bg": "#3A4461",
    "text": "#1E2126",
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

    "sidebar_text": "#F3F6FB",
    "sidebar_muted_text": "#CBD5E1",
}


def app_stylesheet(theme: dict) -> str:
    def T(key: str) -> str:
        if key not in theme:
            raise KeyError(f"Missing theme key: {key}")
        return theme[key]

    return f"""
    QMainWindow {{
        background: {T("window_bg")};
    }}

    * {{
        font-size: {T("font_size")};
    }}

    QLabel, QRadioButton {{
        color: {T("text")};
    }}

    QFrame#Sidebar {{
        background: {T("sidebar_bg")};
        border-right: 1px solid {T("border")};
    }}

    QFrame#Sidebar QWidget {{
        color: {T("sidebar_text")};
    }}

    QLabel#Title {{
        font-size: {T("title_size")};
        font-weight: 700;
        color: {T("text")};
    }}

    QLabel#Subtitle, QLabel#Muted {{
        color: {T("muted_text")};
    }}

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

    QRadioButton {{
        spacing: 10px;
        padding: 6px 4px;
    }}

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


def load_settings() -> dict:
    s = load_json(SETTINGS_FILE, DEFAULT_SETTINGS.copy())
    for k, v in DEFAULT_SETTINGS.items():
        s.setdefault(k, v)
    return s


def save_settings(s: dict) -> None:
    save_json(SETTINGS_FILE, s)


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
                "History": [
                    {"q": "The Roman Empire was centered around which city?", "choices": ["Athens", "Rome", "Paris", "Cairo"], "answer": 1},
                ],
            },
        )


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


# ----------------------------
# NAV TEMPLATE SYSTEM
# ----------------------------
class PageId(str, Enum):
    LOGIN = "login"
    HUB = "hub"
    PROFILE = "profile"
    SETTINGS = "settings"
    QUIZ = "quiz"
    LEADERBOARDS = "leaderboards"
    QUESTIONS = "questions"  # new page for managing questions


class BasePage(QWidget):
    """
    Template page:
      - optional back button
      - title
      - body layout you add widgets into
      - on_show() hook called when navigated to
    """
    def __init__(self, app: "MainWindow", title: str, back_to: Optional[PageId] = None):
        super().__init__()
        self.app = app
        self.back_to = back_to

        root = QVBoxLayout(self)
        root.setContentsMargins(24, 20, 24, 20)
        root.setSpacing(14)

        header = QHBoxLayout()
        header.setSpacing(10)

        if back_to is not None:
            back = QPushButton("← Back")
            back.clicked.connect(lambda: self.app.go(back_to))
            header.addWidget(back)
        else:
            header.addSpacing(1)

        header.addStretch(1)

        self.title = QLabel(title)
        self.title.setObjectName("Title")
        header.addWidget(self.title)

        header.addStretch(1)
        root.addLayout(header)

        self.body = QVBoxLayout()
        self.body.setSpacing(12)
        root.addLayout(self.body)

        root.addStretch(1)

    def on_show(self) -> None:
        pass


# ----------------------------
# Pages
# ----------------------------

class LoginPage(BasePage):
    def __init__(self, app: "MainWindow"):
        super().__init__(app, title="Quiz Game", back_to=None)

        subtitle = QLabel("Log in or create an account to save scores.")
        subtitle.setObjectName("Subtitle")
        subtitle.setWordWrap(True)
        self.body.addWidget(subtitle)

        mode_row = QHBoxLayout()
        self.rb_login = QRadioButton("Login")
        self.rb_create = QRadioButton("Create account")
        self.rb_login.setChecked(True)
        mode_row.addWidget(self.rb_login)
        mode_row.addWidget(self.rb_create)
        mode_row.addStretch(1)
        self.body.addLayout(mode_row)

        self.user = QLineEdit()
        self.user.setPlaceholderText("Username")
        self.pw = QLineEdit()
        self.pw.setPlaceholderText("Password")
        self.pw.setEchoMode(QLineEdit.Password)

        self.body.addWidget(self.user)
        self.body.addWidget(self.pw)

        self.status = QLabel("")
        self.status.setObjectName("Muted")
        self.status.setWordWrap(True)
        self.body.addWidget(self.status)

        btn_row = QHBoxLayout()
        self.btn_go = QPushButton("Continue")
        self.btn_go.setObjectName("Primary")
        self.btn_go.clicked.connect(self.submit)
        btn_row.addWidget(self.btn_go)
        btn_row.addStretch(1)
        self.body.addLayout(btn_row)

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
        self.app.go(PageId.HUB)

    def on_show(self) -> None:
        # reset state when returning to login
        self.user.clear()
        self.pw.clear()
        self.status.clear()
        self.rb_login.setChecked(True)
        self.user.setFocus()


class HubPage(QWidget):
    def __init__(self, app: "MainWindow"):
        super().__init__()
        self.app = app

        root = QHBoxLayout(self)
        root.setSpacing(0)
        root.setContentsMargins(0, 0, 0, 0)

        # Sidebar
        sidebar = QFrame()
        sidebar.setObjectName("Sidebar")
        sidebar.setFixedWidth(240)
        side = QVBoxLayout(sidebar)
        side.setContentsMargins(18, 18, 18, 18)
        side.setSpacing(12)

        btn_profile = QPushButton("👤  Profile")
        btn_profile.setObjectName("Primary")
        btn_profile.clicked.connect(lambda: self.app.go(PageId.PROFILE))

        btn_settings = QPushButton("⚙️  Settings")
        btn_settings.clicked.connect(lambda: self.app.go(PageId.SETTINGS))

        btn_leaderboards = QPushButton("ℹ️  Leaderboards")
        btn_leaderboards.clicked.connect(lambda: self.app.go(PageId.LEADERBOARDS))
        
        btn_questions = QPushButton("📝 Manage Questions")
        btn_questions.clicked.connect(lambda: self.app.go(PageId.QUESTIONS))

        logout_btn = QPushButton("Logout")
        logout_btn.setObjectName("Danger")
        logout_btn.clicked.connect(self.app.logout)

        side.addWidget(btn_profile)
        side.addWidget(btn_settings)
        side.addWidget(btn_leaderboards)
        side.addWidget(btn_questions)
        side.addStretch(1)
        side.addWidget(logout_btn)

        root.addWidget(sidebar)

        # Main area
        right = QWidget()
        right_layout = QVBoxLayout(right)
        right_layout.setContentsMargins(24, 20, 24, 20)
        right_layout.setSpacing(16)

        top = QHBoxLayout()
        title = QLabel("Subjects")
        title.setObjectName("Title")
        self.user_label = QLabel("")
        self.user_label.setObjectName("Muted")
        top.addWidget(title)
        top.addStretch(1)
        top.addWidget(self.user_label)
        right_layout.addLayout(top)

        self.grid = QGridLayout()
        self.grid.setSpacing(18)
        right_layout.addLayout(self.grid)
        right_layout.addStretch(1)

        root.addWidget(right)

    def on_show(self) -> None:
        self.refresh()

    def refresh(self):
        while self.grid.count():
            item = self.grid.takeAt(0)
            w = item.widget()
            if w:
                w.deleteLater()

        self.user_label.setText(f"Signed in as: {self.app.current_user}")

        subjects = list(self.app.qbank.keys())
        scores = self.app.users.get(self.app.current_user, {}).get("scores", {})

        cols = 3
        r = c = 0
        for subject in subjects:
            icon = SUBJECT_ICONS.get(subject, "📘")
            best = scores.get(subject, 0)
            tile = self.subject_tile(subject, icon, best)
            self.grid.addWidget(tile, r, c)

            c += 1
            if c >= cols:
                c = 0
                r += 1

    def subject_tile(self, subject: str, icon: str, best: int) -> QWidget:
        frame = QFrame()
        frame.setObjectName("Tile")
        frame.setMinimumHeight(140)
        frame.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        lay = QVBoxLayout(frame)
        lay.setSpacing(6)

        t = QLabel(f"{icon}  {subject}")
        t.setObjectName("TileTitle")

        s = QLabel(f"Best score: {best}")
        s.setObjectName("TileSub")

        btn = QPushButton("Start Quiz")
        btn.setObjectName("Primary")
        btn.clicked.connect(lambda _, sub=subject: self.app.start_quiz(sub))

        lay.addWidget(t)
        lay.addWidget(s)
        lay.addStretch(1)
        lay.addWidget(btn)

        return frame


class ProfilePage(BasePage):
    def __init__(self, app: "MainWindow"):
        super().__init__(app, title="Profile", back_to=PageId.HUB)

        # User header card
        header_card = QFrame()
        header_card.setObjectName("Tile")
        header_lay = QVBoxLayout(header_card)
        header_lay.setContentsMargins(20, 16, 20, 16)
        header_lay.setSpacing(8)

        self.user_lbl = QLabel("")
        self.user_lbl.setObjectName("TileTitle")
        header_lay.addWidget(self.user_lbl)

        info = QLabel("Your quiz scores and statistics")
        info.setObjectName("TileSub")
        header_lay.addWidget(info)

        self.body.addWidget(header_card)

        # Scores section
        scores_label = QLabel("Score History")
        scores_label.setObjectName("Title")
        self.body.addWidget(scores_label)

        self.scores_box = QVBoxLayout()
        self.scores_box.setSpacing(10)
        self.body.addLayout(self.scores_box)

        # Account management buttons
        self.delete_btn = QPushButton("Delete Account")
        self.delete_btn.setObjectName("Danger")
        self.delete_btn.clicked.connect(self.delete_account)
        self.reset_pw_btn = QPushButton("Reset Password")
        self.reset_pw_btn.clicked.connect(self.reset_password)

        self.body.addWidget(self.delete_btn)
        self.body.addWidget(self.reset_pw_btn)

    def on_show(self) -> None:
        self.refresh()

    def refresh(self):
        self.user_lbl.setText(f"👤 {self.app.current_user}")

        while self.scores_box.count():
            item = self.scores_box.takeAt(0)
            w = item.widget()
            if w:
                w.deleteLater()

        user = self.app.users.get(self.app.current_user, {})
        scores = user.get("scores", {})

        if not scores:
            msg = QLabel("No scores yet. Go do a quiz!")
            msg.setObjectName("Muted")
            self.scores_box.addWidget(msg)
            return

        for subject, best in sorted(scores.items(), key=lambda x: (-x[1], x[0])):
            row = QFrame()
            row.setObjectName("Tile")
            lay = QHBoxLayout(row)
            lay.setContentsMargins(16, 12, 16, 12)
            lay.setSpacing(14)

            icon = SUBJECT_ICONS.get(subject, "📘")
            left = QLabel(f"{icon}  {subject}")
            left.setObjectName("TileTitle")

            right = QLabel(f"{best}")
            right.setObjectName("TileTitle")
            right.setStyleSheet("color: #8CB6FF;")

            lay.addWidget(left)
            lay.addStretch(1)
            lay.addWidget(right)

            self.scores_box.addWidget(row)

    def delete_account(self):
        reply = QMessageBox.question(self, "Confirm", "Are you sure you want to delete your account?",
                                     QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            if self.app.current_user in self.app.users:
                del self.app.users[self.app.current_user]
                self.app.save_users()
                QMessageBox.information(self, "Deleted", "Account deleted.")
                self.app.current_user = None
                self.app.go(PageId.LOGIN)

    def reset_password(self):
        pw, ok = QInputDialog.getText(self, "Reset Password", "Enter new password:", echo=QLineEdit.Password)
        if ok and pw:
            hp = sha256(pw)
            user_data = self.app.users.get(self.app.current_user)
            if user_data:
                user_data["pw_hash"] = hp
                self.app.save_users()
                QMessageBox.information(self, "Reset", "Password reset successfully.")


class SettingsPage(BasePage):
    def __init__(self, app: "MainWindow"):
        super().__init__(app, title="Settings", back_to=PageId.HUB)

        # Theme tile
        theme_tile = QFrame()
        theme_tile.setObjectName("Tile")
        theme_l = QHBoxLayout(theme_tile)
        theme_l.setContentsMargins(14, 10, 14, 10)

        theme_label = QLabel("Theme")
        theme_label.setObjectName("TileTitle")

        self.btn_theme = QPushButton("")
        self.btn_theme.clicked.connect(self.toggle_theme)

        theme_l.addWidget(theme_label)
        theme_l.addStretch(1)
        theme_l.addWidget(self.btn_theme)
        self.body.addWidget(theme_tile)

        # Size tile
        size_tile = QFrame()
        size_tile.setObjectName("Tile")
        size_l = QVBoxLayout(size_tile)
        size_l.setContentsMargins(14, 10, 14, 10)
        size_l.setSpacing(10)

        size_label = QLabel("Window size")
        size_label.setObjectName("TileTitle")
        size_l.addWidget(size_label)

        row = QHBoxLayout()
        b1 = QPushButton("Small (900×600)")
        b1.clicked.connect(lambda: self.apply_size(900, 600))
        b2 = QPushButton("Medium (1100×680)")
        b2.clicked.connect(lambda: self.apply_size(1100, 680))
        b3 = QPushButton("Large (1300×820)")
        b3.clicked.connect(lambda: self.apply_size(1300, 820))

        row.addWidget(b1)
        row.addWidget(b2)
        row.addWidget(b3)
        size_l.addLayout(row)

        self.body.addWidget(size_tile)

        # Manage questions button
        self.questions_btn = QPushButton("Manage Questions")
        self.questions_btn.clicked.connect(lambda: self.app.go(PageId.QUESTIONS))
        self.body.addWidget(self.questions_btn)

    def on_show(self) -> None:
        self.refresh()

    def refresh(self):
        t = self.app.settings.get("theme", "dark")
        self.btn_theme.setText("Dark" if t == "dark" else "Light")

    def toggle_theme(self):
        self.app.settings["theme"] = "light" if self.app.settings.get("theme") == "dark" else "dark"
        save_settings(self.app.settings)
        self.app.apply_theme()
        self.refresh()

    def apply_size(self, w: int, h: int):
        self.app.settings["window_width"] = w
        self.app.settings["window_height"] = h
        save_settings(self.app.settings)
        self.app.resize(w, h)


class QuestionsPage(BasePage):
    def __init__(self, app: "MainWindow"):
        super().__init__(app, title="Manage Questions", back_to=PageId.SETTINGS)

        self.subject_input = QLineEdit()
        self.q_text_input = QLineEdit()
        self.choices_inputs = [QLineEdit() for _ in range(4)]
        self.answer_input = QLineEdit()

        form = QFormLayout()
        form.addRow("Subject:", self.subject_input)
        form.addRow("Question:", self.q_text_input)
        for i, choice in enumerate(self.choices_inputs):
            form.addRow(f"Choice {i+1}:", choice)
        form.addRow("Correct answer (0-3):", self.answer_input)

        self.body.addLayout(form)

        btn_save = QPushButton("Save Question")
        btn_save.clicked.connect(self.save_question)
        self.body.addWidget(btn_save)

        # Load existing questions
        self.load_question()

    def load_question(self):
        # For now, just clear inputs
        self.subject_input.clear()
        self.q_text_input.clear()
        for c in self.choices_inputs:
            c.clear()
        self.answer_input.clear()

    def save_question(self):
        subject = self.subject_input.text().strip()
        question_text = self.q_text_input.text().strip()
        choices = [c.text().strip() for c in self.choices_inputs]
        try:
            answer_idx = int(self.answer_input.text())
        except:
            QMessageBox.warning(self, "Error", "Answer must be an integer 0-3.")
            return
        if not (0 <= answer_idx < 4):
            QMessageBox.warning(self, "Error", "Answer must be between 0 and 3.")
            return
        if not subject or not question_text or any(not c for c in choices):
            QMessageBox.warning(self, "Error", "Fill all fields.")
            return

        # Add question
        questions = self.app.qbank.setdefault(subject, [])
        questions.append({
            "q": question_text,
            "choices": choices,
            "answer": answer_idx
        })
        save_json(QUESTIONS_FILE, self.app.qbank)
        QMessageBox.information(self, "Saved", "Question saved!")
        self.load_question()


class QuizPage(BasePage):
    def __init__(self, app: "MainWindow"):
        super().__init__(app, title="Quiz", back_to=PageId.HUB)

        self.subject: str = ""
        self.questions: List[Dict[str, Any]] = []
        self.index: int = 0
        self.score: int = 0

        self.header_row = QHBoxLayout()
        self.lbl_title = QLabel("")
        self.lbl_title.setObjectName("TileTitle")
        self.header_row.addWidget(self.lbl_title)
        self.header_row.addStretch(1)
        self.body.addLayout(self.header_row)

        self.progress = QProgressBar()
        self.body.addWidget(self.progress)

        self.lbl_q = QLabel("")
        self.lbl_q.setWordWrap(True)
        self.lbl_q.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        self.lbl_q.setStyleSheet("font-size: 14px;")
        self.body.addWidget(self.lbl_q)

        self.choice_group = QButtonGroup(self)
        self.choice_group.setExclusive(True)

        self.choices_box = QVBoxLayout()
        self.choices_box.setSpacing(4)
        self.body.addLayout(self.choices_box)

        bottom = QHBoxLayout()
        self.btn_submit = QPushButton("Submit")
        self.btn_submit.setObjectName("Primary")
        self.btn_submit.clicked.connect(self.submit)
        bottom.addWidget(self.btn_submit)
        bottom.addStretch(1)
        self.lbl_feedback = QLabel("")
        self.lbl_feedback.setObjectName("Muted")
        bottom.addWidget(self.lbl_feedback)
        self.body.addLayout(bottom)

    def load_subject(self, subject: str, questions: List[Dict[str, Any]]):
        self.subject = subject
        self.questions = questions
        self.index = 0
        self.score = 0
        self.lbl_feedback.setText("")
        self.render()

    def _clear_choices(self):
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

        # Update leaderboards
        leaderboards = self.app.leaderboards
        subject_board = leaderboards.get(subject, [])
        # Append score with username
        subject_board.append({"user": self.app.current_user, "score": self.score})
        # Keep top 10 scores
        subject_board = sorted(subject_board, key=lambda x: -x["score"])[:10]
        leaderboards[subject] = subject_board
        self.app.leaderboards = leaderboards
        save_json(LEADERBOARDS_FILE, leaderboards)

        QMessageBox.information(self, "Finished", f"Score: {self.score}/{total}\nBest: {scores.get(subject, self.score)}")
        self.app.go(PageId.HUB)


class LeaderboardsPage(BasePage):
    def __init__(self, app: "MainWindow"):
        super().__init__(app, title="Leaderboards", back_to=PageId.HUB)
        self.leaderboard_widget = QVBoxLayout()
        self.body.addLayout(self.leaderboard_widget)

    def on_show(self):
        self.refresh()

    def refresh(self):
        while self.leaderboard_widget.count():
            item = self.leaderboard_widget.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()

        leaderboards = self.app.leaderboards
        if not leaderboards:
            msg = QLabel("No leaderboards available.")
            msg.setObjectName("Muted")
            self.leaderboard_widget.addWidget(msg)
            return

        for subject, scores in leaderboards.items():
            title_lbl = QLabel(f"{subject} Top Scores")
            title_lbl.setObjectName("TileTitle")
            self.leaderboard_widget.addWidget(title_lbl)

            for entry in scores:
                user = entry['user']
                score = entry['score']
                lbl = QLabel(f"{user}: {score}")
                self.leaderboard_widget.addWidget(lbl)



class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        ensure_questions_file()

        self.settings = load_settings()
        self.users: Dict[str, Any] = normalize_users(load_json(USERS_FILE, {}))
        save_json(USERS_FILE, self.users)

        self.qbank: Dict[str, Any] = load_json(QUESTIONS_FILE, {})
        self.current_user: Optional[str] = None

        # Load leaderboards
        self.leaderboards: dict = load_json(LEADERBOARDS_FILE, {})

        self.setWindowTitle("Quiz Game")
        self.setMinimumSize(900, 600)
        self.resize(self.settings["window_width"], self.settings["window_height"])

        self.stack = QStackedWidget()
        self.setCentralWidget(self.stack)

        # Registry-based page system
        self.pages: Dict[PageId, QWidget] = {}

        self.register_page(PageId.LOGIN, LoginPage(self))
        self.register_page(PageId.HUB, HubPage(self))
        self.register_page(PageId.PROFILE, ProfilePage(self))
        self.register_page(PageId.SETTINGS, SettingsPage(self))
        self.register_page(PageId.QUIZ, QuizPage(self))
        self.register_page(PageId.LEADERBOARDS, LeaderboardsPage(self))
        self.register_page(PageId.QUESTIONS, QuestionsPage(self))

        self.apply_theme()
        self.go(PageId.LOGIN)

    def register_page(self, page_id: PageId, widget: QWidget) -> None:
        self.pages[page_id] = widget
        self.stack.addWidget(widget)

    def go(self, page_id: PageId) -> None:
        w = self.pages.get(page_id)
        if not w:
            raise KeyError(f"Page not registered: {page_id}")

        if hasattr(w, "on_show"):
            try:
                w.on_show()
            except Exception:
                pass

        self.stack.setCurrentWidget(w)

    def apply_theme(self):
        theme_name = self.settings.get("theme", "dark")
        qapp = QApplication.instance()
        qapp.setStyleSheet(app_stylesheet(THEME_LIGHT if theme_name == "light" else THEME))

    def save_users(self):
        save_json(USERS_FILE, self.users)

    def start_quiz(self, subject: str):
        questions = self.qbank.get(subject, [])
        if not questions:
            QMessageBox.warning(self, "No questions", f"No questions for '{subject}'. Add them in {QUESTIONS_FILE}.")
            return
        quiz_page = self.pages[PageId.QUIZ]
        if isinstance(quiz_page, QuizPage):
            quiz_page.load_subject(subject, questions)
        self.go(PageId.QUIZ)

    def logout(self):
        self.current_user = None
        self.go(PageId.LOGIN)


def main():
    app = QApplication([])
    win = MainWindow()
    win.show()
    app.exec()

if __name__ == "__main__":
    main()