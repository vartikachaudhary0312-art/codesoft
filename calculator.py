import tkinter as tk
from tkinter import ttk
from tkinter import messagebox


class StylishCalculator(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Calculator")
        self.geometry("520x420")
        self.resizable(False, False)
        self.configure(bg="#0b1220")

        self._create_styles()
        self._build_ui()
        self._bind_keys()

        self.history = []

    def _create_styles(self):
        style = ttk.Style(self)
        style.theme_use("clam")
        style.configure("TFrame", background="#0b1220")
        style.configure("Card.TFrame", background="#0f1724")
        style.configure("Title.TLabel", background="#0b1220", foreground="#e6eef8", font=("Segoe UI", 18, "bold"))
        style.configure("Label.TLabel", background="#0f1724", foreground="#dbeafe", font=("Segoe UI", 10))
        style.configure("Result.TLabel", background="#0f1724", foreground="#bff0c6", font=("Segoe UI", 16, "bold"))
        style.configure("TButton", font=("Segoe UI", 10, "bold"))
        style.configure("Accent.TButton", background="#2563eb", foreground="#ffffff")
        style.map("Accent.TButton", background=[("active", "#1e40af")])
        style.configure("Secondary.TButton", background="#334155", foreground="#ffffff")

    def _build_ui(self):
        header = ttk.Frame(self, style="TFrame")
        header.pack(fill="x", pady=(16, 6))

        title = ttk.Label(header, text="Professional Calculator", style="Title.TLabel")
        title.pack()

        card = ttk.Frame(self, style="Card.TFrame", padding=18)
        card.pack(padx=18, pady=8, fill="both", expand=True)

        # Input fields
        input_frame = ttk.Frame(card, style="Card.TFrame")
        input_frame.pack(fill="x")

        ttk.Label(input_frame, text="First number:", style="Label.TLabel").grid(row=0, column=0, sticky="w")
        self.entry1 = ttk.Entry(input_frame, font=("Segoe UI", 12))
        self.entry1.grid(row=1, column=0, sticky="we", pady=(4, 10))

        ttk.Label(input_frame, text="Second number:", style="Label.TLabel").grid(row=0, column=1, sticky="w", padx=(12, 0))
        self.entry2 = ttk.Entry(input_frame, font=("Segoe UI", 12))
        self.entry2.grid(row=1, column=1, sticky="we", padx=(12, 0), pady=(4, 10))

        input_frame.columnconfigure(0, weight=1)
        input_frame.columnconfigure(1, weight=1)

        # Operation selection
        op_frame = ttk.Frame(card, style="Card.TFrame")
        op_frame.pack(fill="x", pady=(4, 8))

        ttk.Label(op_frame, text="Operation:", style="Label.TLabel").pack(anchor="w")
        self.operation = tk.StringVar(value="+")
        ops = ["+", "-", "*", "/", "%"]
        for i, op in enumerate(ops):
            b = ttk.Radiobutton(op_frame, text=op, value=op, variable=self.operation, style="TButton")
            b.pack(side="left", padx=6, pady=6)

        # Buttons
        btn_frame = ttk.Frame(card, style="Card.TFrame")
        btn_frame.pack(fill="x", pady=(6, 12))

        calc_btn = ttk.Button(btn_frame, text="Calculate", command=self.calculate, style="Accent.TButton")
        calc_btn.pack(side="left", expand=True, fill="x", padx=(0, 8))

        clear_btn = ttk.Button(btn_frame, text="Clear", command=self.clear_inputs, style="Secondary.TButton")
        clear_btn.pack(side="left", expand=True, fill="x", padx=(8, 8))

        copy_btn = ttk.Button(btn_frame, text="Copy Result", command=self.copy_result)
        copy_btn.pack(side="left", expand=True, fill="x", padx=(8, 0))

        # Result area + history
        bottom = ttk.Frame(card, style="Card.TFrame")
        bottom.pack(fill="both", expand=True)

        result_label = ttk.Label(bottom, text="Result:", style="Label.TLabel")
        result_label.pack(anchor="w")

        self.result_var = tk.StringVar(value="—")
        self.result_display = ttk.Label(bottom, textvariable=self.result_var, style="Result.TLabel", padding=8)
        self.result_display.pack(fill="x", pady=(6, 12))

        # History
        hist_label = ttk.Label(bottom, text="History", style="Label.TLabel")
        hist_label.pack(anchor="w")

        hist_frame = ttk.Frame(bottom, style="Card.TFrame")
        hist_frame.pack(fill="both", expand=True, pady=(6, 0))

        self.history_list = tk.Listbox(hist_frame, bg="#071024", fg="#cfe8ff", bd=0, highlightthickness=0, selectbackground="#164e9c")
        self.history_list.pack(side="left", fill="both", expand=True)
        self.history_list.bind('<Double-Button-1>', self._use_history_item)

        hist_scroll = ttk.Scrollbar(hist_frame, orient="vertical", command=self.history_list.yview)
        hist_scroll.pack(side="right", fill="y")
        self.history_list.config(yscrollcommand=hist_scroll.set)

        self.entry1.focus()

    def _bind_keys(self):
        self.bind('<Return>', lambda e: self.calculate())
        self.bind('<Escape>', lambda e: self.clear_inputs())

    def calculate(self):
        a = self.entry1.get().strip()
        b = self.entry2.get().strip()
        op = self.operation.get()

        try:
            num1 = float(a)
        except ValueError:
            messagebox.showerror("Input Error", "First value is not a valid number.")
            self.entry1.focus()
            return

        try:
            num2 = float(b)
        except ValueError:
            messagebox.showerror("Input Error", "Second value is not a valid number.")
            self.entry2.focus()
            return

        try:
            if op == '+':
                res = num1 + num2
            elif op == '-':
                res = num1 - num2
            elif op == '*':
                res = num1 * num2
            elif op == '/':
                if num2 == 0:
                    raise ZeroDivisionError
                res = num1 / num2
            elif op == '%':
                res = num1 % num2
            else:
                messagebox.showwarning("Operation", "Select a valid operation.")
                return

            # Normalize result display (avoid long floats)
            if isinstance(res, float) and res.is_integer():
                res = int(res)
            else:
                res = round(res, 10)

            expr = f"{num1} {op} {num2} = {res}"
            self.result_var.set(str(res))
            self.history.insert(0, expr)
            self._refresh_history()
        except ZeroDivisionError:
            messagebox.showerror("Math Error", "Cannot divide by zero.")
            self.result_var.set("Error")

    def _refresh_history(self):
        self.history_list.delete(0, tk.END)
        for item in self.history:
            self.history_list.insert(tk.END, item)

    def _use_history_item(self, event):
        sel = self.history_list.curselection()
        if not sel:
            return
        item = self.history_list.get(sel[0])
        # parse format: 'num1 op num2 = res'
        try:
            left, _ = item.split('=', 1)
            parts = left.strip().split()
            if len(parts) >= 3:
                self.entry1.delete(0, tk.END)
                self.entry1.insert(0, parts[0])
                self.operation.set(parts[1])
                self.entry2.delete(0, tk.END)
                self.entry2.insert(0, parts[2])
        except Exception:
            pass

    def clear_inputs(self):
        self.entry1.delete(0, tk.END)
        self.entry2.delete(0, tk.END)
        self.result_var.set('—')

    def copy_result(self):
        res = self.result_var.get()
        if not res or res == '—' or res == 'Error':
            return
        self.clipboard_clear()
        self.clipboard_append(str(res))
        self._flash_message("Result copied to clipboard")

    def _flash_message(self, text):
        orig = self.result_var.get()
        self.result_var.set(text)
        self.after(1000, lambda: self.result_var.set(orig))


if __name__ == '__main__':
    app = StylishCalculator()
    app.mainloop()