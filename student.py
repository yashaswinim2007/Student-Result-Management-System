import sqlite3
import tkinter as tk
from tkinter import messagebox, ttk

# DO NOT import student_Class here. The class definition starts directly below:
class student_Class:

    def __init__(self, root):
        self.root = tk.Toplevel(root)
        self.root.title("Student Result Management System")
        self.root.geometry("1150x650+150+80")
        self.root.configure(bg="white")

        # Focus user interaction on this window
        self.root.grab_set()

        # Database initialization
        self.init_db()

        # --- Window Header Title ---
        title = tk.Label(
            self.root,
            text="Manage Student Details",
            bg="#03a9f4",
            fg="white",
            font=("Times New Roman", 20, "bold"),
        )
        title.pack(fill="x", pady=10)

        # --- Variables ---
        self.var_roll = tk.StringVar()
        self.var_name = tk.StringVar()
        self.var_email = tk.StringVar()
        self.var_gender = tk.StringVar()
        self.var_dob = tk.StringVar()
        self.var_contact = tk.StringVar()
        self.var_course = tk.StringVar()
        self.var_a_date = tk.StringVar()
        self.var_state = tk.StringVar()
        self.var_city = tk.StringVar()
        self.var_pin = tk.StringVar()
        self.var_search = tk.StringVar()

        # --- Form Layout Fields ---
        # Row 1
        tk.Label(self.root, text="Roll No.", font=("Times New Roman", 12, "bold"), bg="white").place(x=20, y=70)
        tk.Entry(self.root, textvariable=self.var_roll, font=("Arial", 11), bg="lightyellow").place(x=120, y=70, width=150)

        tk.Label(self.root, text="D.O.B(dd-mm-yyyy)", font=("Times New Roman", 12, "bold"), bg="white").place(x=300, y=70)
        tk.Entry(self.root, textvariable=self.var_dob, font=("Arial", 11), bg="lightyellow").place(x=450, y=70, width=150)

        # Row 2
        tk.Label(self.root, text="Name", font=("Times New Roman", 12, "bold"), bg="white").place(x=20, y=110)
        tk.Entry(self.root, textvariable=self.var_name, font=("Arial", 11), bg="lightyellow").place(x=120, y=110, width=150)

        tk.Label(self.root, text="Contact No.", font=("Times New Roman", 12, "bold"), bg="white").place(x=300, y=110)
        tk.Entry(self.root, textvariable=self.var_contact, font=("Arial", 11), bg="lightyellow").place(x=450, y=110, width=150)

        # Row 3
        tk.Label(self.root, text="Email", font=("Times New Roman", 12, "bold"), bg="white").place(x=20, y=150)
        tk.Entry(self.root, textvariable=self.var_email, font=("Arial", 11), bg="lightyellow").place(x=120, y=150, width=150)

        tk.Label(self.root, text="Select Course", font=("Times New Roman", 12, "bold"), bg="white").place(x=300, y=150)
        self.course_list = ["Select"]
        self.fetch_courses()  
        self.txt_course = ttk.Combobox(self.root, textvariable=self.var_course, values=self.course_list, font=("Arial", 11), state="readonly")
        self.txt_course.place(x=450, y=150, width=150)
        self.txt_course.current(0)

        # Row 4
        tk.Label(self.root, text="Gender", font=("Times New Roman", 12, "bold"), bg="white").place(x=20, y=190)
        self.txt_gender = ttk.Combobox(self.root, textvariable=self.var_gender, values=("Select Gender", "Male", "Female", "Other"), font=("Arial", 11), state="readonly")
        self.txt_gender.place(x=120, y=190, width=150)
        self.txt_gender.current(0)

        tk.Label(self.root, text="Admission Date", font=("Times New Roman", 12, "bold"), bg="white").place(x=300, y=190)
        tk.Entry(self.root, textvariable=self.var_a_date, font=("Arial", 11), bg="lightyellow").place(x=450, y=190, width=150)

        # Row 5 - State, City, Pin
        tk.Label(self.root, text="State", font=("Times New Roman", 12, "bold"), bg="white").place(x=20, y=230)
        tk.Entry(self.root, textvariable=self.var_state, font=("Arial", 11), bg="lightyellow").place(x=70, y=230, width=100)

        tk.Label(self.root, text="City", font=("Times New Roman", 12, "bold"), bg="white").place(x=185, y=230)
        tk.Entry(self.root, textvariable=self.var_city, font=("Arial", 11), bg="lightyellow").place(x=225, y=230, width=100)

        tk.Label(self.root, text="Pin Code", font=("Times New Roman", 12, "bold"), bg="white").place(x=340, y=230)
        tk.Entry(self.root, textvariable=self.var_pin, font=("Arial", 11), bg="lightyellow").place(x=420, y=230, width=100)

        # Row 6 - Address
        tk.Label(self.root, text="Address", font=("Times New Roman", 12, "bold"), bg="white").place(x=20, y=270)
        self.txt_address = tk.Text(self.root, font=("Arial", 11), bg="lightyellow")
        self.txt_address.place(x=120, y=270, width=480, height=80)

        # --- Form Operational Action Buttons ---
        tk.Button(self.root, text="Save", bg="dodgerblue", fg="white", width=10, font=("Arial", 10, "bold"), command=self.save_data).place(x=120, y=380)
        tk.Button(self.root, text="Update", bg="green", fg="white", width=10, font=("Arial", 10, "bold"), command=self.update_data).place(x=230, y=380)
        tk.Button(self.root, text="Delete", bg="red", fg="white", width=10, font=("Arial", 10, "bold"), command=self.delete_data).place(x=340, y=380)
        tk.Button(self.root, text="Clear", bg="gray", fg="white", width=10, font=("Arial", 10, "bold"), command=self.clear_data).place(x=450, y=380)

        # --- Search Block Frame Section ---
        tk.Label(self.root, text="Search | Roll No.", font=("Times New Roman", 12, "bold"), bg="white").place(x=640, y=70)
        tk.Entry(self.root, textvariable=self.var_search, font=("Arial", 11)).place(x=780, y=70, width=140)
        tk.Button(self.root, text="Search", bg="deepskyblue", fg="white", font=("Arial", 9, "bold"), command=self.search_data).place(x=930, y=68, width=80)

        # --- Table Viewer (Treeview Component Layout) ---
        columns = ("Roll No.", "Name", "Email", "Gender", "D.O.B", "Contact", "Course")
        self.tree = ttk.Treeview(self.root, columns=columns, show="headings")
        
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=90, anchor="center")

        self.tree.place(x=640, y=110, width=480, height=480)
        self.tree.bind("<ButtonRelease-1>", self.get_data)

        self.fetch_data()

    # ---------------- BACKEND QUERIES ---------------- #

    def init_db(self):
        con = sqlite3.connect(database="rms.db")
        cur = con.cursor()
        try:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS student(
                    roll TEXT PRIMARY KEY,
                    name TEXT,
                    email TEXT,
                    gender TEXT,
                    dob TEXT,
                    contact TEXT,
                    course TEXT,
                    admission TEXT,
                    state TEXT,
                    city TEXT,
                    pin TEXT,
                    address TEXT
                )
            """)
            con.commit()
        except Exception as ex:
            print(f"Database Init Error: {ex}")
        finally:
            con.close()

    def fetch_courses(self):
        con = sqlite3.connect(database="rms.db")
        cur = con.cursor()
        try:
            cur.execute("SELECT name FROM course")
            rows = cur.fetchall()
            if len(rows) > 0:
                for row in rows:
                    self.course_list.append(row[0])
        except Exception as ex:
            print(ex)
        finally:
            con.close()

    def save_data(self):
        if self.var_roll.get().strip() == "" or self.var_name.get().strip() == "":
            messagebox.showerror("Error", "Roll No. and Name are mandatory!", parent=self.root)
            return

        con = sqlite3.connect(database="rms.db")
        cur = con.cursor()
        try:
            cur.execute("SELECT * FROM student WHERE roll=?", (self.var_roll.get().strip(),))
            if cur.fetchone() is not None:
                messagebox.showerror("Error", "Roll Number already mapped!", parent=self.root)
                return

            cur.execute("""
                INSERT INTO student (roll, name, email, gender, dob, contact, course, admission, state, city, pin, address)
                VALUES(?,?,?,?,?,?,?,?,?,?,?,?)
            """, (
                self.var_roll.get().strip(),
                self.var_name.get().strip(),
                self.var_email.get().strip(),
                self.var_gender.get(),
                self.var_dob.get().strip(),
                self.var_contact.get().strip(),
                self.var_course.get(),
                self.var_a_date.get().strip(),
                self.var_state.get().strip(),
                self.var_city.get().strip(),
                self.var_pin.get().strip(),
                self.txt_address.get("1.0", "end-1c").strip()
            ))
            con.commit()
            messagebox.showinfo("Success", "Student Added Successfully", parent=self.root)
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
            cur.execute("SELECT roll, name, email, gender, dob, contact, course, admission, state, city, pin, address FROM student")
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
                self.var_roll.set(values[0])
                self.var_name.set(values[1])
                self.var_email.set(values[2])
                self.var_gender.set(values[3])
                self.var_dob.set(values[4])
                self.var_contact.set(values[5])
                self.var_course.set(values[6])
                self.var_a_date.set(values[7])
                self.var_state.set(values[8])
                self.var_city.set(values[9])
                self.var_pin.set(values[10])
                self.txt_address.delete("1.0", tk.END)
                self.txt_address.insert("1.0", values[11])

    def update_data(self):
        selected = self.tree.focus()
        if not selected:
            messagebox.showerror("Error", "Select a student from the table first", parent=self.root)
            return

        con = sqlite3.connect(database="rms.db")
        cur = con.cursor()
        try:
            cur.execute("""
                UPDATE student SET name=?, email=?, gender=?, dob=?, contact=?, course=?, admission=?, state=?, city=?, pin=?, address=? 
                WHERE roll=?
            """, (
                self.var_name.get().strip(),
                self.var_email.get().strip(),
                self.var_gender.get(),
                self.var_dob.get().strip(),
                self.var_contact.get().strip(),
                self.var_course.get(),
                self.var_a_date.get().strip(),
                self.var_state.get().strip(),
                self.var_city.get().strip(),
                self.var_pin.get().strip(),
                self.txt_address.get("1.0", "end-1c").strip(),
                self.var_roll.get().strip()
            ))
            con.commit()
            messagebox.showinfo("Success", "Student records updated", parent=self.root)
            self.fetch_data()
            self.clear_data()
        except Exception as ex:
            messagebox.showerror("Error", str(ex), parent=self.root)
        finally:
            con.close()

    def delete_data(self):
        selected = self.tree.focus()
        if not selected:
            messagebox.showerror("Error", "Select a student from the table first", parent=self.root)
            return

        if messagebox.askyesno("Confirm", "Do you really want to remove this record?", parent=self.root):
            con = sqlite3.connect(database="rms.db")
            cur = con.cursor()
            try:
                cur.execute("DELETE FROM student WHERE roll=?", (self.var_roll.get().strip(),))
                con.commit()
                messagebox.showinfo("Success", "Record dropped successfully", parent=self.root)
                self.fetch_data()
                self.clear_data()
            except Exception as ex:
                messagebox.showerror("Error", str(ex), parent=self.root)
            finally:
                con.close()

    def clear_data(self):
        self.var_roll.set("")
        self.var_name.set("")
        self.var_email.set("")
        self.var_gender.set("Select Gender")
        self.var_dob.set("")
        self.var_contact.set("")
        self.var_course.set("Select")
        self.var_a_date.set("")
        self.var_state.set("")
        self.var_city.set("")
        self.var_pin.set("")
        self.txt_address.delete("1.0", tk.END)
        self.var_search.set("")
        self.fetch_data()

    def search_data(self):
        query = self.var_search.get().strip()
        if not query:
            messagebox.showerror("Input Error", "Enter a roll number to look up", parent=self.root)
            return

        con = sqlite3.connect(database="rms.db")
        cur = con.cursor()
        try:
            cur.execute("SELECT roll, name, email, gender, dob, contact, course, admission, state, city, pin, address FROM student WHERE roll LIKE ?", (f"%{query}%",))
            rows = cur.fetchall()

            self.tree.delete(*self.tree.get_children())
            if rows:
                for row in rows:
                    self.tree.insert("", "end", values=row)
            else:
                messagebox.showinfo("Result", "No matching student profiles found.", parent=self.root)
        except Exception as ex:
            messagebox.showerror("Search Error", str(ex), parent=self.root)
        finally:
            con.close()