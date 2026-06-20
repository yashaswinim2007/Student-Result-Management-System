import streamlit as st
import sqlite3

# 1. Clean browser page setup (No watermarks)
st.set_page_config(page_title="Student Result Management System", layout="wide")
st.title("🎓 Student Result Management System")
st.write("---")

# 2. Connect to your database file
conn = sqlite3.connect('database.db')
cursor = conn.cursor()

# Ensure the database structure exists
cursor.execute('''CREATE TABLE IF NOT EXISTS course 
                  (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, duration TEXT, description TEXT)''')
conn.commit()

# 3. Create the navigation menu on the left side
menu = ["Dashboard", "Manage Courses"]
choice = st.sidebar.selectbox("Navigation Menu", menu)

# --- PAGE 1: MAIN DASHBOARD ---
if choice == "Dashboard":
    st.subheader("📊 System Overview Dashboard")
    
    # Fetch live counts from your tables
    try:
        total_courses = cursor.execute("SELECT COUNT(*) FROM course").fetchone()[0]
    except:
        total_courses = 0
    
    # Display statistics cards side-by-side
    col1, col2 = st.columns(2)
    with col1:
        st.info(f"### Total Courses\n## {total_courses}")
    with col2:
        st.success("### Total Registered Students\n## 0")

# --- PAGE 2: COURSE MANAGE PAGE ---
elif choice == "Manage Courses":
    st.subheader("📝 Course Management Panel")
    
    # Clean input form for your friends or teacher to type into
    with st.form("course_form", clear_on_submit=True):
        course_name = st.text_input("Course Name")
        duration = st.text_input("Duration (e.g., 3 Months)")
        description = st.text_area("Course Description")
        submit = st.form_submit_button("Save Course Details")
        
        if submit:
            if course_name:
                cursor.execute("INSERT INTO course (name, duration, description) VALUES (?,?,?)", 
                               (course_name, duration, description))
                conn.commit()
                st.success(f"Successfully Added: {course_name}")
                st.rerun()
            else:
                st.error("Error: Course Name cannot be left blank.")

    # Display the current data table directly below the entry form
    st.write("### 🗃️ Saved Courses in Database")
    try:
        courses_data = cursor.execute("SELECT * FROM course").fetchall()
    except:
        courses_data = []
        
    if courses_data:
        # Formats the sql data into a clean web table grid
        st.dataframe(courses_data, column_config={
            0: "ID", 1: "Course Name", 2: "Duration", 3: "Description"
        }, use_container_width=True)
    else:
        st.info("The course database is currently empty.")