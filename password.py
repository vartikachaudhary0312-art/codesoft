import tkinter as tk
from tkinter import messagebox, ttk
import random
import string

MIN_LENGTH = 4
MAX_LENGTH = 64

# Function to generate password
def generate_password(event=None):
    try:
        length = int(length_spinbox.get())
        if length < MIN_LENGTH or length > MAX_LENGTH:
            status_var.set(f"Length must be between {MIN_LENGTH} and {MAX_LENGTH}.")
            status_label.configure(foreground="#f28c8c")
            return

        available_chars = ""
        if uppercase_var.get():
            available_chars += string.ascii_uppercase
        if lowercase_var.get():
            available_chars += string.ascii_lowercase
        if digits_var.get():
            available_chars += string.digits
        if symbols_var.get():
            available_chars += string.punctuation

        if not available_chars:
            status_var.set("Select at least one character type.")
            status_label.configure(foreground="#f28c8c")
            return

        password = ''.join(random.choice(available_chars) for _ in range(length))
        password_var.set(password)
        status_var.set("Password generated successfully.")
        status_label.configure(foreground="#9ae69a")

    except ValueError:
        status_var.set("Enter a valid number for length.")
        status_label.configure(foreground="#f28c8c")


# Function to copy password
def copy_password(event=None):
    password = password_var.get()
    if not password:
        status_var.set("Generate a password before copying.")
        status_label.configure(foreground="#f28c8c")
        return

    root.clipboard_clear()
    root.clipboard_append(password)
    root.update()
    status_var.set("Password copied to clipboard.")
    status_label.configure(foreground="#9ae69a")


def clear_password():
    password_var.set("")
    status_var.set("")


root = tk.Tk()
root.title("Password Generator")
root.geometry("540x460")
root.resizable(False, False)
root.configure(bg="#2d3445")

style = ttk.Style(root)
style.theme_use("clam")
style.configure("TFrame", background="#2d3445")
style.configure("TLabel", background="#2d3445", foreground="#f3f4f8", font=("Segoe UI", 11))
style.configure("Title.TLabel", font=("Segoe UI", 20, "bold"), foreground="#ffffff")
style.configure("TButton", font=("Segoe UI", 11, "bold"), padding=8)
style.map(
    "TButton",
    background=[("!disabled", "#5663e5"), ("active", "#6d7ef5")],
    foreground=[("!disabled", "#ffffff")]
)
style.configure("TEntry", padding=6)
style.configure("TSpinbox", padding=6)
style.configure("TCheckbutton", background="#2d3445", foreground="#f3f4f8", font=("Segoe UI", 10))

main_frame = ttk.Frame(root, padding=20)
main_frame.pack(fill="both", expand=True)

header_frame = ttk.Frame(main_frame)
header_frame.pack(fill="x", pady=(0, 12))

ttk.Label(header_frame, text="Secure Password Generator", style="Title.TLabel").pack()
ttk.Label(header_frame, text="Build strong passwords with custom options.", font=("Segoe UI", 10), foreground="#c5c9de").pack(pady=(6, 0))

input_card = ttk.Frame(main_frame, padding=18, style="TFrame")
input_card.pack(fill="x", pady=10)
input_card.configure(borderwidth=1, relief="ridge")

length_label = ttk.Label(input_card, text="Password Length")
length_label.grid(row=0, column=0, sticky="w", pady=(0, 8))
length_spinbox = ttk.Spinbox(input_card, from_=MIN_LENGTH, to=MAX_LENGTH, width=10, justify="center")
length_spinbox.set(14)
length_spinbox.grid(row=1, column=0, sticky="w")

options_label = ttk.Label(input_card, text="Include characters")
options_label.grid(row=2, column=0, sticky="w", pady=(18, 8))

uppercase_var = tk.BooleanVar(value=True)
lowercase_var = tk.BooleanVar(value=True)
digits_var = tk.BooleanVar(value=True)
symbols_var = tk.BooleanVar(value=True)

checkbox_frame = ttk.Frame(input_card)
checkbox_frame.grid(row=3, column=0, sticky="w")

ttk.Checkbutton(checkbox_frame, text="Uppercase", variable=uppercase_var).grid(row=0, column=0, sticky="w", padx=(0, 12), pady=2)
ttk.Checkbutton(checkbox_frame, text="Lowercase", variable=lowercase_var).grid(row=0, column=1, sticky="w", padx=(0, 12), pady=2)
ttk.Checkbutton(checkbox_frame, text="Digits", variable=digits_var).grid(row=1, column=0, sticky="w", padx=(0, 12), pady=2)
ttk.Checkbutton(checkbox_frame, text="Symbols", variable=symbols_var).grid(row=1, column=1, sticky="w", pady=2)

button_frame = ttk.Frame(main_frame)
button_frame.pack(fill="x", pady=10)

generate_button = ttk.Button(button_frame, text="Generate Password", command=generate_password)
generate_button.pack(fill="x")

result_card = ttk.Frame(main_frame, padding=18, style="TFrame")
result_card.pack(fill="x", pady=10)
result_card.configure(borderwidth=1, relief="ridge")

password_var = tk.StringVar()

result_label = ttk.Label(result_card, text="Generated Password")
result_label.pack(anchor="w")
password_entry = ttk.Entry(result_card, textvariable=password_var, font=("Segoe UI", 11), justify="center", width=38, state="readonly")
password_entry.pack(fill="x", pady=(10, 12))

card_button_frame = ttk.Frame(result_card)
card_button_frame.pack(fill="x")

copy_button = ttk.Button(card_button_frame, text="Copy to Clipboard", command=copy_password)
copy_button.pack(side="left", fill="x", expand=True, padx=(0, 8))

clear_button = ttk.Button(card_button_frame, text="Clear", command=clear_password)
clear_button.pack(side="left", fill="x", expand=True)

status_var = tk.StringVar()
status_label = ttk.Label(main_frame, textvariable=status_var, font=("Segoe UI", 10), foreground="#bec4d7")
status_label.pack(pady=(10, 0))

footer_label = ttk.Label(main_frame, text="Tip: press Enter to generate and Ctrl+C to copy the password.", foreground="#bec4d7")
footer_label.pack(pady=(8, 0))

root.bind("<Return>", generate_password)
root.bind("<Control-c>", copy_password)
root.bind("<Control-C>", copy_password)

length_spinbox.focus()
root.mainloop()