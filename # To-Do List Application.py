import tkinter as tk
from tkinter import ttk
from tkinter import messagebox


class TodoApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Professional To-Do List")
        self.geometry("620x720")
        self.resizable(False, False)
        self.configure(bg="#0f172a")

        self.tasks = []
        self.view_task_indices = []
        self.selected_index = None
        self.task_text = tk.StringVar()
        self.priority_text = tk.StringVar(value="Medium")
        self.search_text = tk.StringVar()
        self.filter_mode = tk.StringVar(value="All")

        self._setup_style()
        self._build_header()
        self._build_task_panel()
        self._build_filter_panel()
        self._build_actions_panel()
        self._build_footer()

        self.bind("<Return>", lambda event: self.add_task())
        self.bind("<Delete>", lambda event: self.delete_task())

    def _setup_style(self):
        style = ttk.Style(self)
        style.theme_use("clam")
        style.configure("Card.TFrame", background="#111827")
        style.configure("Section.TLabel", background="#0f172a", foreground="#e2e8f0", font=("Segoe UI", 18, "bold"))
        style.configure("Subtitle.TLabel", background="#0f172a", foreground="#94a3b8", font=("Segoe UI", 10))
        style.configure("Field.TLabel", background="#111827", foreground="#e2e8f0", font=("Segoe UI", 12))
        style.configure("TEntry", fieldbackground="#1e293b", foreground="#e2e8f0", padding=8)
        style.configure("TCombobox", fieldbackground="#1e293b", foreground="#e2e8f0", background="#1e293b")
        style.configure("TButton", font=("Segoe UI", 10, "bold"), padding=10)
        style.configure("Primary.TButton", background="#2563eb", foreground="#ffffff")
        style.map("Primary.TButton", background=[("active", "#1d4ed8")])
        style.configure("Accent.TButton", background="#14b8a6", foreground="#ffffff")
        style.map("Accent.TButton", background=[("active", "#0f766e")])
        style.configure("Danger.TButton", background="#ef4444", foreground="#ffffff")
        style.map("Danger.TButton", background=[("active", "#dc2626")])
        style.configure("Secondary.TButton", background="#475569", foreground="#ffffff")
        style.map("Secondary.TButton", background=[("active", "#334155")])

    def _build_header(self):
        header_frame = ttk.Frame(self, style="Card.TFrame", padding=(28, 24, 28, 18))
        header_frame.pack(fill="x", padx=24, pady=(24, 8))

        title = ttk.Label(header_frame, text="TO-DO LIST", style="Section.TLabel")
        title.pack(anchor="w")

        subtitle = ttk.Label(
            header_frame,
            text="Plan your day with focus, priority, and smooth interactions.",
            style="Subtitle.TLabel",
        )
        subtitle.pack(anchor="w", pady=(6, 0))

    def _build_task_panel(self):
        task_frame = ttk.Frame(self, style="Card.TFrame", padding=24)
        task_frame.pack(fill="x", padx=24, pady=(0, 12))

        entry_label = ttk.Label(task_frame, text="Task description", style="Field.TLabel")
        entry_label.pack(anchor="w", pady=(0, 8))

        task_entry = ttk.Entry(task_frame, textvariable=self.task_text, style="TEntry", font=("Segoe UI", 12))
        task_entry.pack(fill="x", pady=(0, 16))
        task_entry.focus()

        options_frame = ttk.Frame(task_frame, style="Card.TFrame")
        options_frame.pack(fill="x", pady=(0, 16))

        priority_label = ttk.Label(options_frame, text="Priority", style="Field.TLabel")
        priority_label.grid(row=0, column=0, sticky="w")

        priority_select = ttk.Combobox(
            options_frame,
            textvariable=self.priority_text,
            values=["High", "Medium", "Low"],
            state="readonly",
            style="TCombobox",
            font=("Segoe UI", 11),
            width=12,
        )
        priority_select.grid(row=1, column=0, sticky="w")

        search_label = ttk.Label(options_frame, text="Search tasks", style="Field.TLabel")
        search_label.grid(row=0, column=1, sticky="w", padx=(28, 0))

        search_entry = ttk.Entry(options_frame, textvariable=self.search_text, style="TEntry", font=("Segoe UI", 11), width=28)
        search_entry.grid(row=1, column=1, sticky="w", padx=(28, 0))
        self.search_text.trace_add("write", lambda *_: self.refresh_tasks())

    def _build_filter_panel(self):
        filter_frame = ttk.Frame(self, style="Card.TFrame", padding=24)
        filter_frame.pack(fill="x", padx=24, pady=(0, 12))

        filter_label = ttk.Label(filter_frame, text="Filter tasks", style="Field.TLabel")
        filter_label.pack(anchor="w", pady=(0, 4))

        button_frame = ttk.Frame(filter_frame, style="Card.TFrame")
        button_frame.pack(fill="x")

        for label, mode in [("All", "All"), ("Active", "Active"), ("Completed", "Completed")]:
            button = ttk.Radiobutton(
                button_frame,
                text=label,
                variable=self.filter_mode,
                value=mode,
                style="TButton",
                command=self.refresh_tasks,
            )
            button.pack(side="left", expand=True, fill="x", padx=6)

    def _build_actions_panel(self):
        action_frame = ttk.Frame(self, style="Card.TFrame", padding=24)
        action_frame.pack(fill="both", padx=24, pady=(0, 12), expand=True)

        action_buttons = ttk.Frame(action_frame, style="Card.TFrame")
        action_buttons.pack(fill="x", pady=(0, 16))

        add_button = ttk.Button(action_buttons, text="Add Task", style="Primary.TButton", command=self.add_task)
        add_button.pack(side="left", expand=True, fill="x", padx=6)

        update_button = ttk.Button(action_buttons, text="Update Task", style="Accent.TButton", command=self.update_task)
        update_button.pack(side="left", expand=True, fill="x", padx=6)

        complete_button = ttk.Button(action_buttons, text="Complete", style="Secondary.TButton", command=self.toggle_complete)
        complete_button.pack(side="left", expand=True, fill="x", padx=6)

        list_label = ttk.Label(action_frame, text="Task list", style="Field.TLabel")
        list_label.pack(anchor="w", pady=(8, 8))

        listbox_border = tk.Frame(action_frame, bg="#1e293b", bd=0)
        listbox_border.pack(fill="both", expand=True)

        self.listbox = tk.Listbox(
            listbox_border,
            bg="#0f172a",
            fg="#e2e8f0",
            selectbackground="#2563eb",
            selectforeground="#ffffff",
            font=("Segoe UI", 12),
            activestyle="none",
            bd=0,
            highlightthickness=0,
            relief="flat",
            selectmode="browse",
        )
        self.listbox.pack(fill="both", expand=True, side="left", padx=2, pady=2)
        self.listbox.bind("<<ListboxSelect>>", self.on_task_select)
        self.listbox.bind("<Double-Button-1>", lambda event: self.toggle_complete())

        scrollbar = ttk.Scrollbar(listbox_border, orient="vertical", command=self.listbox.yview)
        scrollbar.pack(side="right", fill="y")
        self.listbox.config(yscrollcommand=scrollbar.set)

        quick_actions = ttk.Frame(action_frame, style="Card.TFrame")
        quick_actions.pack(fill="x", pady=(14, 0))

        delete_button = ttk.Button(quick_actions, text="Delete Task", style="Danger.TButton", command=self.delete_task)
        delete_button.pack(side="left", expand=True, fill="x", padx=6)

        clear_completed = ttk.Button(quick_actions, text="Clear Completed", style="Primary.TButton", command=self.clear_completed)
        clear_completed.pack(side="left", expand=True, fill="x", padx=6)

        clear_all = ttk.Button(quick_actions, text="Clear All", style="Danger.TButton", command=self.clear_all)
        clear_all.pack(side="left", expand=True, fill="x", padx=6)

    def _build_footer(self):
        footer_frame = ttk.Frame(self, style="Card.TFrame", padding=(24, 18, 24, 18))
        footer_frame.pack(fill="x", padx=24, pady=(0, 24))

        self.stats_label = ttk.Label(footer_frame, text="Total: 0 | Active: 0 | Completed: 0", style="Subtitle.TLabel")
        self.stats_label.pack(anchor="w")

        self.status_label = ttk.Label(footer_frame, text="Use the search field to filter tasks instantly.", style="Subtitle.TLabel")
        self.status_label.pack(anchor="w", pady=(8, 0))

    def add_task(self):
        text = self.task_text.get().strip()
        if not text:
            self._set_status("Type a task description before adding.", warning=True)
            return

        self.tasks.append(
            {
                "text": text,
                "done": False,
                "priority": self.priority_text.get(),
            }
        )
        self.task_text.set("")
        self.selected_index = None
        self._set_status("Task added successfully.")
        self.refresh_tasks()

    def update_task(self):
        if self.selected_index is None:
            self._set_status("Select a task to update from the list.", warning=True)
            return

        new_text = self.task_text.get().strip()
        if not new_text:
            self._set_status("Enter new text before updating.", warning=True)
            return

        self.tasks[self.selected_index]["text"] = new_text
        self.tasks[self.selected_index]["priority"] = self.priority_text.get()
        self._set_status("Task updated successfully.")
        self.refresh_tasks()

    def delete_task(self):
        if self.selected_index is None:
            self._set_status("Select a task to delete.", warning=True)
            return

        deleted_task = self.tasks.pop(self.selected_index)
        self.selected_index = None
        self.task_text.set("")
        self._set_status(f"Deleted task: {deleted_task['text']}")
        self.refresh_tasks()

    def toggle_complete(self):
        if self.selected_index is None:
            self._set_status("Select a task to toggle completion.", warning=True)
            return

        task = self.tasks[self.selected_index]
        task["done"] = not task["done"]
        if task["done"]:
            self._set_status(f"Marked complete: {task['text']}")
        else:
            self._set_status(f"Marked active: {task['text']}")
        self.refresh_tasks()

    def clear_completed(self):
        completed_count = sum(1 for task in self.tasks if task["done"])
        self.tasks = [task for task in self.tasks if not task["done"]]
        self.selected_index = None
        self.task_text.set("")
        self._set_status(f"Cleared {completed_count} completed task(s).")
        self.refresh_tasks()

    def clear_all(self):
        self.tasks = []
        self.selected_index = None
        self.task_text.set("")
        self._set_status("All tasks have been cleared.")
        self.refresh_tasks()

    def on_task_select(self, event):
        selected = self.listbox.curselection()
        if not selected:
            self.selected_index = None
            return

        view_index = selected[0]
        self.selected_index = self.view_task_indices[view_index]
        selected_task = self.tasks[self.selected_index]
        self.task_text.set(selected_task["text"])
        self.priority_text.set(selected_task["priority"])

    def _filtered_tasks(self):
        query = self.search_text.get().strip().lower()
        mode = self.filter_mode.get()
        filtered = []

        for index, task in enumerate(self.tasks):
            if mode == "Active" and task["done"]:
                continue
            if mode == "Completed" and not task["done"]:
                continue
            if query and query not in task["text"].lower():
                continue
            filtered.append((index, task))

        return filtered

    def refresh_tasks(self):
        self.listbox.delete(0, tk.END)
        self.view_task_indices = []

        filtered = self._filtered_tasks()
        for task_index, task in filtered:
            prefix = "✔" if task["done"] else "○"
            display_text = f"{prefix} {task['text']}  •  {task['priority']}"
            self.listbox.insert(tk.END, display_text)
            self.view_task_indices.append(task_index)

        total = len(self.tasks)
        completed = sum(task["done"] for task in self.tasks)
        active = total - completed
        self.stats_label.config(text=f"Total: {total} | Active: {active} | Completed: {completed}")

        if total == 0:
            self._set_status("No tasks yet. Start by adding a new task.")
        elif active == 0:
            self._set_status("All tasks completed. Great work!")
        else:
            self._set_status(f"{active} active task(s). Use search or filter to find items.")

        if self.selected_index is not None:
            try:
                view_index = self.view_task_indices.index(self.selected_index)
                self.listbox.selection_set(view_index)
                self.listbox.activate(view_index)
            except ValueError:
                self.selected_index = None

    def _set_status(self, message, warning=False):
        self.status_label.config(text=message, foreground="#f8fafc" if not warning else "#f87171")


if __name__ == "__main__":
    app = TodoApp()
    app.mainloop()
