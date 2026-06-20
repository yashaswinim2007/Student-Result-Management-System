import streamlit as st
import sqlite3

# Clean browser page setup
st.set_page_config(page_title="Student Result Management System", layout="wide")
st.title("🎓 Student Result Management System")
st.write("---")

# Connect to your existing database file
conn = sqlite3.connect('rms.db')  # Connects to your main database
cursor = conn.cursor()

# Create tables if they don't exist yet
cursor.execute('''CREATE TABLE IF NOT EXISTS student 
                  (roll INTEGER PRIMARY KEY, name TEXT, email TEXT, gender TEXT, dob TEXT, contact TEXT, admission TEXT, course TEXT, state TEXT, city TEXT, pin TEXT, address TEXT)''')
cursor.execute('''CREATE TABLE IF NOT EXISTS result 
                  (id INTEGER PRIMARY KEY AUTOINCREMENT, roll TEXT, name TEXT, course TEXT, marks_ob TEXT, full_marks TEXT, per TEXT)''')
cursor.execute('''CREATE TABLE IF NOT EXISTS course 
                  (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, duration TEXT, description TEXT)''')
conn.commit()

# --- SIDEBAR NAVIGATION ---
menu = ["📊 Dashboard", "📝 Manage Courses", "👥 Manage Students", "🏆 View & Add Results"]
choice = st.sidebar.selectbox("Main Navigation Menu", menu)

# ==========================================
# PAGE 1: MAIN DASHBOARD
# ==========================================
if choice == "📊 Dashboard":
    st.subheader("📊 System Overview Dashboard")
    
    # Fetch live counts from your actual database tables
    try:
        total_courses = cursor.execute("SELECT COUNT(*) FROM course").fetchone()[0]
        total_students = cursor.execute("SELECT COUNT(*) FROM student").fetchone()[0]
        total_results = cursor.execute("SELECT COUNT(*) FROM result").fetchone()[0]
    except:
        total_courses, total_students, total_results = 0, 0, 0
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.info(f"### Total Courses\n## {total_courses}")
    with col2:
        st.success(f"### Total Registered Students\n## {total_students}")
    with col3:
        st.warning(f"### Results Published\n## {total_results}")

# ==========================================
# PAGE 2: COURSE MANAGEMENT
# ==========================================
elif choice == "📝 Manage Courses":
    st.subheader("📝 Course Management Panel")
    
    with st.form("course_form", clear_on_submit=True):
        course_name = st.text_input("Course Name")
        duration = st.text_input("Duration (e.g., 3 Months)")
        description = st.text_area("Course Description")
        submit = st.form_submit_button("Save Course Details")
        
        if submit and course_name:
            cursor.execute("INSERT INTO course (name, duration, description) VALUES (?,?,?)", (course_name, duration, description))
            conn.commit()
            st.success(f"Successfully Added: {course_name}")
            st.rerun()

    st.write("### 🗃️ Saved Courses")
    courses_data = cursor.execute("SELECT * FROM course").fetchall()
    if courses_data:
        st.dataframe(courses_data, use_container_width=True)

# ==========================================
# PAGE 3: STUDENT MANAGEMENT
# ==========================================
elif choice == "👥 Manage Students":
    st.subheader("👥 Student Registration & Management")
    
    with st.form("student_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        with col1:
            roll = st.text_input("Roll Number")
            name = st.text_input("Full Name")
            email = st.text_input("Email ID")
        with col2:
            course_assigned = st.text_input("Course Name")
            contact = st.text_input("Contact Number")
            gender = st.selectbox("Gender", ["Male", "Female", "Other"])
            
        submit = st.form_submit_button("Register Student")
        
        if submit and roll and name:
            try:
                cursor.execute("INSERT INTO student (roll, name, email, gender, contact, course) VALUES (?,?,?,?,?,?)", 
                               (roll, name, email, gender, contact, course_assigned))
                conn.commit()
                st.success(f"Registered Student: {name}")
                st.rerun()
            except:
                st.error("Roll Number already exists!")

    st.write("### 🗃️ Registered Students List")
    students_data = cursor.execute("SELECT roll, name, email, gender, contact, course FROM student").fetchall()
    if students_data:
        st.dataframe(students_data, use_container_width=True)

# ==========================================
# PAGE 4: VIEW & ADD RESULTS
# ==========================================
elif choice == "🏆 View & Add Results":
    st.subheader("🏆 Student Results Portal")
    
    tab1, tab2 = st.tabs(["🔍 View Student Results", "➕ Add New Result Entry"])
    
    with tab1:
        search_roll = st.text_input("Enter Student Roll Number to Search")
        if search_roll:
            res = cursor.execute("SELECT * FROM result WHERE roll=?", (search_roll,)).fetchone()
            if res:
                st.markdown(f"### 📋 Result Card for Roll No: **{res[1]}**")
                st.write(f"**Student Name:** {res[2]}")
                st.write(f"**Course:** {res[3]}")
                st.write(f"**Marks Obtained:** {res[4]} / {res[5]}")
                st.info(f"**Percentage:** {res[6]}%")
            else:
                st.error("No result records found for this Roll Number.")
                
        st.write("---")
        st.write("### 🗃️ Overall Published Results Ledger")
        results_data = cursor.execute("SELECT * FROM result").fetchall()
        if results_data:
            st.dataframe(results_data, use_container_width=True)
            
    with tab2:
        with st.form("result_form", clear_on_submit=True):
            r_roll = st.text_input("Student Roll Number")
            r_name = st.text_input("Student Name")
            r_course = st.text_input("Course Name")
            marks_ob = st.number_input("Marks Obtained", min_value=0, max_value=100, value=0)
            full_marks = st.number_input("Full Marks", min_value=10, max_value=100, value=100)
            
            submit_res = st.form_submit_button("Publish Result")
            if submit_res and r_roll:
                percentage = round((marks_ob / full_marks) * 100, 2)
                cursor.execute("INSERT INTO result (roll, name, course, marks_ob, full_marks, per) VALUES (?,?,?,?,?,?)", 
                               (r_roll, r_name, r_course, str(marks_ob), str(full_marks), str(percentage)))
                conn.commit()
                st.success(f"Published result for {r_name} successfully!")
                st.rerun()