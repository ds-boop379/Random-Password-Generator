import tkinter as tk
from tkinter import ttk, messagebox
from generator import generate_password, validate_params, MIN_LENGTH, MAX_LENGTH
from storage import load_history, add_to_history

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Random Password Generator")
        self.root.geometry("600x500")

        self.length_var = tk.IntVar(value=12)
        self.digits_var = tk.BooleanVar(value=True)
        self.letters_var = tk.BooleanVar(value=True)
        self.special_var = tk.BooleanVar(value=True)

        self._build_ui()
        self._refresh_table()

    def _build_ui(self):
        frame = ttk.LabelFrame(self.root, text="Параметры пароля", padding=10)
        frame.pack(fill=tk.X, padx=10, pady=5)

        ttk.Label(frame, text="Длина пароля:").grid(row=0, column=0, sticky=tk.W)
        scale = ttk.Scale(frame, from_=MIN_LENGTH, to=MAX_LENGTH,
                          variable=self.length_var, orient=tk.HORIZONTAL,
                          command=lambda e: self._update_len_label())
        scale.grid(row=0, column=1, sticky=tk.EW, padx=5)
        self.len_label = ttk.Label(frame, textvariable=self.length_var, width=3)
        self.len_label.grid(row=0, column=2)

        ttk.Checkbutton(frame, text="Цифры (0-9)", variable=self.digits_var).grid(row=1, column=1, sticky=tk.W)
        ttk.Checkbutton(frame, text="Буквы (a-z, A-Z)", variable=self.letters_var).grid(row=2, column=1, sticky=tk.W)
        ttk.Checkbutton(frame, text="Спецсимволы (!@#...)", variable=self.special_var).grid(row=3, column=1, sticky=tk.W)
        frame.columnconfigure(1, weight=1)

        ttk.Button(self.root, text="Сгенерировать пароль", command=self._generate).pack(pady=10)

        self.result_var = tk.StringVar()
        ttk.Entry(self.root, textvariable=self.result_var, font=("Courier", 14), justify="center")\
            .pack(fill=tk.X, padx=10, pady=5)

        hist_frame = ttk.LabelFrame(self.root, text="История паролей", padding=10)
        hist_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        cols = ("timestamp", "password", "length", "digits", "letters", "special")
        self.tree = ttk.Treeview(hist_frame, columns=cols, show="headings", height=8)
        for c in cols:
            self.tree.heading(c, text=c.capitalize())
        self.tree.column("timestamp", width=120)
        self.tree.column("password", width=150)
        self.tree.column("length", width=50)
        self.tree.column("digits", width=50)
        self.tree.column("letters", width=50)
        self.tree.column("special", width=50)

        scrollbar = ttk.Scrollbar(hist_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    def _update_len_label(self):
        self.len_label.config(text=str(self.length_var.get()))

    def _generate(self):
        length = self.length_var.get()
        digits = self.digits_var.get()
        letters = self.letters_var.get()
        special = self.special_var.get()

        errors = validate_params(length, digits, letters, special)
        if errors:
            messagebox.showerror("Ошибка", "\n".join(errors))
            return

        password = generate_password(length, digits, letters, special)
        self.result_var.set(password)
        add_to_history(password, length, digits, letters, special)
        self._refresh_table()

    def _refresh_table(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        for entry in load_history():
            self.tree.insert("", tk.END, values=(
                entry.get("timestamp", ""),
                entry.get("password", ""),
                entry.get("length", ""),
                "да" if entry.get("digits") else "нет",
                "да" if entry.get("letters") else "нет",
                "да" if entry.get("special") else "нет"
            ))
