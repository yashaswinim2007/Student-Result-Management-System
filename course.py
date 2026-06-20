import sqlite3
import tkinter as tk
from tkinter import messagebox, ttk


class course_Class:

    def __init__(self, root):
        # Create a Toplevel child window instead of a new tk.Tk() instance
        self.root = tk.Toplevel(root)
        self.root.title("Student Result Management System")
        self.root.geometry("1150x650+150+80")
        self.root.configure(bg="white")

        # Focus focus on this window
        self.root.grab_set()

        # Database connection/initialization
        self.init_db()

        # --- Window Header Title ---
        title = tk.Label(
            self.root,
            text="Manage Course Details",
            bg="darkblue",
            fg="white",
            font=("Times New Roman", 24, "bold"),
        )
        title.pack(fill="x", pady=10)

        # --- Input Fields Form ---
        tk.Label(
            self.root, text="Course Name", font=("Times New Roman", 16), bg="white"
        ).place(x=20, y=80)
        self.entry_course = tk.Entry(self.root, width=30, font=("Arial", 12))
        self.entry_course.place(x=200, y=85)

        tk.Label(
            self.root, text="Duration", font=("Times New Roman", 16), bg="white"
        ).place(x=20, y=140)
        self.entry_duration = tk.Entry(self.root, width=30, font=("Arial", 12))
        self.entry_duration.place(x=200, y=145)

        tk.Label(
            self.root, text="Charges", font=("Times New Roman", 16), bg="white"
        ).place(x=20, y=200)
        self.entry_charges = tk.Entry(self.root, width=30, font=("Arial", 12))
        self.entry_charges.place(x=200, y=205)

        tk.Label(
            self.root, text="Description", font=("Times New Roman", 16), bg="white"
        ).place(x=20, y=260)
        self.txt_description = tk.Text(
            self.root, width=40, height=8, font=("Arial", 10)
        )
        self.txt_description.place(x=200, y=265)

        # --- Operation Buttons ---
        tk.Button(
            self.root,
            text="Save",
            bg="dodgerblue",
            fg="white",
            width=12,
            font=("Arial", 10, "bold"),
            command=self.save_data,
        ).place(x=180, y=500)
        tk.Button(
            self.root,
            text="Update",
            bg="green",
            fg="white",
            width=12,
            font=("Arial", 10, "bold"),
            command=self.update_data,
        ).place(x=310, y=500)
        tk.Button(
            self.root,
            text="Delete",
            bg="red",
            fg="white",
            width=12,
            font=("Arial", 10, "bold"),
            command=self.delete_data,
        ).place(x=440, y=500)
        tk.Button(
            self.root,
            text="Clear",
            bg="gray",
            fg="white",
            width=12,
            font=("Arial", 10, "bold"),
            command=self.clear_data,
        ).place(x=570, y=500)

        # --- Search Block Section ---
        tk.Label(
            self.root, text="Search Course", font=("Times New Roman", 16), bg="white"
        ).place(x=680, y=80)
        self.search_entry = tk.Entry(self.root, width=20, font=("Arial", 12))
        self.search_entry.place(x=840, y=85)

        tk.Button(
            self.root,
            text="Search",
            bg="deepskyblue",
            fg="white",
            width=10,
            font=("Arial", 9, "bold"),
            command=self.search_data,
        ).place(x=1040, y=82)

        # --- Data Table View layout ---
        columns = ("Course Name", "Duration", "Charges", "Description")
        self.tree = ttk.Treeview(
            self.root, columns=columns, show="headings", height=18
        )

        self.tree.heading("Course Name", text="Course Name")
        self.tree.column("Course Name", width=130, anchor="w")
        self.tree.heading("Duration", text="Duration")
        self.tree.column("Duration", width=80, anchor="center")
        self.tree.heading("Charges", text="Charges")
        self.tree.column("Charges", width=80, anchor="center")
        self.tree.heading("Description", text="Description")
        self.tree.column("Description", width=150, anchor="w")

        self.tree.place(x=680, y=140, width=450)
        self.tree.bind("<ButtonRelease-1>", self.get_data)

        # Auto load current entries on initialization
        self.fetch_data()

    # ---------------- FUNCTION LOGIC BLOCKS ---------------- #

    def init_db(self):
        con = sqlite3.connect(database="rms.db")
        cur = con.cursor()
        try:
            cur.execute(
                """
                CREATE TABLE IF NOT EXISTS course(
                    cid INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT UNIQUE,
                    duration TEXT,
                    charges TEXT,
                    description TEXT
                )
            """
            )
            con.commit()
        except Exception as ex:
            print(f"DB Init Error: {ex}")
        finally:
            con.close()

    def save_data(self):
        course = self.entry_course.get().strip()
        duration = self.entry_duration.get().strip()
        charges = self.entry_charges.get().strip()
        description = self.txt_description.get("1.0", "end-1c").strip()

        if course == "" or duration == "" or charges == "":
            messagebox.showerror(
                "Error", "All fields are required", parent=self.root
            )
            return

        con = sqlite3.connect(database="rms.db")
        cur = con.cursor()
        try:
            cur.execute(
                "SELECT * FROM course WHERE LOWER(name)=?", (course.lower(),)
            )
            if cur.fetchone() is not None:
                messagebox.showerror(
                    "Error", "Course Name already exists!", parent=self.root
                )
                return

            cur.execute(
                "INSERT INTO course (name, duration, charges, description) VALUES(?,?,?,?)",
                (course, duration, charges, description),
            )
            con.commit()
            messagebox.showinfo(
                "Success", "Course Added Successfully", parent=self.root
            )
            self.fetch_data()
            self.clear_data()
        except Exception as ex:
            messagebox.showerror("Error", f"Error: {ex}", parent=self.root)
        finally:
            con.close()

    def fetch_data(self):
        self.tree.delete(*self.tree.get_children())
        con = sqlite3.connect(database="rms.db")
        cur = con.cursor()
        try:
            cur.execute("SELECT name, duration, charges, description FROM course")
            for row in cur.fetchall():
                self.tree.insert("", "end", values=row)
        except Exception as ex:
            print(f"Fetch Error: {ex}")
        finally:
            con.close()

    def get_data(self, event):
        selected = self.tree.focus()
        if selected:
            values = self.tree.item(selected, "values")
            if values:
                self.entry_course.delete(0, tk.END)
                self.entry_course.insert(0, values[0])
                self.entry_duration.delete(0, tk.END)
                self.entry_duration.insert(0, values[1])
                self.entry_charges.delete(0, tk.END)
                self.entry_charges.insert(0, values[2])
                self.txt_description.delete("1.0", tk.END)
                if len(values) > 3:
                    self.txt_description.insert("1.0", values[3])

    def update_data(self):
        selected = self.tree.focus()
        if not selected:
            messagebox.showerror(
                "Error", "Select a course from the table first", parent=self.root
            )
            return

        course = self.entry_course.get().strip()
        duration = self.entry_duration.get().strip()
        charges = self.entry_charges.get().strip()
        description = self.txt_description.get("1.0", "end-1c").strip()

        con = sqlite3.connect(database="rms.db")
        cur = con.cursor()
        try:
            cur.execute(
                "UPDATE course SET duration=?, charges=?, description=? WHERE LOWER(name)=?",
                (duration, charges, description, course.lower()),
            )
            con.commit()
            messagebox.showinfo(
                "Success", "Course updated successfully", parent=self.root
            )
            self.fetch_data()
            self.clear_data()
        except Exception as ex:
            messagebox.showerror("Error", str(ex), parent=self.root)
        finally:
            con.close()

    def delete_data(self):
        selected = self.tree.focus()
        if not selected:
            messagebox.showerror(
                "Error", "Select a course from the table first", parent=self.root
            )
            return

        course = self.entry_course.get().strip()
        if messagebox.askyesno(
            "Confirm", "Do you really want to delete?", parent=self.root
        ):
            con = sqlite3.connect(database="rms.db")
            cur = con.cursor()
            try:
                cur.execute(
                    "DELETE FROM course WHERE LOWER(name)=?", (course.lower(),)
                )
                con.commit()
                messagebox.showinfo(
                    "Success", "Course deleted successfully", parent=self.root
                )
                self.fetch_data()
                self.clear_data()
            except Exception as ex:
                messagebox.showerror("Error", str(ex), parent=self.root)
            finally:
                con.close()

    def clear_data(self):
        self.entry_course.delete(0, tk.END)
        self.entry_duration.delete(0, tk.END)
        self.entry_charges.delete(0, tk.END)
        self.txt_description.delete("1.0", tk.END)
        self.search_entry.delete(0, tk.END)
        self.fetch_data()

    def search_data(self):
        query = self.search_entry.get().strip()
        if not query:
            messagebox.showerror(
                "Input Error", "Please type a course name to search", parent=self.root
            )
            return

        con = sqlite3.connect(database="rms.db")
        cur = con.cursor()
        try:
            cur.execute(
                "SELECT name, duration, charges, description FROM course WHERE LOWER(name) LIKE ?",
                (f"%{query.lower()}%",),
            )
            rows = cur.fetchall()

            self.tree.delete(*self.tree.get_children())
            if rows:
                for row in rows:
                    self.tree.insert("", "end", values=row)
            else:
                messagebox.showinfo(
                    "Result", "No matching courses found.", parent=self.root
                )
        except Exception as ex:
            messagebox.showerror("Search Error", str(ex), parent=self.root)
        finally:
            con.close()