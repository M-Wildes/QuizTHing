from __future__ import annotations

from typing import Any, Dict, List, Optional

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget,
    QStackedWidget, QVBoxLayout, QHBoxLayout, QGridLayout,
    QLabel, QLineEdit, QPushButton, QRadioButton, QButtonGroup,
    QMessageBox, QProgressBar, QSizePolicy, QFrame
)

import data


SUBJECT_ICONS = {
    "Math": "➗",
    "Science": "🧪",
    "History": "🏛️",
    "English": "📚",
    "Geography": "🗺️",
}


THEME_DARK = {
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

    # sidebar overrides (keeps text readable)
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


def stylesheet(t: Dict[str, str]) -> str:
    def T(k: str) -> str:
        return t[k]

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

    QFrame#Sidebar QLabel#Subtitle, QFrame#Sidebar QLabel#Muted {{
        color: {T("sidebar_muted_text")};
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


class LoginPage(QWidget):
    def __init__(self, app: "MainWindow"):
        super().__init__()
        self.app = app

        root = QVBoxLayout(self)
        root.setSpacing(12)

        title = QLabel("Quiz Game")
        title.setObjectName("Title")
        subtitle = QLabel("Log in or create an account to save scores.")
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

        btn = QPushButton("Continue")
        btn.setObjectName("Primary")
        btn.clicked.connect(self.submit)
        root.addWidget(btn)

        root.addStretch(1)

    def _set_status(self, msg: str) -> None:
        self.status.setText(msg)

    def submit(self) -> None:
        u = self.user.text().strip()
        p = self.pw.text()

        if not u or not p:
            self._set_status("Enter a username and password.")
            return

        if self.rb_create.isChecked():
            if u in self.app.users:
                self._set_status("That username already exists.")
                return
            self.app.users[u] = {"pw_hash": data.hash_password(p), "scores": {}}
            self.app.save_users()
            self._set_status("Account created. Now log in.")
            self.rb_login.setChecked(True)
            self.pw.clear()
            self.user.setFocus()
            return

        rec = self.app.users.get(u)
        if not isinstance(rec, dict) or not data.verify_password(p, rec.get("pw_hash", "")):
            self._set_status("Wrong username or password.")
            return

        self._set_status("")
        self.pw.clear()
        self.app.current_user = u
        self.app.show_hub()


class HubPage(QWidget):
    def __init__(self, app: "MainWindow"):
        super().__init__()
        self.app = app

        root = QHBoxLayout(self)
        root.setSpacing(0)
        root.setContentsMargins(0, 0, 0, 0)

        sidebar = QFrame()
        sidebar.setObjectName("Sidebar")
        sidebar.setFixedWidth(240)
        side = QVBoxLayout(sidebar)
        side.setContentsMargins(18, 18, 18, 18)
        side.setSpacing(12)

        btn_profile = QPushButton("👤  Profile")
        btn_profile.setObjectName("Primary")
        btn_profile.clicked.connect(self.app.show_profile)

        btn_settings = QPushButton("⚙️  Settings")
        btn_settings.clicked.connect(self.app.show_settings)

        logout_btn = QPushButton("Logout")
        logout_btn.setObjectName("Danger")
        logout_btn.clicked.connect(self.app.logout)

        side.addWidget(btn_profile)
        side.addWidget(btn_settings)
        side.addStretch(1)
        side.addWidget(logout_btn)

        root.addWidget(sidebar)

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

    def refresh(self) -> None:
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
            self.grid.addWidget(self._subject_tile(subject, icon, best), r, c)
            c += 1
            if c >= cols:
                c = 0
                r += 1

    def _subject_tile(self, subject: str, icon: str, best: int) -> QWidget:
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


class ProfilePage(QWidget):
    def __init__(self, app: "MainWindow"):
        super().__init__()
        self.app = app

        root = QVBoxLayout(self)
        root.setSpacing(14)

        top = QHBoxLayout()
        back = QPushButton("← Back")
        back.clicked.connect(self.app.show_hub)
        top.addWidget(back)
        top.addStretch(1)

        title = QLabel("Profile")
        title.setObjectName("Title")
        top.addWidget(title)
        root.addLayout(top)

        self.user_lbl = QLabel("")
        self.user_lbl.setObjectName("TileTitle")
        root.addWidget(self.user_lbl)

        info = QLabel("Online leaderboards: placeholder for now (add API later).")
        info.setObjectName("Muted")
        info.setWordWrap(True)
        root.addWidget(info)

        self.scores_box = QVBoxLayout()
        self.scores_box.setSpacing(10)
        root.addLayout(self.scores_box)

        root.addStretch(1)

    def refresh(self) -> None:
        self.user_lbl.setText(f"👤 {self.app.current_user}")

        while self.scores_box.count():
            item = self.scores_box.takeAt(0)
            w = item.widget()
            if w:
                w.deleteLater()

        scores = self.app.users.get(self.app.current_user, {}).get("scores", {})
        if not scores:
            msg = QLabel("No scores yet. Go do a quiz.")
            msg.setObjectName("Muted")
            self.scores_box.addWidget(msg)
            return

        for subject, best in sorted(scores.items(), key=lambda x: (-x[1], x[0])):
            row = QFrame()
            row.setObjectName("Tile")
            lay = QHBoxLayout(row)
            lay.setContentsMargins(14, 10, 14, 10)

            left = QLabel(subject)
            left.setObjectName("TileTitle")

            right = QLabel(f"Best: {best}")
            right.setObjectName("TileSub")

            lay.addWidget(left)
            lay.addStretch(1)
            lay.addWidget(right)

            self.scores_box.addWidget(row)


class SettingsPage(QWidget):
    def __init__(self, app: "MainWindow"):
        super().__init__()
        self.app = app

        root = QVBoxLayout(self)
        root.setSpacing(14)

        top = QHBoxLayout()
        back = QPushButton("← Back")
        back.clicked.connect(self.app.show_hub)
        top.addWidget(back)
        top.addStretch(1)

        title = QLabel("Settings")
        title.setObjectName("Title")
        top.addWidget(title)
        root.addLayout(top)

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
        root.addWidget(theme_tile)

        size_tile = QFrame()
        size_tile.setObjectName("Tile")
        size_l = QVBoxLayout(size_tile)
        size_l.setContentsMargins(14, 10, 14, 10)
        size_l.setSpacing(10)

        size_label = QLabel("Window size")
        size_label.setObjectName("TileTitle")
        size_l.addWidget(size_label)

        row = QHBoxLayout()
        row.addWidget(self._size_btn("Small (900×600)", 900, 600))
        row.addWidget(self._size_btn("Medium (1100×680)", 1100, 680))
        row.addWidget(self._size_btn("Large (1300×820)", 1300, 820))
        size_l.addLayout(row)

        root.addWidget(size_tile)
        root.addStretch(1)

    def _size_btn(self, label: str, w: int, h: int) -> QPushButton:
        b = QPushButton(label)
        b.clicked.connect(lambda: self.apply_size(w, h))
        return b

    def refresh(self) -> None:
        t = self.app.settings.get("theme", "dark")
        self.btn_theme.setText("Dark" if t == "dark" else "Light")

    def toggle_theme(self) -> None:
        self.app.settings["theme"] = "light" if self.app.settings.get("theme") == "dark" else "dark"
        data.save_settings(self.app.settings)
        self.app.apply_theme()
        self.refresh()

    def apply_size(self, w: int, h: int) -> None:
        self.app.settings["window_width"] = w
        self.app.settings["window_height"] = h
        data.save_settings(self.app.settings)
        self.app.resize(w, h)


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
        back = QPushButton("← Subjects")
        back.clicked.connect(self.app.show_hub)
        top.addWidget(back)
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
        self.lbl_q.setStyleSheet("font-size: 14px;")
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

    def load_subject(self, subject: str, questions: List[Dict[str, Any]]) -> None:
        self.subject = subject
        self.questions = questions
        self.index = 0
        self.score = 0
        self.lbl_feedback.setText("")
        self._render()

    def _clear_choices(self) -> None:
        while self.choices_box.count():
            item = self.choices_box.takeAt(0)
            w = item.widget()
            if w:
                self.choice_group.removeButton(w)
                w.deleteLater()

    def _render(self) -> None:
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

    def submit(self) -> None:
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
            self._finish()
        else:
            self._render()

    def _finish(self) -> None:
        total = len(self.questions)
        subject = self.subject

        user = self.app.users.setdefault(self.app.current_user, {"pw_hash": "", "scores": {}})
        scores = user.setdefault("scores", {})
        best = scores.get(subject, 0)

        if self.score > best:
            scores[subject] = self.score
            self.app.save_users()

        QMessageBox.information(self, "Finished", f"Score: {self.score}/{total}\nBest: {scores.get(subject, self.score)}")
        self.app.show_hub()


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        data.ensure_questions_file()
        self.settings = data.load_settings()
        self.users: Dict[str, Any] = data.load_users()
        self.qbank: Dict[str, Any] = data.load_questions()
        self.current_user: Optional[str] = None

        self.setWindowTitle("Quiz Game")
        self.setMinimumSize(900, 600)
        self.resize(self.settings["window_width"], self.settings["window_height"])

        self.stack = QStackedWidget()
        self.setCentralWidget(self.stack)

        self.login_page = LoginPage(self)
        self.hub_page = HubPage(self)
        self.profile_page = ProfilePage(self)
        self.settings_page = SettingsPage(self)
        self.quiz_page = QuizPage(self)

        for p in (self.login_page, self.hub_page, self.profile_page, self.settings_page, self.quiz_page):
            self.stack.addWidget(p)

        self.apply_theme()
        self.show_login()

    def apply_theme(self) -> None:
        theme = THEME_LIGHT if self.settings.get("theme") == "light" else THEME_DARK
        QApplication.instance().setStyleSheet(stylesheet(theme))

    def save_users(self) -> None:
        data.save_users(self.users)

    def show_login(self) -> None:
        self.current_user = None
        self.stack.setCurrentWidget(self.login_page)

    def show_hub(self) -> None:
        self.hub_page.refresh()
        self.stack.setCurrentWidget(self.hub_page)

    def show_profile(self) -> None:
        self.profile_page.refresh()
        self.stack.setCurrentWidget(self.profile_page)

    def show_settings(self) -> None:
        self.settings_page.refresh()
        self.stack.setCurrentWidget(self.settings_page)

    def start_quiz(self, subject: str) -> None:
        questions = self.qbank.get(subject, [])
        if not questions:
            QMessageBox.warning(self, "No questions", f"No questions for '{subject}'. Add them in {data.QUESTIONS_FILE}.")
            return
        self.quiz_page.load_subject(subject, questions)
        self.stack.setCurrentWidget(self.quiz_page)

    def logout(self) -> None:
        self.show_login()


def main():
    app = QApplication([])
    win = MainWindow()
    win.show()
    app.exec()


if __name__ == "__main__":
    main()
