import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

# =============================================================================
# MAIN APPLICATION WINDOW
# =============================================================================
root = tk.Tk()
root.title("Student Personal Details Form")
root.geometry("700x750")
root.configure(bg="#f0f4f8")  # Light background for the main window

# =============================================================================
# STYLING CONFIGURATION
# =============================================================================
style = ttk.Style()
style.theme_use("clam")

# Custom styles for various widgets
style.configure("Title.TLabel", font=("Helvetica", 20, "bold"), foreground="#ffffff",
                background="#2c3e50", padding=10)
style.configure("Heading.TLabel", font=("Helvetica", 14, "bold"), foreground="#2c3e50",
                background="#f0f4f8")
style.configure("Field.TLabel", font=("Helvetica", 11), foreground="#34495e",
                background="#f0f4f8")
style.configure("Submit.TButton", font=("Helvetica", 12, "bold"), foreground="#ffffff",
                background="#27ae60", borderwidth=0, focusthickness=3, padding=8)
style.map("Submit.TButton",
          background=[("active", "#2ecc71"), ("!active", "#27ae60")])

# =============================================================================
# HEADER / TITLE BAR
# =============================================================================
header_frame = tk.Frame(root, bg="#2c3e50", padx=20, pady=15)
header_frame.pack(fill=tk.X)

title_label = ttk.Label(header_frame, text="🎓 Student Personal Details Form",
                        style="Title.TLabel")
title_label.pack()

# =============================================================================
# SCROLLABLE FORM AREA (so nothing gets cut off)
# =============================================================================
canvas = tk.Canvas(root, bg="#f0f4f8", highlightthickness=0)
scrollbar = ttk.Scrollbar(root, orient="vertical", command=canvas.yview)
scrollable_frame = tk.Frame(canvas, bg="#f0f4f8")

scrollable_frame.bind("<Configure>",
                      lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
canvas.configure(yscrollcommand=scrollbar.set)

canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(20, 0), pady=20)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y, padx=(0, 20), pady=20)

# =============================================================================
# FORM SECTION - CONTAINER
# =============================================================================
form_container = tk.Frame(scrollable_frame, bg="#ffffff", relief=tk.RIDGE,
                          bd=2, padx=30, pady=25)
form_container.pack(fill=tk.X, padx=10, pady=(0, 20))

# Section heading
section_heading = ttk.Label(form_container, text="📝 Fill Your Personal Details",
                            style="Heading.TLabel")
section_heading.grid(row=0, column=0, columnspan=3, pady=(0, 20), sticky="w")

# =============================================================================
# VARIABLES TO HOLD FORM DATA
# =============================================================================
var_name = tk.StringVar()
var_father = tk.StringVar()
var_mother = tk.StringVar()
var_dob = tk.StringVar()
var_gender = tk.StringVar(value="Male")
var_address = tk.StringVar()
var_email = tk.StringVar()
var_phone = tk.StringVar()
var_course = tk.StringVar()
var_semester = tk.StringVar(value="1")

# =============================================================================
# FUNCTION TO CREATE FORM ROWS EASILY
# =============================================================================
def create_form_row(parent, row, label_text, variable, show=None, width=40):
    """Create a label + entry row and return the Entry widget."""
    lbl = ttk.Label(parent, text=label_text, style="Field.TLabel")
    lbl.grid(row=row, column=0, sticky="w", pady=6, padx=(0, 10))
    entry = ttk.Entry(parent, textvariable=variable, font=("Helvetica", 11),
                      width=width, show=show)
    entry.grid(row=row, column=1, columnspan=2, sticky="ew", pady=6)
    return entry

# =============================================================================
# FORM FIELDS
# =============================================================================

# Row 1 - Student Name
create_form_row(form_container, 1, "Full Name:", var_name)

# Row 2 - Father's Name
create_form_row(form_container, 2, "Father's Name:", var_father)

# Row 3 - Mother's Name
create_form_row(form_container, 3, "Mother's Name:", var_mother)

# Row 4 - Date of Birth
create_form_row(form_container, 4, "Date of Birth (DD/MM/YYYY):", var_dob)

# Row 5 - Gender (Radio buttons)
gender_label = ttk.Label(form_container, text="Gender:", style="Field.TLabel")
gender_label.grid(row=5, column=0, sticky="w", pady=6, padx=(0, 10))

gender_frame = tk.Frame(form_container, bg="#ffffff")
gender_frame.grid(row=5, column=1, columnspan=2, sticky="w", pady=6)

