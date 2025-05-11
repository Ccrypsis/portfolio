# Anthony Robbins, CIS 345, Final Project, Online

import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
from registration import Registration, register_customer, cancel_registration, display_grouped, load_registrations, save_registrations

CLASSES = [
    ("Yoga", "9:00 AM"),
    ("Pilates", "11:00 AM"),
    ("Spin", "1:00 PM"),
    ("Zumba", "3:00 PM")
]

class SunshineFitnessApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Sunshine Fitness Studio - Class Registration")
        self.geometry("600x600")
        self.configure(bg="#f0f8ff")

        image = Image.open("fitness_logo.png")
        image = image.resize((150, 150))
        self.logo = ImageTk.PhotoImage(image)
        logo_label = tk.Label(self, image=self.logo, bg="#f0f8ff")
        logo_label.pack(pady=10)

        tk.Label(self, text="Welcome to Sunshine Fitness Studio!", font=("Helvetica", 18, "bold"), fg="#ff6600", bg="#f0f8ff").pack(pady=10)

        self.role_var = tk.StringVar()
        role_frame = tk.Frame(self, bg="#f0f8ff")
        role_frame.pack(pady=5)
        ttk.Radiobutton(role_frame, text="Customer", variable=self.role_var, value="Customer", command=self.show_customer_page).grid(row=0, column=0, padx=10)
        ttk.Radiobutton(role_frame, text="Staff", variable=self.role_var, value="Staff", command=self.show_staff_page).grid(row=0, column=1, padx=10)

        self.dynamic_frame = tk.Frame(self, bg="#f0f8ff")
        self.dynamic_frame.pack(pady=20)

        tk.Button(self, text="Exit App", command=self.quit, bg="#ff6666", fg="white", font=("Helvetica", 12, "bold"), width=15).pack(pady=10)

    def clear_frame(self):
        for widget in self.dynamic_frame.winfo_children():
            widget.destroy()

    def show_customer_page(self):
        self.clear_frame()
        tk.Label(self.dynamic_frame, text="Customer Name:", bg="#f0f8ff").pack()
        self.name_entry = tk.Entry(self.dynamic_frame, width=30)
        self.name_entry.pack()

        tk.Label(self.dynamic_frame, text="Customer Email:", bg="#f0f8ff").pack()
        self.email_entry = tk.Entry(self.dynamic_frame, width=30)
        self.email_entry.pack()

        tk.Label(self.dynamic_frame, text="Choose a Class:", font=("Helvetica", 12, "bold"), bg="#f0f8ff").pack(pady=5)
        self.class_var = tk.StringVar()
        for class_name, class_time in CLASSES:
            class_display = f"{class_name} at {class_time}"
            ttk.Radiobutton(self.dynamic_frame, text=class_display, variable=self.class_var, value=class_display).pack(anchor="w")

        tk.Button(self.dynamic_frame, text="Register", command=self.handle_register, bg="#add8e6").pack(pady=5)
        tk.Button(self.dynamic_frame, text="Cancel Registration", command=self.handle_cancel, bg="#ffcccb").pack(pady=5)

    def handle_register(self):
        name = self.name_entry.get().strip()
        email = self.email_entry.get().strip()
        class_info = self.class_var.get().strip()
        if not all([name, email, class_info]):
            messagebox.showerror("Missing Info", "Please fill out all fields.")
            return
        class_name, class_time = class_info.split(" at ")
        success = register_customer(name, email, class_name, class_time)  #method called
        if success:
            messagebox.showinfo("Success", "Registration complete!")
            self.name_entry.delete(0, tk.END)
            self.email_entry.delete(0, tk.END)
        else:
            messagebox.showwarning("Duplicate", "Customer is already registered for this class.")

    def handle_cancel(self):
        name = self.name_entry.get().strip()
        email = self.email_entry.get().strip()
        class_info = self.class_var.get().strip()
        if not all([name, email, class_info]):
            messagebox.showerror("Missing Info", "Please fill out all fields to cancel.")
            return
        class_name, class_time = class_info.split(" at ")
        success = cancel_registration(name, email, class_name, class_time) #method called
        if success:
            messagebox.showinfo("Success", "Registration cancelled.")
        else:
            messagebox.showwarning("Not Found", "No matching registration found.")

    def show_staff_page(self):
        pin_window = tk.Toplevel(self)
        pin_window.title("Staff PIN")
        pin_window.geometry("250x150")
        pin_window.configure(bg="#f0f8ff")

        tk.Label(pin_window, text="Enter Staff PIN:", bg="#f0f8ff").pack(pady=10)
        pin_entry = tk.Entry(pin_window, show="*")
        pin_entry.pack(pady=5)

        def check_pin():
            if pin_entry.get() == "4444":
                pin_window.destroy()
                self.display_staff_controls()
            else:
                messagebox.showerror("Access Denied", "Incorrect PIN")

        tk.Button(pin_window, text="Submit", command=check_pin).pack(pady=10)

    def display_staff_controls(self):
        self.clear_frame()
        tk.Label(self.dynamic_frame, text="Class Registrations", font=("Helvetica", 14, "bold"), bg="#f0f8ff").pack(pady=5)
        self.registration_listbox = tk.Listbox(self.dynamic_frame, width=70)
        self.registration_listbox.pack(pady=10)
        self.refresh_registrations()

        tk.Button(self.dynamic_frame, text="Delete Selected Registration", command=self.delete_selected_registration, bg="#ff6666", fg="white").pack(pady=5)
        tk.Button(self.dynamic_frame, text="Edit Selected Registration", command=self.edit_selected_registration, bg="#add8e6").pack(pady=5)

    def refresh_registrations(self):
        self.registration_listbox.delete(0, tk.END)
        for line in display_grouped():                                #method called
            self.registration_listbox.insert(tk.END, line)

    def delete_selected_registration(self):
        selection = self.registration_listbox.curselection()
        if not selection:
            messagebox.showwarning("No Selection", "Please select a registration to delete.")
            return
        selected_text = self.registration_listbox.get(selection[0])
        if selected_text.startswith("==="):
            messagebox.showwarning("Invalid Selection", "Please select a customer, not a header.")
            return
        try:
            name, email, rest = selected_text.split(" | ")
            class_part, _ = rest.split(" - ", 1)
            class_name, time = class_part.strip().rsplit(" at ", 1)
        except ValueError:
            messagebox.showerror("Parsing Error", "Could not parse selected item.")
            return
        registrations = load_registrations()
        updated = [
            r for r in registrations
            if not (r.name == name and r.email == email and r.class_name == class_name and r.time == time)
        ]
        if len(updated) == len(registrations):
            messagebox.showinfo("Not Found", "Could not find the selected registration.")
        else:
            save_registrations(updated)
            messagebox.showinfo("Deleted", "Registration has been deleted.")
            self.refresh_registrations()

    def edit_selected_registration(self):
        selection = self.registration_listbox.curselection()
        if not selection:
            messagebox.showwarning("No Selection", "Please select a registration to edit.")
            return
        selected_text = self.registration_listbox.get(selection[0])
        if selected_text.startswith("==="):
            messagebox.showwarning("Invalid Selection", "Please select a customer, not a header.")
            return
        name, email, rest = selected_text.split(" | ")
        class_part, _ = rest.split(" - ", 1)
        class_name, time = class_part.strip().rsplit(" at ", 1)
        registrations = load_registrations()                  #method called
        original = next((r for r in registrations if r.name == name and r.email == email and r.class_name == class_name and r.time == time), None)
        if not original:
            messagebox.showinfo("Not Found", "Could not find the selected registration.")
            return
        edit_window = tk.Toplevel(self)
        edit_window.title("Edit Registration")
        edit_window.geometry("400x300")
        edit_window.configure(bg="#f0f8ff")

        tk.Label(edit_window, text="Name:", bg="#f0f8ff").pack()
        name_entry = tk.Entry(edit_window, width=30)
        name_entry.insert(0, original.name)
        name_entry.pack()

        tk.Label(edit_window, text="Email:", bg="#f0f8ff").pack()
        email_entry = tk.Entry(edit_window, width=30)
        email_entry.insert(0, original.email)
        email_entry.pack()

        tk.Label(edit_window, text="Class:", bg="#f0f8ff").pack()
        class_var = tk.StringVar()
        for class_name, class_time in CLASSES:
            value = f"{class_name} at {class_time}"
            ttk.Radiobutton(edit_window, text=value, variable=class_var, value=value).pack(anchor="w")
        class_var.set(f"{original.class_name} at {original.time}")

        def save_changes():
            new_name = name_entry.get().strip()
            new_email = email_entry.get().strip()
            class_info = class_var.get().strip()
            if not all([new_name, new_email, class_info]):
                messagebox.showerror("Missing Info", "Please fill out all fields.")
                return
            new_class, new_time = class_info.split(" at ")
            registrations.remove(original)
            registrations.append(Registration(new_name, new_email, new_class, new_time, original.duration, original.fee))
            save_registrations(registrations)             #method called
            messagebox.showinfo("Success", "Registration updated successfully.")
            edit_window.destroy()
            self.refresh_registrations()

        tk.Button(edit_window, text="Save Changes", command=save_changes, bg="#90ee90").pack(pady=10)

if __name__ == "__main__":
    app = SunshineFitnessApp()
    app.mainloop()
