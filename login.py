import sys
import tkinter as tk
from tkinter import messagebox
from dashboard import RMSDashboard  # Imports your dashboard class

class LoginSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("Login System - Student Result Management System")
        self.root.geometry("1350x700+0+0")
        self.root.configure(bg="#0f2027")

        # --- Dual-Tone Background Design ---
        left_bg = tk.Frame(self.root, bg="#03a9f4", width=500, height=700)
        left_bg.place(x=0, y=0)
        
        right_bg = tk.Frame(self.root, bg="#263238", width=850, height=700)
        right_bg.place(x=500, y=0)

        # --- Left Panel Side: Clock / Title Showcase ---
        clock_frame = tk.Frame(left_bg, bg="#111", bd=5, relief="ridge")
        clock_frame.place(x=100, y=150, width=300, height=380)

        lbl_clock_title = tk.Label(
            clock_frame,
            text="WebCode Clock",
            font=("Arial", 18, "bold"),
            bg="#111",
            fg="white"
        )
        lbl_clock_title.pack(pady=20)

        canvas_clock = tk.Canvas(
            clock_frame, width=160, height=160, bg="#111", highlightthickness=0
        )
        canvas_clock.pack(pady=10)
        canvas_clock.create_oval(10, 10, 150, 150, outline="white", width=4)
        canvas_clock.create_line(80, 80, 80, 40, fill="yellow", width=3)   # Hour Hand
        canvas_clock.create_line(80, 80, 115, 80, fill="green", width=2)  # Minute Hand
        canvas_clock.create_line(80, 80, 50, 100, fill="red", width=1)    # Second Hand

        # --- Right Panel Side: Floating Login Box Container ---
        login_frame = tk.Frame(self.root, bg="white", bd=2, relief="groove")
        login_frame.place(x=450, y=120, width=550, height=440)

        title = tk.Label(
            login_frame,
            text="LOGIN HERE",
            font=("Goudy Old Style", 24, "bold"),
            bg="white",
            fg="#009688"
        )
        title.place(x=40, y=40)

        # Email Input Field
        lbl_email = tk.Label(
            login_frame,
            text="EMAIL ADDRESS",
            font=("Goudy Old Style", 12, "bold"),
            bg="white",
            fg="gray"
        )
        lbl_email.place(x=40, y=120)
        
        self.txt_email = tk.Entry(
            login_frame,
            font=("Arial", 12),
            bg="#eaeded",
            bd=0
        )
        self.txt_email.place(x=40, y=150, width=450, height=35)

        # Password Input Field
        lbl_password = tk.Label(
            login_frame,
            text="PASSWORD",
            font=("Goudy Old Style", 12, "bold"),
            bg="white",
            fg="gray"
        )
        lbl_password.place(x=40, y=210)
        
        self.txt_password = tk.Entry(
            login_frame,
            font=("Arial", 12),
            bg="#eaeded",
            bd=0,
            show="*"
        )
        self.txt_password.place(x=40, y=240, width=450, height=35)

        # Links
        btn_reg = tk.Button(
            login_frame, text="Register new Account?", font=("Arial", 9), bg="white", fg="red", bd=0, activebackground="white", cursor="hand2"
        )
        btn_reg.place(x=40, y=290)

        btn_forget = tk.Button(
            login_frame, text="Forget Password?", font=("Arial", 9), bg="white", fg="red", bd=0, activebackground="white", cursor="hand2"
        )
        btn_forget.place(x=380, y=290)

        # Actions Button Trigger
        btn_login = tk.Button(
            login_frame,
            text="Login",
            command=self.login_action,
            bg="#d32f2f",
            fg="white",
            font=("Arial", 13, "bold"),
            bd=0,
            cursor="hand2"
        )
        btn_login.place(x=40, y=340, width=150, height=40)

        # --- Lower App Footer bar ---
        footer = tk.Label(
            self.root,
            text="ProjectName: Student Result Management System  |  Email Us: WebCode867@gmail.com",
            font=("Arial", 10),
            bg="#111",
            fg="white",
            pady=8
        )
        footer.pack(side="bottom", fill="x")

    def login_action(self):
        """Validates credentials. Default credentials set to admin/admin."""
        email = self.txt_email.get()
        password = self.txt_password.get()

        if email == "" or password == "":
            messagebox.showerror("Error", "All entry fields are required!", parent=self.root)
        elif email == "admin" and password == "admin":
            messagebox.showinfo("Success", f"Welcome Back!\nLogin Successful.", parent=self.root)
            
            # Hide the Login window, open Dashboard window cleanly
            self.root.withdraw()
            self.new_root = tk.Toplevel()
            # Pass our login root reference down to handle logouts properly
            self.dashboard_app = RMSDashboard(self.new_root, login_window=self.root)
        else:
            messagebox.showerror("Access Denied", "Invalid Email Address or Password!", parent=self.root)