for i, g in enumerate(["Male", "Female", "Other"]):
    rb = ttk.Radiobutton(gender_frame, text=g, variable=var_gender, value=g)
    rb.pack(side=tk.LEFT, padx=(0, 20))

# Row 6 - Address (Multi-line Text)
address_label = ttk.Label(form_container, text="Address:", style="Field.TLabel")
address_label.grid(row=6, column=0, sticky="nw", pady=6, padx=(0, 10))

address_text = tk.Text(form_container, font=("Helvetica", 11), height=4, width=43,
                       wrap=tk.WORD, relief=tk.SUNKEN, bd=2)
address_text.grid(row=6, column=1, columnspan=2, sticky="ew", pady=6)

# Row 7 - Email
create_form_row(form_container, 7, "Email:", var_email)

# Row 8 - Phone Number
create_form_row(form_container, 8, "Phone Number:", var_phone)

# Row 9 - Course / Program
create_form_row(form_container, 9, "Course / Program:", var_course)

# Row 10 - Semester (Dropdown)
sem_label = ttk.Label(form_container, text="Semester:", style="Field.TLabel")
sem_label.grid(row=10, column=0, sticky="w", pady=6, padx=(0, 10))

sem_combo = ttk.Combobox(form_container, textvariable=var_semester,
                         values=["1", "2", "3", "4", "5", "6", "7", "8"],
                         state="readonly", font=("Helvetica", 11), width=38)
sem_combo.grid(row=10, column=1, columnspan=2, sticky="w", pady=6)

# Make columns expand nicely
form_container.columnconfigure(1, weight=1)

# =============================================================================
# SUBMIT BUTTON
# =============================================================================
button_frame = tk.Frame(scrollable_frame, bg="#f0f4f8")
button_frame.pack(fill=tk.X, padx=10, pady=(0, 20))

submit_btn = ttk.Button(button_frame, text="✅  Submit Form", style="Submit.TButton",
                        command=lambda: submit_form())
submit_btn.pack(pady=5)

# =============================================================================
# DISPLAY AREA - Where submitted data appears
# =============================================================================
display_container = tk.Frame(scrollable_frame, bg="#ffffff", relief=tk.RIDGE,
                             bd=2, padx=25, pady=20)
display_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 20))

display_heading = ttk.Label(display_container, text="📋 Submitted Student Details",
                            style="Heading.TLabel")
display_heading.pack(anchor="w", pady=(0, 15))

# This label will show all the submitted information
display_output = tk.Label(display_container,
                          text="No data submitted yet. Fill the form and click Submit.",
                          font=("Consolas", 11), foreground="#7f8c8d",
                          background="#ffffff", justify=tk.LEFT, anchor="nw",
                          padx=10, pady=10)
display_output.pack(fill=tk.BOTH, expand=True)

# =============================================================================
# SUBMIT FUNCTION
# =============================================================================
def submit_form():
    """Collect all form data and display it in the output area below."""
    # Get values from the form fields
    name = var_name.get().strip()
    father = var_father.get().strip()
    mother = var_mother.get().strip()
    dob = var_dob.get().strip()
    gender = var_gender.get()
    address = address_text.get("1.0", tk.END).strip()
    email = var_email.get().strip()
    phone = var_phone.get().strip()
    course = var_course.get().strip()
    semester = var_semester.get()

    # Basic validation - ensure required fields are not empty
    if not name:
        messagebox.showwarning("Validation Error", "Please enter the student's name.")
        return
    if not course:
        messagebox.showwarning("Validation Error", "Please enter the course name.")
        return

    # Format the output in a clean, readable way
    output_text = f"""
    ╔══════════════════════════════════════════════╗
    ║         STUDENT DETAILS                      ║
    ╠══════════════════════════════════════════════╣
    ║  Full Name     : {name:<35} ║
    ║  Father's Name : {father:<35} ║
    ║  Mother's Name : {mother:<35} ║
    ║  Date of Birth : {dob:<35} ║
    ║  Gender        : {gender:<35} ║
    ║  Address       : {address[:35]:<35} ║
    ║  Email         : {email:<35} ║
    ║  Phone         : {phone:<35} ║
    ║  Course        : {course:<35} ║
    ║  Semester      : {semester:<35} ║
    ╚══════════════════════════════════════════════╝

    Submitted on: {datetime.now().strftime("%d-%m-%Y  %I:%M %p")}
    """

    # Update the display label with the formatted output
    display_output.configure(text=output_text, foreground="#2c3e50")

    # Show a success message to the user
    messagebox.showinfo("Success", "Student details have been submitted successfully!")


# =============================================================================
# START THE APPLICATION
# =============================================================================
root.mainloop()
