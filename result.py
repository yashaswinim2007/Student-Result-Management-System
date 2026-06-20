from tkinter import *
from tkinter import ttk, messagebox
import sqlite3

class resultClass:
    def __init__(self, root):
        self.root = root
        
        # This frame attaches directly to the dashboard's main workspace area
        self.main_frame = Frame(self.root, bg="white", bd=2, relief="ridge")
        self.main_frame.place(x=340, y=120, width=980, height=500)

        # Database Connection
        self.con = sqlite3.connect("database.db")
        self.cur = self.con.cursor()
        self.create_table()

        # --- GUI Elements ---
        title = Label(
            self.main_frame,
            text="Add Student Result",
            font=("Arial", 22, "bold"),
            bg="orange",
            fg="white"
        )
        title.pack(fill=X, pady=10)

        # Sub-container frame to center form components elegantly
        form_frame = Frame(self.main_frame, bg="white")
        form_frame.pack(pady=25)

        Label(form_frame, text="Roll No", font=("Arial", 13), bg="white").grid(row=0, column=0, pady=12, sticky="w", padx=10)
        self.txt_roll = Entry(form_frame, width=30, font=("Arial", 12), bd=2, relief="groove")
        self.txt_roll.grid(row=0, column=1, pady=12)

        Label(form_frame, text="Name", font=("Arial", 13), bg="white").grid(row=1, column=0, pady=12, sticky="w", padx=10)
        self.txt_name = Entry(form_frame, width=30, font=("Arial", 12), bd=2, relief="groove")
        self.txt_name.grid(row=1, column=1, pady=12)

        Label(form_frame, text="Course", font=("Arial", 13), bg="white").grid(row=2, column=0, pady=12, sticky="w", padx=10)
        self.txt_course = Entry(form_frame, width=30, font=("Arial", 12), bd=2, relief="groove")
        self.txt_course.grid(row=2, column=1, pady=12)

        Label(form_frame, text="Marks Obtained", font=("Arial", 13), bg="white").grid(row=3, column=0, pady=12, sticky="w", padx=10)
        self.txt_marks = Entry(form_frame, width=30, font=("Arial", 12), bd=2, relief="groove")
        self.txt_marks.grid(row=3, column=1, pady=12)

        Label(form_frame, text="Full Marks", font=("Arial", 13), bg="white").grid(row=4, column=0, pady=12, sticky="w", padx=10)
        self.txt_full = Entry(form_frame, width=30, font=("Arial", 12), bd=2, relief="groove")
        self.txt_full.grid(row=4, column=1, pady=12)

        # Button row alignment
        btn_frame = Frame(form_frame, bg="white")
        btn_frame.grid(row=5, columnspan=2, pady=20)

        Button(
            btn_frame,
            text="Submit",
            bg="green",
            fg="white",
            font=("Arial", 11, "bold"),
            width=13,
            cursor="hand2",
            command=self.save_result
        ).pack(side=LEFT, padx=10)

        Button(
            btn_frame,
            text="Clear",
            bg="red",
            fg="white",
            font=("Arial", 11, "bold"),
            width=13,
            cursor="hand2",
            command=self.clear
        ).pack(side=LEFT, padx=10)

    def create_table(self):
        self.cur.execute("""
        CREATE TABLE IF NOT EXISTS result(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        roll_no TEXT,
        name TEXT,
        course TEXT,
        marks_obtained INTEGER,
        full_marks INTEGER,
        percentage REAL
        )
        """)
        self.con.commit()

    def save_result(self):
        roll = self.txt_roll.get()
        name = self.txt_name.get()
        course = self.txt_course.get()
        marks = self.txt_marks.get()
        full = self.txt_full.get()

        if roll == "" or name == "" or marks == "" or full == "":
            messagebox.showerror("Error", "All fields are required", parent=self.main_frame)
            return

        try:
            percentage = round((int(marks) / int(full)) * 100, 2)
        except ZeroDivisionError:
            messagebox.showerror("Error", "Full marks cannot be zero", parent=self.main_frame)
            return
        except ValueError:
            messagebox.showerror("Error", "Marks must be valid numbers", parent=self.main_frame)
            return

        self.cur.execute(
            """
            INSERT INTO result
            (roll_no,name,course,marks_obtained,full_marks,percentage)
            VALUES(?,?,?,?,?,?)
            """,
            (roll, name, course, marks, full, percentage)
        )
        self.con.commit()

        messagebox.showinfo(
            "Success",
            f"Result Saved\nPercentage = {percentage}%",
            parent=self.main_frame
        )
        self.clear()

    def clear(self):
        self.txt_roll.delete(0, END)
        self.txt_name.delete(0, END)
        self.txt_course.delete(0, END)
        self.txt_marks.delete(0, END)
        self.txt_full.delete(0, END)