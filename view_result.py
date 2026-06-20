import tkinter as tk
from tkinter import ttk, messagebox

# Functions
def save_data():
    messagebox.showinfo("Save", "Course Saved")

def update_data():
    messagebox.showinfo("Update", "Course Updated")

def delete_data():
    messagebox.showinfo("Delete", "Course Deleted")

def clear_data():
    entry_course.delete(0, tk.END)
    entry_duration.delete(0, tk.END)
    entry_charges.delete(0, tk.END)
    txt_description.delete("1.0", tk.END)

# Main window
root = tk.Tk()
root.title("Student Result Management System")
root.geometry("1100x600")
root.configure(bg="white")

# Title bar
title = tk.Label(root, text="Manage Course Details",
                 bg="darkblue", fg="white",
                 font=("Times New Roman", 24, "bold"))
title.pack(fill="x", pady=10)

# Left section
tk.Label(root, text="Course Name", font=("Times New Roman", 16), bg="white").place(x=20, y=80)
entry_course = tk.Entry(root, width=25)
entry_course.place(x=180, y=85)

tk.Label(root, text="Duration", font=("Times New Roman", 16), bg="white").place(x=20, y=130)
entry_duration = tk.Entry(root, width=25)
entry_duration.place(x=180, y=135)

tk.Label(root, text="Charges", font=("Times New Roman", 16), bg="white").place(x=20, y=180)
entry_charges = tk.Entry(root, width=25)
entry_charges.place(x=180, y=185)

tk.Label(root, text="Description", font=("Times New Roman", 16), bg="white").place(x=20, y=230)
txt_description = tk.Text(root, width=45, height=8)
txt_description.place(x=180, y=235)

# Buttons
tk.Button(root, text="Save", bg="dodgerblue", fg="white",
          width=10, command=save_data).place(x=180, y=450)

tk.Button(root, text="Update", bg="green", fg="white",
          width=10, command=update_data).place(x=300, y=450)

tk.Button(root, text="Delete", bg="red", fg="white",
          width=10, command=delete_data).place(x=420, y=450)

tk.Button(root, text="Clear", bg="gray", fg="white",
          width=10, command=clear_data).place(x=540, y=450)

# Right search section
tk.Label(root, text="Course Name", font=("Times New Roman", 16), bg="white").place(x=700, y=80)

search_entry = tk.Entry(root, width=20)
search_entry.place(x=860, y=85)

tk.Button(root, text="Search", bg="deepskyblue", fg="white",
          width=10).place(x=1000, y=82)

# Table
columns = ("Course", "Duration", "Charges")
tree = ttk.Treeview(root, columns=columns, show="headings", height=15)

for col in columns:
    tree.heading(col, text=col)
    tree.column(col, width=150)

tree.place(x=700, y=130)

root.mainloop()