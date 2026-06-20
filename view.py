from tkinter import *
from tkinter import ttk, messagebox
import sqlite3

class viewClass:
    def __init__(self, root):
        self.root = root
        
        # Fits exactly inside the dashboard workspace coordinates
        self.main_frame = Frame(self.root, bg="white", bd=2, relief="ridge")
        self.main_frame.place(x=340, y=120, width=980, height=500)

        # Database Connection
        self.con = sqlite3.connect("database.db")
        self.cur = self.con.cursor()

        # --- GUI Title ---
        title = Label(
            self.main_frame,
            text="View Student Results",
            font=("Goudy Old Style", 22, "bold"),
            bg="#e67e22",
            fg="white"
        )
        title.pack(fill=X, pady=10)

        # --- Search Controls Area ---
        search_frame = Frame(self.main_frame, bg="white")
        search_frame.pack(pady=15)

        Label(
            search_frame, 
            text="Search By | Roll No.", 
            font=("Arial", 13, "bold"), 
            bg="white"
        ).grid(row=0, column=0, padx=10)
        
        self.var_search = StringVar()
        txt_search = Entry(
            search_frame, 
            textvariable=self.var_search, 
            font=("Arial", 12), 
            width=25, 
            bg="#f5f6fa", 
            bd=2, 
            relief="groove"
        )
        txt_search.grid(row=0, column=1, padx=10)

        Button(
            search_frame, 
            text="Search", 
            command=self.search_result, 
            bg="#2980b9", 
            fg="white", 
            font=("Arial", 11, "bold"), 
            width=12, 
            cursor="hand2"
        ).grid(row=0, column=2, padx=10)
        
        Button(
            search_frame, 
            text="Clear", 
            command=self.clear, 
            bg="#7f8c8d", 
            fg="white", 
            font=("Arial", 11, "bold"), 
            width=12, 
            cursor="hand2"
        ).grid(row=0, column=3, padx=10)

        # --- Treeview Data Table Frame ---
        table_frame = Frame(self.main_frame, bg="white")
        table_frame.pack(fill=BOTH, expand=True, padx=20, pady=10)

        scroll_y = Scrollbar(table_frame, orient=VERTICAL)
        scroll_x = Scrollbar(table_frame, orient=HORIZONTAL)

        # Configuring columns to look exactly like your screenshot
        self.ResultTable = ttk.Treeview(
            table_frame, 
            columns=("roll", "name", "course", "marks", "full", "per"), 
            xscrollcommand=scroll_x.set, 
            yscrollcommand=scroll_y.set
        )
        
        scroll_y.pack(side=RIGHT, fill=Y)
        scroll_x.pack(side=BOTTOM, fill=X)
        scroll_y.config(command=self.ResultTable.yview)
        scroll_x.config(command=self.ResultTable.xview)

        self.ResultTable.heading("roll", text="Roll No")
        self.ResultTable.heading("name", text="Name")
        self.ResultTable.heading("course", text="Course")
        self.ResultTable.heading("marks", text="Marks Obtained")
        self.ResultTable.heading("full", text="Total Marks")
        self.ResultTable.heading("per", text="Percentage")
        self.ResultTable['show'] = 'headings'

        # Set column widths
        self.ResultTable.column("roll", width=100, anchor=CENTER)
        self.ResultTable.column("name", width=150, anchor=CENTER)
        self.ResultTable.column("course", width=120, anchor=CENTER)
        self.ResultTable.column("marks", width=120, anchor=CENTER)
        self.ResultTable.column("full", width=120, anchor=CENTER)
        self.ResultTable.column("per", width=100, anchor=CENTER)

        self.ResultTable.pack(fill=BOTH, expand=True)

        # --- Delete Records Action ---
        Button(
            self.main_frame, 
            text="Delete", 
            command=self.delete_result, 
            bg="#c0392b", 
            fg="white", 
            font=("Arial", 12, "bold"), 
            width=15, 
            cursor="hand2"
        ).pack(pady=15)

        self.show_all_results()

    # --- Database Core Operations ---
    def show_all_results(self):
        """Fetches and renders all saved rows onto the grid platform."""
        self.ResultTable.delete(*self.ResultTable.get_children())
        try:
            self.cur.execute("SELECT roll_no, name, course, marks_obtained, full_marks, percentage FROM result")
            rows = self.cur.fetchall()
            for row in rows:
                self.ResultTable.insert('', END, values=row)
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.main_frame)

    def search_result(self):
        """Filters rows to pinpoint a specific student record entry matching the roll input."""
        if self.var_search.get() == "":
            messagebox.showerror("Error", "Roll No. is required for filtering records", parent=self.main_frame)
            return
        
        try:
            self.cur.execute("SELECT roll_no, name, course, marks_obtained, full_marks, percentage FROM result WHERE roll_no=?", (self.var_search.get(),))
            row = self.cur.fetchone()
            if row is not None:
                self.ResultTable.delete(*self.ResultTable.get_children())
                self.ResultTable.insert('', END, values=row)
            else:
                messagebox.showinfo("No Match", "No records found matching this Roll Number", parent=self.main_frame)
        except Exception as ex:
            messagebox.showerror("Error", f"Search error occurred: {str(ex)}", parent=self.main_frame)

    def delete_result(self):
        """Deletes the highlighted record target."""
        focus_row = self.ResultTable.focus()
        if not focus_row:
            messagebox.showerror("Selection Error", "Please select a student row from the table to delete", parent=self.main_frame)
            return
        
        row_content = self.ResultTable.item(focus_row)
        roll_num = row_content['values'][0]

        confirm = messagebox.askyesno("Confirm Delete", f"Are you sure you want to permanently drop Roll No: {roll_num}?", parent=self.main_frame)
        if confirm:
            try:
                self.cur.execute("DELETE FROM result WHERE roll_no=?", (roll_num,))
                self.con.commit()
                messagebox.showinfo("Deleted", "Student result dropped successfully", parent=self.main_frame)
                self.clear()
            except Exception as ex:
                messagebox.showerror("Error", f"Deletion task failed: {str(ex)}", parent=self.main_frame)

    def clear(self):
        self.var_search.set("")
        self.show_all_results()