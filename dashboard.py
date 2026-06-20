import sys
import tkinter as tk
from tkinter import messagebox
import sqlite3  # <--- Added for live database connectivity

# Safely importing your sub-module view layouts:
try:
    from course import course_Class
except ImportError:
    course_Class = None

try:
    from student import student_Class
except ImportError:
    student_Class = None

from result import resultClass  
from view import viewClass  


class RMSDashboard:
    def __init__(self, root):
        self.root = root
        self.root.title("Student Result Management System")
        self.root.geometry("1350x700+0+0")
        self.root.configure(bg="#f4f6f9")

        # --- STEP 1: CREATE THE LOGIN SCREEN FIRST ---
        self.show_login_screen()

    def show_login_screen(self):
        """This builds the login interface shown in your image"""
        for widget in self.root.winfo_children():
            widget.destroy()

        self.root.configure(bg="#0f2027")

        # Split background colors (Left teal, Right dark blue)
        left_bg = tk.Frame(self.root, bg="#03a9f4", width=500, height=700)
        left_bg.place(x=0, y=0)
        
        right_bg = tk.Frame(self.root, bg="#263238", width=850, height=700)
        right_bg.place(x=500, y=0)

        # Left Clock Box
        clock_frame = tk.Frame(left_bg, bg="#111", bd=5, relief="ridge")
        clock_frame.place(x=100, y=150, width=300, height=380)

        tk.Label(clock_frame, text="WebCode Clock", font=("Arial", 18, "bold"), bg="#111", fg="white").pack(pady=20)
        canvas_clock = tk.Canvas(clock_frame, width=140, height=140, bg="#111", highlightthickness=0)
        canvas_clock.pack(pady=10)
        canvas_clock.create_oval(10, 10, 130, 130, outline="white", width=4)
        canvas_clock.create_line(70, 70, 70, 40, fill="yellow", width=3)
        canvas_clock.create_line(70, 70, 100, 70, fill="green", width=2)

        # Right White Login Box
        login_frame = tk.Frame(self.root, bg="white", bd=2, relief="groove")
        login_frame.place(x=550, y=150, width=500, height=400)

        tk.Label(login_frame, text="LOGIN HERE", font=("Goudy Old Style", 24, "bold"), bg="white", fg="#009688").place(x=40, y=30)

        # Input fields
        tk.Label(login_frame, text="EMAIL ADDRESS", font=("Goudy Old Style", 11, "bold"), bg="white", fg="gray").place(x=40, y=100)
        self.txt_email = tk.Entry(login_frame, font=("Arial", 12), bg="#eaeded", bd=0)
        self.txt_email.place(x=40, y=130, width=420, height=35)

        tk.Label(login_frame, text="PASSWORD", font=("Goudy Old Style", 11, "bold"), bg="white", fg="gray").place(x=40, y=190)
        self.txt_password = tk.Entry(login_frame, font=("Arial", 12), bg="#eaeded", bd=0, show="*")
        self.txt_password.place(x=40, y=220, width=420, height=35)

        # Login Button
        btn_login = tk.Button(
            login_frame, text="Login", font=("Arial", 13, "bold"),
            bg="#d32f2f", fg="white", bd=0, cursor="hand2",
            command=self.check_login
        )
        btn_login.place(x=40, y=300, width=150, height=40)

    def check_login(self):
        email = self.txt_email.get()
        password = self.txt_password.get()

        if email == "admin" and password == "admin":
            messagebox.showinfo("Success", "Login Successful!")
            self.show_main_dashboard() 
        else:
            messagebox.showerror("Error", "Use username 'admin' and password 'admin'")

    # --- STEP 2: CREATE THE MAIN DASHBOARD VIEW ---
    def show_main_dashboard(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        self.root.configure(bg="#f4f6f9")
        self.active_window = None

        # --- Top Blue Header Bar ---
        title = tk.Label(self.root, text="Student Result Management System", font=("Goudy Old Style", 26, "bold"), bg="#0b5377", fg="white", pady=15)
        title.pack(fill="x")

        # --- Top Menu Buttons ---
        menu_frame = tk.Frame(self.root, bg="#0b5377", padx=10, pady=5)
        menu_frame.pack(fill="x")

        tk.Button(menu_frame, text="Course", font=("Goudy Old Style", 14, "bold"), bg="#03a9f4", fg="white", width=12, cursor="hand2", command=self.open_course).pack(side="left", padx=10)
        tk.Button(menu_frame, text="Student", font=("Goudy Old Style", 14, "bold"), bg="#03a9f4", fg="white", width=12, cursor="hand2", command=self.open_student).pack(side="left", padx=10)
        tk.Button(menu_frame, text="Result", font=("Goudy Old Style", 14, "bold"), bg="#03a9f4", fg="white", width=12, cursor="hand2", command=self.open_result).pack(side="left", padx=10)
        tk.Button(menu_frame, text="View Student Result", font=("Goudy Old Style", 14, "bold"), bg="#03a9f4", fg="white", width=16, cursor="hand2", command=self.open_view).pack(side="left", padx=10)
        tk.Button(menu_frame, text="Logout", font=("Goudy Old Style", 14, "bold"), bg="#03a9f4", fg="white", width=12, cursor="hand2", command=self.logout_action).pack(side="left", padx=10)
        tk.Button(menu_frame, text="Exit", font=("Goudy Old Style", 14, "bold"), bg="#03a9f4", fg="white", width=12, cursor="hand2", command=self.exit_action).pack(side="left", padx=10)

        # --- Left Panel Side (Clock) ---
        left_panel = tk.Frame(self.root, bg="#263238", width=240, height=520)
        left_panel.place(x=20, y=120)
        tk.Label(left_panel, text="Analog Clock", font=("Arial", 16, "bold"), bg="#263238", fg="white").place(x=50, y=20)
        
        canvas_clock = tk.Canvas(left_panel, width=140, height=140, bg="#263238", highlightthickness=0)
        canvas_clock.place(x=50, y=80)
        canvas_clock.create_oval(10, 10, 130, 130, outline="white", width=4)
        canvas_clock.create_line(70, 70, 70, 35, fill="white", width=3)
        canvas_clock.create_line(70, 70, 100, 70, fill="white", width=2)

        # --- Central Body Workspace Container ---
        self.home_elements = {}
        self.home_elements['title'] = tk.Label(self.root, text="Student Management System Dashboard", font=("Goudy Old Style", 20), bg="#f4f6f9", fg="#263238")
        self.home_elements['title'].place(x=500, y=220)

        # Total Students Box
        self.lbl_students = tk.Label(self.root, text="Total Students\n[ 0 ]", font=("Goudy Old Style", 15, "bold"), bg="#e53935", fg="white", bd=4, relief="ridge", width=18, pady=12)
        self.lbl_students.place(x=380, y=420)
        self.home_elements['students'] = self.lbl_students

        # Total Course Box
        self.lbl_courses = tk.Label(self.root, text="Total Course\n[ 0 ]", font=("Goudy Old Style", 15, "bold"), bg="#1e88e5", fg="white", bd=4, relief="ridge", width=18, pady=12)
        self.lbl_courses.place(x=660, y=420)
        self.home_elements['courses'] = self.lbl_courses

        # Total Results Box
        self.lbl_results = tk.Label(self.root, text="Total Results\n[ 0 ]", font=("Goudy Old Style", 15, "bold"), bg="#43a047", fg="white", bd=4, relief="ridge", width=18, pady=12)
        self.lbl_results.place(x=940, y=420)
        self.home_elements['results'] = self.lbl_results

        footer = tk.Label(self.root, text="SRMS - Student Result Management System", font=("Arial", 11), bg="#263238", fg="white")
        footer.pack(side="bottom", fill="x")

        # Call the update function to fetch database totals immediately!
        self.update_counts_from_database()

    def update_counts_from_database(self):
        """Fetches the actual real-time count of students, courses, and results from your SQL database"""
        try:
            con = sqlite3.connect("database.db")
            cur = con.cursor()

            # 1. Fetch Students count (Assumed table name is 'student')
            try:
                cur.execute("SELECT COUNT(*) FROM student")
                student_count = cur.fetchone()[0]
                self.lbl_students.config(text=f"Total Students\n[ {student_count} ]")
            except Exception:
                self.lbl_students.config(text="Total Students\n[ 0 ]")

            # 2. Fetch Courses count (Assumed table name is 'course')
            try:
                cur.execute("SELECT COUNT(*) FROM course")
                course_count = cur.fetchone()[0]
                self.lbl_courses.config(text=f"Total Course\n[ {course_count} ]")
            except Exception:
                self.lbl_courses.config(text="Total Course\n[ 0 ]")

            # 3. Fetch Results count (Table name is 'result')
            try:
                cur.execute("SELECT COUNT(*) FROM result")
                result_count = cur.fetchone()[0]
                self.lbl_results.config(text=f"Total Results\n[ {result_count} ]")
            except Exception:
                self.lbl_results.config(text="Total Results\n[ 0 ]")

            con.close()
        except Exception as ex:
            messagebox.showerror("Error", f"Error updating counts: {str(ex)}")

    def clear_workspace(self):
        for element in self.home_elements.values():
            element.place_forget()
        if hasattr(self, 'active_window') and self.active_window and hasattr(self.active_window, 'main_frame'):
            self.active_window.main_frame.destroy()

    # Button Redirections
    def open_course(self):
        if course_Class:
            self.clear_workspace()
            self.active_window = course_Class(self.root)

    def open_student(self):
        if student_Class:
            self.clear_workspace()
            self.active_window = student_Class(self.root)

    def open_result(self):
        self.clear_workspace()
        self.active_window = resultClass(self.root)

    def open_view(self):
        self.clear_workspace()
        self.active_window = viewClass(self.root)

    def logout_action(self):
        if messagebox.askyesno("Logout", "Are you sure you want to log out?"):
            self.show_login_screen()

    def exit_action(self):
        if messagebox.askyesno("Exit System", "Do you really want to close the app?"):
            self.root.destroy()
            sys.exit()


if __name__ == "__main__":
    root = tk.Tk()
    obj = RMSDashboard(root)
    root.mainloop()