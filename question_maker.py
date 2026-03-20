import json
import os
from typing import Dict, Any, List, Optional

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget,
    QHBoxLayout, QVBoxLayout, QFormLayout,
    QListWidget, QListWidgetItem,
    QLabel, QLineEdit, QPushButton, QMessageBox, QComboBox, QFrame
)

QUESTIONS_FILE = "questions.json"
CHOICE_COUNT = 4  # change if you want more options per question


def load_json(path: str, default):
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return default


def save_json(path: str, data) -> None:
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


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
                ],
            },
        )


class QuestionEditor(QMainWindow):
    def __init__(self):
        super().__init__()
        ensure_questions_file()

        self.setWindowTitle("Question Editor")
        self.resize(1100, 650)

        self.data: Dict[str, List[Dict[str, Any]]] = load_json(QUESTIONS_FILE, {})
        if not isinstance(self.data, dict):
            self.data = {}

        self.current_subject: Optional[str] = None
        self.current_question_index: Optional[int] = None
        self._dirty = False
        self._loading_ui = False

        root = QWidget()
        self.setCentralWidget(root)

        main = QHBoxLayout(root)
        main.setSpacing(14)

        # -------------------------
        # Left: Subjects
        # -------------------------
        left = QFrame()
        left.setFrameShape(QFrame.StyledPanel)
        left_l = QVBoxLayout(left)
        left_l.setSpacing(8)

        left_l.addWidget(QLabel("Subjects"))

        self.subject_list = QListWidget()
        self.subject_list.itemSelectionChanged.connect(self.on_subject_selected)
        left_l.addWidget(self.subject_list, 1)

        sub_btn_row = QHBoxLayout()
        self.btn_add_subject = QPushButton("Add")
        self.btn_rename_subject = QPushButton("Rename")
        self.btn_delete_subject = QPushButton("Delete")

        self.btn_add_subject.clicked.connect(self.add_subject)
        self.btn_rename_subject.clicked.connect(self.rename_subject)
        self.btn_delete_subject.clicked.connect(self.delete_subject)

        sub_btn_row.addWidget(self.btn_add_subject)
        sub_btn_row.addWidget(self.btn_rename_subject)
        sub_btn_row.addWidget(self.btn_delete_subject)
        left_l.addLayout(sub_btn_row)

        main.addWidget(left, 1)

        # -------------------------
        # Middle: Questions list
        # -------------------------
        mid = QFrame()
        mid.setFrameShape(QFrame.StyledPanel)
        mid_l = QVBoxLayout(mid)
        mid_l.setSpacing(8)

        self.lbl_questions = QLabel("Questions")
        mid_l.addWidget(self.lbl_questions)

        self.question_list = QListWidget()
        self.question_list.itemSelectionChanged.connect(self.on_question_selected)
        mid_l.addWidget(self.question_list, 1)

        q_btn_row = QHBoxLayout()
        self.btn_add_q = QPushButton("Add")
        self.btn_delete_q = QPushButton("Delete")
        self.btn_add_q.clicked.connect(self.add_question)
        self.btn_delete_q.clicked.connect(self.delete_question)
        q_btn_row.addWidget(self.btn_add_q)
        q_btn_row.addWidget(self.btn_delete_q)
        mid_l.addLayout(q_btn_row)

        main.addWidget(mid, 2)

        # -------------------------
        # Right: Editor
        # -------------------------
        right = QFrame()
        right.setFrameShape(QFrame.StyledPanel)
        right_l = QVBoxLayout(right)
        right_l.setSpacing(10)

        header = QHBoxLayout()
        self.lbl_editor = QLabel("Editor")
        self.lbl_editor.setStyleSheet("font-weight: 700; font-size: 16px;")
        header.addWidget(self.lbl_editor)
        header.addStretch(1)

        self.btn_save = QPushButton("Save")
        self.btn_save.clicked.connect(self.save)
        header.addWidget(self.btn_save)

        right_l.addLayout(header)

        form = QFormLayout()
        form.setLabelAlignment(Qt.AlignLeft)
        form.setFormAlignment(Qt.AlignTop)

        self.edit_question = QLineEdit()
        self.edit_question.textEdited.connect(self.mark_dirty)

        self.choice_edits: List[QLineEdit] = []
        for i in range(CHOICE_COUNT):
            e = QLineEdit()
            e.setPlaceholderText(f"Choice {i+1}")
            e.textEdited.connect(self.mark_dirty)
            self.choice_edits.append(e)

        self.cmb_answer = QComboBox()
        self.cmb_answer.currentIndexChanged.connect(self.mark_dirty)

        form.addRow("Question:", self.edit_question)
        for i, e in enumerate(self.choice_edits):
            form.addRow(f"Choice {i+1}:", e)
        form.addRow("Correct answer:", self.cmb_answer)

        right_l.addLayout(form)

        action_row = QHBoxLayout()
        self.btn_apply = QPushButton("Apply changes")
        self.btn_revert = QPushButton("Revert")
        self.btn_apply.clicked.connect(self.apply_to_model)
        self.btn_revert.clicked.connect(self.reload_editor_from_model)
        action_row.addWidget(self.btn_apply)
        action_row.addWidget(self.btn_revert)
        action_row.addStretch(1)
        right_l.addLayout(action_row)

        self.lbl_status = QLabel("")
        self.lbl_status.setStyleSheet("color: #888;")
        right_l.addWidget(self.lbl_status)

        right_l.addStretch(1)
        main.addWidget(right, 3)

        self.refresh_subjects()

    # -------------------------
    # UI helpers
    # -------------------------
    def mark_dirty(self):
        if self._loading_ui:
            return
        self._dirty = True
        self.update_status()

    def update_status(self):
        if self._dirty:
            self.lbl_status.setText("Unsaved changes (Apply changes, then Save).")
        else:
            self.lbl_status.setText("")

    def ask_text(self, title: str, label: str, initial: str = "") -> Optional[str]:
        from PySide6.QtWidgets import QInputDialog
        text, ok = QInputDialog.getText(self, title, label, text=initial)
        if not ok:
            return None
        text = text.strip()
        return text if text else None

    def confirm(self, title: str, msg: str) -> bool:
        return QMessageBox.question(self, title, msg, QMessageBox.Yes | QMessageBox.No) == QMessageBox.Yes

    # -------------------------
    # Subjects
    # -------------------------
    def refresh_subjects(self):
        self.subject_list.clear()
        subjects = sorted(self.data.keys(), key=str.lower)
        for s in subjects:
            self.subject_list.addItem(QListWidgetItem(s))

        # preserve selection if possible
        if self.current_subject and self.current_subject in self.data:
            items = self.subject_list.findItems(self.current_subject, Qt.MatchExactly)
            if items:
                self.subject_list.setCurrentItem(items[0])
        elif subjects:
            self.subject_list.setCurrentRow(0)
        else:
            self.current_subject = None
            self.refresh_questions()

    def on_subject_selected(self):
        if self._dirty:
            if not self.confirm("Unsaved changes", "You have unsaved changes. Discard them and switch subject?"):
                # revert UI selection
                self._loading_ui = True
                try:
                    if self.current_subject:
                        items = self.subject_list.findItems(self.current_subject, Qt.MatchExactly)
                        if items:
                            self.subject_list.setCurrentItem(items[0])
                finally:
                    self._loading_ui = False
                return

        item = self.subject_list.currentItem()
        self.current_subject = item.text() if item else None
        self.current_question_index = None
        self._dirty = False
        self.update_status()
        self.refresh_questions()

    def add_subject(self):
        name = self.ask_text("Add Subject", "Subject name:")
        if not name:
            return
        if name in self.data:
            QMessageBox.warning(self, "Exists", "That subject already exists.")
            return
        self.data[name] = []
        self.current_subject = name
        self.refresh_subjects()

    def rename_subject(self):
        if not self.current_subject:
            return
        new = self.ask_text("Rename Subject", "New name:", self.current_subject)
        if not new or new == self.current_subject:
            return
        if new in self.data:
            QMessageBox.warning(self, "Exists", "That subject name already exists.")
            return
        self.data[new] = self.data.pop(self.current_subject)
        self.current_subject = new
        self.refresh_subjects()

    def delete_subject(self):
        if not self.current_subject:
            return
        if not self.confirm("Delete subject", f"Delete subject '{self.current_subject}' and all its questions?"):
            return
        self.data.pop(self.current_subject, None)
        self.current_subject = None
        self.current_question_index = None
        self._dirty = False
        self.refresh_subjects()
    # -------------------------
    # Questions
    # -------------------------
    def refresh_questions(self):
        self.question_list.clear()
        self.lbl_questions.setText(f"Questions" + (f" ({self.current_subject})" if self.current_subject else ""))

        if not self.current_subject or self.current_subject not in self.data:
            self.set_editor_enabled(False)
            self.clear_editor()
            return

        qs = self.data.get(self.current_subject, [])
        for i, q in enumerate(qs):
            text = q.get("q", "").strip() or f"(Question {i+1})"
            self.question_list.addItem(QListWidgetItem(text))

        if qs:
            self.question_list.setCurrentRow(0)
        else:
            self.current_question_index = None
            self.set_editor_enabled(False)
            self.clear_editor()

    def on_question_selected(self):
        if self._dirty:
            if not self.confirm("Unsaved changes", "You have unsaved changes. Discard them and switch question?"):
                # revert selection
                self._loading_ui = True
                try:
                    if self.current_question_index is not None:
                        self.question_list.setCurrentRow(self.current_question_index)
                finally:
                    self._loading_ui = False
                return

        row = self.question_list.currentRow()
        self.current_question_index = row if row >= 0 else None
        self._dirty = False
        self.update_status()
        self.reload_editor_from_model()

    def add_question(self):
        if not self.current_subject:
            QMessageBox.warning(self, "No subject", "Create/select a subject first.")
            return

        qs = self.data.setdefault(self.current_subject, [])
        qs.append({
            "q": "New question?",
            "choices": [f"Choice {i+1}" for i in range(CHOICE_COUNT)],
            "answer": 0
        })
        self.refresh_questions()
        self.question_list.setCurrentRow(len(qs) - 1)

    def delete_question(self):
        if self.current_subject is None or self.current_question_index is None:
            return
        qs = self.data.get(self.current_subject, [])
        if not qs:
            return
        if not self.confirm("Delete question", "Delete this question?"):
            return
        qs.pop(self.current_question_index)
        self.current_question_index = None
        self._dirty = False
        self.refresh_questions()

    # -------------------------
    # Editor
    # -------------------------
    def set_editor_enabled(self, enabled: bool):
        self.edit_question.setEnabled(enabled)
        for e in self.choice_edits:
            e.setEnabled(enabled)
        self.cmb_answer.setEnabled(enabled)
        self.btn_apply.setEnabled(enabled)
        self.btn_revert.setEnabled(enabled)

    def clear_editor(self):
        self._loading_ui = True
        try:
            self.edit_question.setText("")
            for e in self.choice_edits:
                e.setText("")
            self.cmb_answer.clear()
        finally:
            self._loading_ui = False

    def reload_editor_from_model(self):
        if self.current_subject is None or self.current_question_index is None:
            self.set_editor_enabled(False)
            self.clear_editor()
            return

        qs = self.data.get(self.current_subject, [])
        if not (0 <= self.current_question_index < len(qs)):
            self.set_editor_enabled(False)
            self.clear_editor()
            return

        q = qs[self.current_question_index]
        question_text = str(q.get("q", ""))

        choices = q.get("choices", [])
        if not isinstance(choices, list):
            choices = []
        choices = [str(x) for x in choices][:CHOICE_COUNT]
        while len(choices) < CHOICE_COUNT:
            choices.append("")

        answer = int(q.get("answer", 0))
        if answer < 0 or answer >= CHOICE_COUNT:
            answer = 0

        self._loading_ui = True
        try:
            self.set_editor_enabled(True)
            self.edit_question.setText(question_text)
            for i, e in enumerate(self.choice_edits):
                e.setText(choices[i])

            self.cmb_answer.clear()
            for i in range(CHOICE_COUNT):
                label = choices[i].strip() or f"Choice {i+1}"
                self.cmb_answer.addItem(f"{i+1}. {label}", i)
            self.cmb_answer.setCurrentIndex(answer)
        finally:
            self._loading_ui = False

        self._dirty = False
        self.update_status()

    def apply_to_model(self):
        if self.current_subject is None or self.current_question_index is None:
            return

        q_text = self.edit_question.text().strip()
        choices = [e.text().strip() for e in self.choice_edits]
        answer = self.cmb_answer.currentIndex()

        # Validation: no empty question/choices
        if not q_text:
            QMessageBox.warning(self, "Invalid", "Question text can't be empty.")
            return
        if any(not c for c in choices):
            QMessageBox.warning(self, "Invalid", "All choices must be filled in.")
            return
        if answer < 0 or answer >= len(choices):
            QMessageBox.warning(self, "Invalid", "Select a correct answer.")
            return

        qs = self.data.get(self.current_subject, [])
        if not (0 <= self.current_question_index < len(qs)):
            return

        qs[self.current_question_index] = {"q": q_text, "choices": choices, "answer": answer}
        self._dirty = False
        self.update_status()

        # update list display text + answer dropdown labels
        self.refresh_questions()
        self.question_list.setCurrentRow(self.current_question_index)
        self.reload_editor_from_model()

    def save(self):
        if self._dirty:
            QMessageBox.warning(self, "Unsaved changes", "Click 'Apply changes' first, then Save.")
            return
        save_json(QUESTIONS_FILE, self.data)
        QMessageBox.information(self, "Saved", f"Saved to {QUESTIONS_FILE}.")


def main():
    app = QApplication([])
    win = QuestionEditor()
    win.show()
    app.exec()


if __name__ == "__main__":
    main()
