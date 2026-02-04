import json
import os
import hashlib
import tkinter as tk
from tkinter import messagebox

USERS_FILE = "users.json"
QUESTIONS_FILE = "questions.json"


def sha256(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def load_json(path, default):
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return default


def save_json(path, data):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)


class QuizApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Educational Quiz Game")
        self.resizable(False, False)

        self.users = load_json(USERS_FILE, {})  # {username: {pw_hash: "...", scores: {subject: best}}}
        self.qbank = load_json(QUESTIONS_FILE, {})  # {subject: [ {q, choices, answer}, ... ]}

        self.current_user = None
        self.current_subject = None
        self.questions = []
        self.q_index = 0
        self.score = 0

        self.container = tk.Frame(self, padx=12, pady=12)
        self.container.pack()

        self.show_login()

    def clear(self):
        for w in self.container.winfo_children():
            w.destroy()

    # ---------- LOGIN / CREATE ----------
    def show_login(self):
        self.clear()

        tk.Label(self.container, text="Login / Create Account", font=("Arial", 14, "bold")).grid(row=0, column=0, columnspan=2, pady=(0, 10))

        self.mode = tk.StringVar(value="login")
        tk.Radiobutton(self.container, text="Login", variable=self.mode, value="login").grid(row=1, column=0, sticky="w")
        tk.Radiobutton(self.container, text="Create", variable=self.mode, value="create").grid(row=1, column=1, sticky="w")

        tk.Label(self.container, text="Username").grid(row=2, column=0, columnspan=2, sticky="w", pady=(10, 0))
        self.ent_user = tk.Entry(self.container, width=30)
        self.ent_user.grid(row=3, column=0, columnspan=2, sticky="w")

        tk.Label(self.container, text="Password").grid(row=4, column=0, columnspan=2, sticky="w", pady=(10, 0))
        self.ent_pass = tk.Entry(self.container, width=30, show="*")
        self.ent_pass.grid(row=5, column=0, columnspan=2, sticky="w")

        tk.Button(self.container, text="Submit", width=28, command=self.submit_login).grid(row=6, column=0, columnspan=2, pady=(12, 0))

        self.bind("<Return>", lambda e: self.submit_login())

    def submit_login(self):
        u = self.ent_user.get().strip()
        p = self.ent_pass.get()

        if not u or not p:
            messagebox.showerror("Error", "Enter a username and password.")
            return

        hp = sha256(p)

        if self.mode.get() == "create":
            if u in self.users:
                messagebox.showerror("Error", "That user already exists.")
                return
            self.users[u] = {"pw_hash": hp, "scores": {}}
            save_json(USERS_FILE, self.users)
            messagebox.showinfo("Success", "Account created. Now login.")
            self.mode.set("login")
            self.ent_pass.delete(0, tk.END)
            return

        # login
        rec = self.users.get(u)
        if not rec or rec.get("pw_hash") != hp:
            messagebox.showerror("Nope", "Wrong username or password.")
            return

        self.current_user = u
        self.show_subject_hub()

    # ---------- SUBJECT HUB ----------
    def show_subject_hub(self):
        self.clear()

        tk.Label(self.container, text=f"Welcome, {self.current_user}", font=("Arial", 12, "bold")).grid(row=0, column=0, sticky="w")
        tk.Button(self.container, text="Logout", command=self.logout).grid(row=0, column=1, sticky="e")

        tk.Label(self.container, text="Choose a subject:", font=("Arial", 12)).grid(row=1, column=0, columnspan=2, sticky="w", pady=(10, 8))

        subjects = list(self.qbank.keys())
        if not subjects:
            tk.Label(self.container, text="No subjects found. Add some to questions.json.").grid(row=2, column=0, columnspan=2, sticky="w")
            return

        # "Clickable objects": we’ll do big buttons in a grid (simple + obvious)
        # You can swap these for image buttons later if you want.
        cols = 2
        r = 2
        c = 0

        for subject in subjects:
            best = self.users[self.current_user].get("scores", {}).get(subject, 0)
            text = f"{subject}\nBest: {best}"

            btn = tk.Button(
                self.container,
                text=text,
                width=18,
                height=4,
                command=lambda s=subject: self.start_quiz(s)
            )
            btn.grid(row=r, column=c, padx=6, pady=6, sticky="nsew")

            c += 1
            if c >= cols:
                c = 0
                r += 1

    def logout(self):
        self.current_user = None
        self.show_login()

    # ---------- QUIZ ----------
    def start_quiz(self, subject):
        qs = self.qbank.get(subject, [])
        if not qs:
            messagebox.showerror("Error", f"No questions for {subject}.")
            return

        self.current_subject = subject
        self.questions = qs
        self.q_index = 0
        self.score = 0
        self.show_question()

    def show_question(self):
        self.clear()

        subject = self.current_subject
        total = len(self.questions)
        q = self.questions[self.q_index]

        tk.Button(self.container, text="← Back to subjects", command=self.show_subject_hub).grid(row=0, column=0, sticky="w")
        tk.Label(self.container, text=f"{subject} ({self.q_index+1}/{total})", font=("Arial", 12, "bold")).grid(row=0, column=1, sticky="e")

        tk.Label(self.container, text=q["q"], wraplength=380, justify="left", font=("Arial", 12)).grid(row=1, column=0, columnspan=2, sticky="w", pady=(12, 10))

        self.choice_var = tk.IntVar(value=-1)

        for i, choice in enumerate(q["choices"]):
            rb = tk.Radiobutton(self.container, text=choice, variable=self.choice_var, value=i, anchor="w", justify="left")
            rb.grid(row=2+i, column=0, columnspan=2, sticky="w", pady=2)

        tk.Button(self.container, text="Submit Answer", command=self.submit_answer).grid(row=2+len(q["choices"]), column=0, columnspan=2, pady=(12, 0))

    def submit_answer(self):
        pick = self.choice_var.get()
        if pick == -1:
            messagebox.showerror("Error", "Pick an answer.")
            return

        q = self.questions[self.q_index]
        correct = int(q["answer"])

        if pick == correct:
            self.score += 1
            messagebox.showinfo("Correct", "Correct.")
        else:
            messagebox.showinfo("Wrong", f"Wrong.\nCorrect answer: {q['choices'][correct]}")

        self.q_index += 1
        if self.q_index >= len(self.questions):
            self.finish_quiz()
        else:
            self.show_question()

    def finish_quiz(self):
        subject = self.current_subject
        total = len(self.questions)

        # Update best score
        scores = self.users[self.current_user].setdefault("scores", {})
        best = scores.get(subject, 0)
        if self.score > best:
            scores[subject] = self.score
            save_json(USERS_FILE, self.users)

        messagebox.showinfo("Quiz Finished", f"Score: {self.score}/{total}")
        self.show_subject_hub()


if __name__ == "__main__":
    # Small sanity check so the user doesn’t stare at a blank app and cry.
    if not os.path.exists(QUESTIONS_FILE):
        save_json(QUESTIONS_FILE, {
            "Math": [
                {"q": "2 + 2 = ?", "choices": ["3", "4", "5", "22"], "answer": 1}
            ],
            "Science": [
                {"q": "Water freezes at what temperature (°C)?", "choices": ["0", "100", "-10", "50"], "answer": 0}
            ]
        })

    app = QuizApp()
    app.mainloop()