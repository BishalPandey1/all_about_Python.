import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from datetime import datetime, timedelta, date
import json
import os

# =============================================================================
# DATA FILE PATH (for auto-save / load)
# =============================================================================
DATA_FILE = "tracker_data.json"

# =============================================================================
# GLOBAL DATA STORE
# =============================================================================
# Each task: {name, date_str, start, end, duration_min, category}
tasks_data = []

# User's daily productive goal (in minutes)
daily_goal_minutes = 240  # 4 hours default

# =============================================================================
# HELPER FUNCTIONS
# =============================================================================
def parse_time(time_str):
    """Convert 'HH:MM AM/PM' string to a datetime object."""
    for fmt in ("%I:%M %p", "%H:%M"):
        try:
            return datetime.strptime(time_str.strip(), fmt)
        except ValueError:
            continue
    return None

def format_minutes(mins):
    """Convert total minutes to 'Xh Ym' string."""
    if mins is None or mins < 0:
        return "0h 0m"
    h = int(mins // 60)
    m = int(mins % 60)
    return f"{h}h {m}m"

def get_week_range(ref_date):
    """Return (monday, sunday) for the week containing ref_date."""
    mon = ref_date - timedelta(days=ref_date.weekday())
    sun = mon + timedelta(days=6)
    return mon, sun

# =============================================================================
# SAVE / LOAD DATA (JSON persistence)
# =============================================================================
def save_data():
    """Write tasks_data and goal to a JSON file."""
    payload = {
        "tasks": [
            {
                "name": t["name"],
                "date_str": t["date"].strftime("%d-%m-%Y") if isinstance(t["date"], date) else t["date"],
                "start": t["start"],
                "end": t["end"],
                "duration_min": t["duration_min"],
                "category": t["category"]
            }
            for t in tasks_data
        ],
        "daily_goal_minutes": daily_goal_minutes
    }
    try:
        with open(DATA_FILE, "w") as f:
            json.dump(payload, f, indent=2)
    except Exception:
        pass  # Silently fail — no crash for save errors

def load_data():
    """Load tasks and goal from JSON file (if it exists)."""
    global tasks_data, daily_goal_minutes
    if not os.path.exists(DATA_FILE):
        return
    try:
        with open(DATA_FILE, "r") as f:
            payload = json.load(f)
        tasks_data.clear()
        for t in payload.get("tasks", []):
            try:
                d = datetime.strptime(t["date_str"], "%d-%m-%Y").date()
            except Exception:
                d = date.today()
            tasks_data.append({
                "name": t["name"],
                "date": d,
                "start": t["start"],
                "end": t["end"],
                "duration_min": t["duration_min"],
                "category": t["category"]
            })
        daily_goal_minutes = payload.get("daily_goal_minutes", 240)
    except Exception:
        pass

# =============================================================================
# MAIN WINDOW
# =============================================================================
root = tk.Tk()
root.title("Student Daily Life Tracker")
root.geometry(f"1250x700+{(root.winfo_screenwidth()-1250)//2}+30")
root.configure(bg="#f0f2f5")
root.minsize(1100, 700)

# Load saved data
load_data()

# =============================================================================
# CUSTOM TTK STYLES
# =============================================================================
style = ttk.Style()
style.theme_use("clam")

# Color palette
NAVY = "#1a1a2e"
TEAL = "#00b894"
CORAL = "#ff6b6b"
GOLD = "#fdcb6e"
WHITE = "#ffffff"
BG = "#f0f2f5"
CARD_BG = "#ffffff"
DARK_TEXT = "#2d3436"
GREY_TEXT = "#636e72"

style.configure(".", font=("Segoe UI", 10))
style.configure("Header.TLabel", font=("Segoe UI", 20, "bold"), foreground=WHITE, background=NAVY)
style.configure("SubHead.TLabel", font=("Segoe UI", 10), foreground="#a0a0b0", background=NAVY)
style.configure("CardTitle.TLabel", font=("Segoe UI", 13, "bold"), foreground="#16213e", background=CARD_BG)
style.configure("Field.TLabel", font=("Segoe UI", 10), foreground=DARK_TEXT, background=CARD_BG)
style.configure("StatValue.TLabel", font=("Segoe UI", 16, "bold"), foreground=NAVY, background=CARD_BG)
style.configure("StatLabel.TLabel", font=("Segoe UI", 9), foreground=GREY_TEXT, background=CARD_BG)

style.configure("Add.TButton", font=("Segoe UI", 10, "bold"), foreground=WHITE, background=TEAL)
style.map("Add.TButton", background=[("active", "#00cec9"), ("!active", TEAL)])

style.configure("Danger.TButton", font=("Segoe UI", 9, "bold"), foreground=WHITE, background=CORAL)
style.map("Danger.TButton", background=[("active", "#ee5a24"), ("!active", CORAL)])

style.configure("Nav.TButton", font=("Segoe UI", 9, "bold"), foreground=DARK_TEXT, background="#dfe6e9")
style.map("Nav.TButton", background=[("active", "#b2bec3"), ("!active", "#dfe6e9")])

style.configure("Goal.TButton", font=("Segoe UI", 9), foreground=WHITE, background="#6c5ce7")
style.map("Goal.TButton", background=[("active", "#a29bfe"), ("!active", "#6c5ce7")])

style.configure("Treeview", font=("Segoe UI", 10), rowheight=30, background=CARD_BG, fieldbackground=CARD_BG)
style.configure("Treeview.Heading", font=("Segoe UI", 10, "bold"), foreground=NAVY, background="#dfe6e9")
style.layout("Treeview", [("Treeview.treearea", {"sticky": "nswe"})])

# =============================================================================
# HEADER
# =============================================================================
header_frame = tk.Frame(root, bg=NAVY, padx=30, pady=12)
header_frame.pack(fill=tk.X)

ttk.Label(header_frame, text="  STUDENT DAILY LIFE TRACKER", style="Header.TLabel").pack(anchor="w")
ttk.Label(header_frame, text="Log your activities, measure productivity, and build better habits",
          style="SubHead.TLabel").pack(anchor="w")

# =============================================================================
# SCROLLABLE CONTENT
# =============================================================================
canvas = tk.Canvas(root, bg=BG, highlightthickness=0)
v_scroll = ttk.Scrollbar(root, orient="vertical", command=canvas.yview)
content = tk.Frame(canvas, bg=BG)
content.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
canvas.create_window((0, 0), window=content, anchor="nw")
canvas.configure(yscrollcommand=v_scroll.set)
canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
v_scroll.pack(side=tk.RIGHT, fill=tk.Y)

# =============================================================================
# VARIABLES
# =============================================================================
today = date.today()
current_week_start, current_week_end = get_week_range(today)

var_task = tk.StringVar()
var_date = tk.StringVar(value=today.strftime("%d-%m-%Y"))
var_start_h = tk.StringVar(value="09")
var_start_m = tk.StringVar(value="00")
var_start_ampm = tk.StringVar(value="AM")
var_end_h = tk.StringVar(value="10")
var_end_m = tk.StringVar(value="00")
var_end_ampm = tk.StringVar(value="AM")
var_category = tk.StringVar(value="Productive")
var_editing_index = None  # Set to an index when editing an existing task

# =============================================================================
# WEEK NAVIGATION
# =============================================================================
week_nav_frame = tk.Frame(content, bg=CARD_BG, padx=20, pady=10, relief=tk.RIDGE, bd=1)
week_nav_frame.pack(fill=tk.X, padx=20, pady=(18, 0))

week_label = ttk.Label(week_nav_frame, font=("Segoe UI", 12, "bold"), foreground=NAVY, background=CARD_BG)

def update_week_label():
    week_label.config(text=f"Week:  {current_week_start.strftime('%d %b %Y')}  —  {current_week_end.strftime('%d %b %Y')}")

def week_navigate(delta):
    global current_week_start, current_week_end
    current_week_start += timedelta(days=7 * delta)
    current_week_end += timedelta(days=7 * delta)
    update_week_label()
    refresh_all()

def reset_week():
    global current_week_start, current_week_end
    current_week_start, current_week_end = get_week_range(date.today())
    update_week_label()
    refresh_all()

ttk.Button(week_nav_frame, text="  ◀  Prev  ", style="Nav.TButton", command=lambda: week_navigate(-1)).pack(side=tk.LEFT)
ttk.Button(week_nav_frame, text="  Today  ", style="Nav.TButton", command=reset_week).pack(side=tk.LEFT, padx=6)
week_label.pack(side=tk.LEFT, expand=True)
ttk.Button(week_nav_frame, text="  Next  ▶  ", style="Nav.TButton", command=lambda: week_navigate(1)).pack(side=tk.RIGHT)
update_week_label()

# =============================================================================
# FORM CARD
# =============================================================================
form_card = tk.Frame(content, bg=CARD_BG, relief=tk.RIDGE, bd=1, padx=25, pady=18)
form_card.pack(fill=tk.X, padx=20, pady=14)

ttk.Label(form_card, text="  Add New Activity", style="CardTitle.TLabel").grid(row=0, column=0, columnspan=6, sticky="w", pady=(0, 14))

# Row 1: Name + Date
ttk.Label(form_card, text="Activity Name :", style="Field.TLabel").grid(row=1, column=0, sticky="w", pady=5)
e_name = ttk.Entry(form_card, textvariable=var_task, font=("Segoe UI", 11), width=28)
e_name.grid(row=1, column=1, sticky="w", pady=5, padx=(0, 20))

ttk.Label(form_card, text="Date (DD-MM-YYYY) :", style="Field.TLabel").grid(row=1, column=2, sticky="w", pady=5, padx=(10, 0))
e_date = ttk.Entry(form_card, textvariable=var_date, font=("Segoe UI", 11), width=16)
e_date.grid(row=1, column=3, sticky="w", pady=5, padx=(5, 0))

# Row 2: Start time + Quick preset buttons
ttk.Label(form_card, text="Start Time :", style="Field.TLabel").grid(row=2, column=0, sticky="w", pady=5)

tf1 = tk.Frame(form_card, bg=CARD_BG)
tf1.grid(row=2, column=1, sticky="w", pady=5)
ttk.Combobox(tf1, textvariable=var_start_h, values=[f"{i:02d}" for i in range(1, 13)], width=4, state="readonly", font=("Segoe UI", 11)).pack(side=tk.LEFT)
ttk.Label(tf1, text=" : ", font=("Segoe UI", 11, "bold"), background=CARD_BG).pack(side=tk.LEFT)
ttk.Combobox(tf1, textvariable=var_start_m, values=[f"{i:02d}" for i in range(0, 60, 5)], width=4, state="readonly", font=("Segoe UI", 11)).pack(side=tk.LEFT)
ttk.Combobox(tf1, textvariable=var_start_ampm, values=["AM", "PM"], width=5, state="readonly", font=("Segoe UI", 11)).pack(side=tk.LEFT, padx=(5, 0))

# Quick preset label
ttk.Label(form_card, text="Quick Duration :", style="Field.TLabel").grid(row=2, column=2, sticky="w", pady=5, padx=(10, 0))
preset_frame = tk.Frame(form_card, bg=CARD_BG)
preset_frame.grid(row=2, column=3, columnspan=2, sticky="w", pady=5)

# Apply a preset: add X minutes to start time to auto-fill end time
def apply_preset(minutes):
    start_str = f"{var_start_h.get()}:{var_start_m.get()} {var_start_ampm.get()}"
    st = parse_time(start_str)
    if st is None:
        return
    et = st + timedelta(minutes=minutes)
    h = et.hour
    m = et.minute
    ampm = "AM" if h < 12 else "PM"
    if h == 0:
        h = 12
    elif h > 12:
        h -= 12
    var_end_h.set(f"{h:02d}")
    var_end_m.set(f"{m:02d}")
    var_end_ampm.set(ampm)

for mins, lbl in [(30, "30m"), (60, "1h"), (90, "1.5h"), (120, "2h")]:
    btn = tk.Button(preset_frame, text=lbl, font=("Segoe UI", 9, "bold"),
                    bg="#dfe6e9", fg=DARK_TEXT, relief=tk.RAISED, bd=1, padx=10, pady=2,
                    cursor="hand2", command=lambda m=mins: apply_preset(m))
    btn.pack(side=tk.LEFT, padx=3)

# Row 3: End time + Category
ttk.Label(form_card, text="End Time :", style="Field.TLabel").grid(row=3, column=0, sticky="w", pady=5)

tf2 = tk.Frame(form_card, bg=CARD_BG)
tf2.grid(row=3, column=1, sticky="w", pady=5)
ttk.Combobox(tf2, textvariable=var_end_h, values=[f"{i:02d}" for i in range(1, 13)], width=4, state="readonly", font=("Segoe UI", 11)).pack(side=tk.LEFT)
ttk.Label(tf2, text=" : ", font=("Segoe UI", 11, "bold"), background=CARD_BG).pack(side=tk.LEFT)
ttk.Combobox(tf2, textvariable=var_end_m, values=[f"{i:02d}" for i in range(0, 60, 5)], width=4, state="readonly", font=("Segoe UI", 11)).pack(side=tk.LEFT)
ttk.Combobox(tf2, textvariable=var_end_ampm, values=["AM", "PM"], width=5, state="readonly", font=("Segoe UI", 11)).pack(side=tk.LEFT, padx=(5, 0))

ttk.Label(form_card, text="Category :", style="Field.TLabel").grid(row=3, column=2, sticky="w", pady=5, padx=(10, 0))
cat_combo = ttk.Combobox(form_card, textvariable=var_category, values=["Productive", "Non-Productive"],
                         state="readonly", font=("Segoe UI", 11), width=16)
cat_combo.grid(row=3, column=3, sticky="w", pady=5)

# Row 4: Action buttons
action_frame = tk.Frame(form_card, bg=CARD_BG)
action_frame.grid(row=4, column=0, columnspan=6, pady=(14, 0))

add_btn = ttk.Button(action_frame, text="  +  Add Activity  ", style="Add.TButton", command=lambda: add_activity())
add_btn.pack(side=tk.LEFT, padx=5)

clear_btn = ttk.Button(action_frame, text="  Clear  ", style="Nav.TButton", command=lambda: clear_form())
clear_btn.pack(side=tk.LEFT, padx=5)

# =============================================================================
# STATISTICS ROW
# =============================================================================
stats_card = tk.Frame(content, bg=CARD_BG, relief=tk.RIDGE, bd=1, padx=20, pady=14)
stats_card.pack(fill=tk.X, padx=20, pady=(0, 14))

ttk.Label(stats_card, text="  Weekly Statistics", style="CardTitle.TLabel").grid(row=0, column=0, columnspan=6, sticky="w", pady=(0, 10))

# Stat boxes
stat_boxes = []
stat_data = [
    ("Productive Time", "0h 0m", TEAL),
    ("Non-Productive", "0h 0m", CORAL),
    ("Net Balance", "0h 0m", NAVY),
    ("Productivity %", "0%", GOLD),
    ("Goal Progress", "0 / 0h", "#6c5ce7"),
    ("Best Day", "—", "#00cec9"),
]
for i, (title, val, color) in enumerate(stat_data):
    box = tk.Frame(stats_card, bg=color, padx=14, pady=8)
    box.grid(row=1, column=i, padx=5, sticky="ew")
    stats_card.columnconfigure(i, weight=1)
    tk.Label(box, text=title, font=("Segoe UI", 9), fg=WHITE, bg=color).pack(anchor="w")
    val_label = tk.Label(box, text=val, font=("Segoe UI", 15, "bold"), fg=WHITE, bg=color)
    val_label.pack(anchor="w")
    stat_boxes.append(val_label)

# Daily goal setter button
def set_goal():
    global daily_goal_minutes
    ans = simpledialog.askstring("Daily Goal", "Enter target productive hours per day:", parent=root, initialvalue=str(daily_goal_minutes // 60))
    if ans:
        try:
            daily_goal_minutes = max(1, int(float(ans) * 60))
            save_data()
            refresh_all()
        except ValueError:
            pass

ttk.Button(stats_card, text="Set Daily Goal", style="Goal.TButton", command=set_goal).grid(row=2, column=0, columnspan=6, sticky="e", pady=(8, 0))

# =============================================================================
# DAILY BREAKDOWN BAR CHART
# =============================================================================
breakdown_card = tk.Frame(content, bg=CARD_BG, relief=tk.RIDGE, bd=1, padx=20, pady=14)
breakdown_card.pack(fill=tk.X, padx=20, pady=(0, 14))

ttk.Label(breakdown_card, text="  Daily Breakdown (this week)", style="CardTitle.TLabel").pack(anchor="w", pady=(0, 10))

day_frame = tk.Frame(breakdown_card, bg=CARD_BG)
day_frame.pack(fill=tk.X)

day_labels = []  # To update later
day_bars = []    # Canvas bar widgets (prod bar, nonprod bar, text)

DAY_NAMES = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

BAR_HEIGHT = 22
BAR_MAX = 250  # max pixel width for bars

def build_day_rows():
    """Create the 7 day rows in day_frame."""
    for row_idx in range(7):
        day_name = DAY_NAMES[row_idx]
        row_fr = tk.Frame(day_frame, bg=CARD_BG)
        row_fr.pack(fill=tk.X, pady=3)

        # Day name label
        lbl = tk.Label(row_fr, text=day_name[:3], font=("Segoe UI", 9, "bold"),
                       width=4, anchor="w", fg=DARK_TEXT, bg=CARD_BG)
        lbl.pack(side=tk.LEFT)

        # Date label
        date_lbl = tk.Label(row_fr, text="", font=("Segoe UI", 8), width=10,
                            anchor="w", fg=GREY_TEXT, bg=CARD_BG)
        date_lbl.pack(side=tk.LEFT)

        # Productive bar (teal)
        p_canvas = tk.Canvas(row_fr, height=BAR_HEIGHT, bg="#e8f8f5",
                             highlightthickness=0, width=BAR_MAX)
        p_canvas.pack(side=tk.LEFT, padx=2)
        p_bar = p_canvas.create_rectangle(0, 0, 0, BAR_HEIGHT, fill=TEAL, outline="")

        # Non-Productive bar (coral)
        n_canvas = tk.Canvas(row_fr, height=BAR_HEIGHT, bg="#fde8e8",
                             highlightthickness=0, width=BAR_MAX)
        n_canvas.pack(side=tk.LEFT, padx=2)
        n_bar = n_canvas.create_rectangle(0, 0, 0, BAR_HEIGHT, fill=CORAL, outline="")

        # Duration text
        dur_lbl = tk.Label(row_fr, text="", font=("Segoe UI", 8), width=14,
                           anchor="w", fg=GREY_TEXT, bg=CARD_BG)
        dur_lbl.pack(side=tk.LEFT)

        # Info text (productive%)
        info_lbl = tk.Label(row_fr, text="", font=("Segoe UI", 8, "bold"), width=10,
                            anchor="w", fg=TEAL, bg=CARD_BG)
        info_lbl.pack(side=tk.LEFT)

        day_labels.append((date_lbl, dur_lbl, info_lbl))
        day_bars.append((p_canvas, p_bar, n_canvas, n_bar))

build_day_rows()

# =============================================================================
# TABLES SIDE BY SIDE
# =============================================================================
tables_frame = tk.Frame(content, bg=BG)
tables_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 20))

# ---------- Productive Table ----------
prod_frame = tk.Frame(tables_frame, bg=CARD_BG, relief=tk.RIDGE, bd=1)
prod_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 8))

prod_header = tk.Frame(prod_frame, bg=TEAL, padx=12, pady=7)
prod_header.pack(fill=tk.X)
tk.Label(prod_header, text="  PRODUCTIVE ACTIVITIES", font=("Segoe UI", 12, "bold"), fg=WHITE, bg=TEAL).pack(anchor="w")

prod_tree = ttk.Treeview(prod_frame, columns=("#", "Activity", "Date", "Start", "End", "Duration"), show="headings", height=7, selectmode="browse")
for c, w in [("#", 35), ("Activity", 170), ("Date", 95), ("Start", 75), ("End", 75), ("Duration", 75)]:
    prod_tree.heading(c, text=c)
    prod_tree.column(c, width=w, anchor="center")
prod_tree.column("Activity", anchor="w")
prod_sb = ttk.Scrollbar(prod_frame, orient="vertical", command=prod_tree.yview)
prod_tree.configure(yscrollcommand=prod_sb.set)
prod_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=6, pady=6)
prod_sb.pack(side=tk.RIGHT, fill=tk.Y, pady=6)

# Double-click to edit
prod_tree.bind("<Double-1>", lambda e: edit_task_dialog(prod_tree, "Productive"))

btn_row_p = tk.Frame(prod_frame, bg=CARD_BG)
btn_row_p.pack(fill=tk.X, padx=6, pady=(0, 6))
ttk.Button(btn_row_p, text="Delete Selected", style="Danger.TButton", command=lambda: delete_task(prod_tree, "Productive")).pack(side=tk.LEFT, padx=2)
ttk.Button(btn_row_p, text="Edit", style="Nav.TButton", command=lambda: edit_task_dialog(prod_tree, "Productive")).pack(side=tk.LEFT, padx=2)

# ---------- Non-Productive Table ----------
nonprod_frame = tk.Frame(tables_frame, bg=CARD_BG, relief=tk.RIDGE, bd=1)
nonprod_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(8, 0))

nonprod_header = tk.Frame(nonprod_frame, bg=CORAL, padx=12, pady=7)
nonprod_header.pack(fill=tk.X)
tk.Label(nonprod_header, text="  NON-PRODUCTIVE ACTIVITIES", font=("Segoe UI", 12, "bold"), fg=WHITE, bg=CORAL).pack(anchor="w")

nonprod_tree = ttk.Treeview(nonprod_frame, columns=("#", "Activity", "Date", "Start", "End", "Duration"), show="headings", height=7, selectmode="browse")
for c, w in [("#", 35), ("Activity", 170), ("Date", 95), ("Start", 75), ("End", 75), ("Duration", 75)]:
    nonprod_tree.heading(c, text=c)
    nonprod_tree.column(c, width=w, anchor="center")
nonprod_tree.column("Activity", anchor="w")
nonprod_sb = ttk.Scrollbar(nonprod_frame, orient="vertical", command=nonprod_tree.yview)
nonprod_tree.configure(yscrollcommand=nonprod_sb.set)
nonprod_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=6, pady=6)
nonprod_sb.pack(side=tk.RIGHT, fill=tk.Y, pady=6)

nonprod_tree.bind("<Double-1>", lambda e: edit_task_dialog(nonprod_tree, "Non-Productive"))

btn_row_n = tk.Frame(nonprod_frame, bg=CARD_BG)
btn_row_n.pack(fill=tk.X, padx=6, pady=(0, 6))
ttk.Button(btn_row_n, text="Delete Selected", style="Danger.TButton", command=lambda: delete_task(nonprod_tree, "Non-Productive")).pack(side=tk.LEFT, padx=2)
ttk.Button(btn_row_n, text="Edit", style="Nav.TButton", command=lambda: edit_task_dialog(nonprod_tree, "Non-Productive")).pack(side=tk.LEFT, padx=2)

# =============================================================================
# CORE APPLICATION LOGIC
# =============================================================================
def add_activity():
    """Validate input, calculate duration, store task, and refresh UI."""
    name = var_task.get().strip()
    date_str = var_date.get().strip()
    start_str = f"{var_start_h.get()}:{var_start_m.get()} {var_start_ampm.get()}"
    end_str = f"{var_end_h.get()}:{var_end_m.get()} {var_end_ampm.get()}"
    category = var_category.get()

    if not name:
        messagebox.showwarning("Validation", "Please enter an activity name.")
        return

    try:
        task_date = datetime.strptime(date_str, "%d-%m-%Y").date()
    except ValueError:
        messagebox.showwarning("Validation", "Date must be in DD-MM-YYYY format.")
        return

    start_dt = parse_time(start_str)
    end_dt = parse_time(end_str)
    if start_dt is None or end_dt is None:
        messagebox.showwarning("Validation", "Please enter valid time values (HH:MM AM/PM).")
        return

    duration_min = (end_dt - start_dt).total_seconds() / 60.0
    if duration_min <= 0:
        messagebox.showwarning("Validation", "End time must be after start time.")
        return

    task = {
        "name": name,
        "date": task_date,
        "start": start_str,
        "end": end_str,
        "duration_min": duration_min,
        "category": category
    }

    idx = var_editing_index.get() if var_editing_index is not None else None
    # We don't use var_editing_index in the current flow, but we could for edit mode
    # For now, simple add:
    tasks_data.append(task)

    save_data()
    refresh_all()
    clear_form()
    messagebox.showinfo("Success", f"'{name}' added as {category}!")

def clear_form():
    """Reset form fields to defaults."""
    var_task.set("")
    var_date.set(today.strftime("%d-%m-%Y"))
    var_start_h.set("09")
    var_start_m.set("00")
    var_start_ampm.set("AM")
    var_end_h.set("10")
    var_end_m.set("00")
    var_end_ampm.set("AM")
    var_category.set("Productive")

def delete_task(tree, category):
    """Delete the selected row from the tree and from data store."""
    sel = tree.selection()
    if not sel:
        messagebox.showinfo("Info", "Select a task to delete.")
        return
    item = tree.item(sel[0])
    vals = item["values"]
    if not vals:
        return

    # Filter current week tasks by category
    week_tasks = [t for t in tasks_data
                  if current_week_start <= t["date"] <= current_week_end and t["category"] == category]
    idx = int(vals[0]) - 1
    if 0 <= idx < len(week_tasks):
        tgt = week_tasks[idx]
        tasks_data.remove(tgt)
        save_data()
        refresh_all()

def edit_task_dialog(tree, category):
    """Open a simple dialog to edit the selected task's name and duration."""
    sel = tree.selection()
    if not sel:
        messagebox.showinfo("Info", "Select a task to edit.")
        return
    item = tree.item(sel[0])
    vals = item["values"]
    if not vals:
        return

    week_tasks = [t for t in tasks_data
                  if current_week_start <= t["date"] <= current_week_end and t["category"] == category]
    idx = int(vals[0]) - 1
    if not (0 <= idx < len(week_tasks)):
        return
    task = week_tasks[idx]

    # Pre-fill form with this task's values for editing
    var_task.set(task["name"])
    var_date.set(task["date"].strftime("%d-%m-%Y"))
    # Parse start time
    st = parse_time(task["start"])
    if st:
        h = st.hour
        ampm = "AM" if h < 12 else "PM"
        if h == 0:
            h = 12
        elif h > 12:
            h -= 12
        var_start_h.set(f"{h:02d}")
        var_start_m.set(f"{st.minute:02d}")
        var_start_ampm.set(ampm)
    et = parse_time(task["end"])
    if et:
        h = et.hour
        ampm = "AM" if h < 12 else "PM"
        if h == 0:
            h = 12
        elif h > 12:
            h -= 12
        var_end_h.set(f"{h:02d}")
        var_end_m.set(f"{et.minute:02d}")
        var_end_ampm.set(ampm)
    var_category.set(task["category"])

    # Remove old entry, will be re-added on submit
    tasks_data.remove(task)

    # Notify user to modify and re-submit
    messagebox.showinfo("Edit Mode", f"Editing '{task['name']}'.\nModify the form and click 'Add Activity' to save changes.")
    save_data()
    refresh_all()

def refresh_all():
    """Refresh statistics, daily breakdown, tables, and summary."""
    # --- Filter this week's tasks ---
    week_tasks = [t for t in tasks_data
                  if current_week_start <= t["date"] <= current_week_end]

    prod_tasks = [t for t in week_tasks if t["category"] == "Productive"]
    nonprod_tasks = [t for t in week_tasks if t["category"] == "Non-Productive"]

    total_prod = sum(t["duration_min"] for t in prod_tasks)
    total_nonprod = sum(t["duration_min"] for t in nonprod_tasks)
    net = total_prod - total_nonprod
    total_all = total_prod + total_nonprod

    # --- Update Statistics Boxes ---
    if len(stat_boxes) >= 6:
        stat_boxes[0].config(text=format_minutes(total_prod))
        stat_boxes[1].config(text=format_minutes(total_nonprod))
        stat_boxes[2].config(text=format_minutes(abs(net)) + (" ✅" if net > 0 else (" ⚠️" if net < 0 else " ⚖️")))
        pct = (total_prod / total_all * 100) if total_all > 0 else 0
        stat_boxes[3].config(text=f"{pct:.0f}%")

        # Goal progress — find best day
        goal_hrs = daily_goal_minutes / 60
        # Sum productive minutes per day this week
        day_prod = {}
        for t in prod_tasks:
            d = t["date"]
            day_prod[d] = day_prod.get(d, 0) + t["duration_min"]
        best_day_mins = max(day_prod.values()) if day_prod else 0
        best_day_str = max(day_prod, key=day_prod.get).strftime("%a") if day_prod else "—"
        stat_boxes[4].config(text=f"{format_minutes(best_day_mins)} / {goal_hrs:.1f}h")
        stat_boxes[5].config(text=best_day_str)

    # --- Daily Breakdown ---
    for row_idx in range(7):
        d = current_week_start + timedelta(days=row_idx)
        day_prod_mins = sum(t["duration_min"] for t in prod_tasks if t["date"] == d)
        day_nonprod_mins = sum(t["duration_min"] for t in nonprod_tasks if t["date"] == d)
        total_day = day_prod_mins + day_nonprod_mins

        date_lbl, dur_lbl, info_lbl = day_labels[row_idx]
        p_canvas, p_bar, n_canvas, n_bar = day_bars[row_idx]

        # Scale bars
        max_mins = max(day_prod_mins, day_nonprod_mins, 1)
        p_width = int((day_prod_mins / max_mins) * BAR_MAX) if max_mins else 0
        n_width = int((day_nonprod_mins / max_mins) * BAR_MAX) if max_mins else 0

        p_canvas.coords(p_bar, 0, 0, p_width, BAR_HEIGHT)
        n_canvas.coords(n_bar, 0, 0, n_width, BAR_HEIGHT)

        date_lbl.config(text=f"{d.strftime('%d/%m')} ")
        dur_lbl.config(text=f"P:{format_minutes(day_prod_mins)}  NP:{format_minutes(day_nonprod_mins)}")
        if total_day > 0:
            info_lbl.config(text=f"  {day_prod_mins/total_day*100:.0f}% prod", fg=TEAL)
        else:
            info_lbl.config(text="  —", fg=GREY_TEXT)

    # --- Tables ---
    for tree in (prod_tree, nonprod_tree):
        for row in tree.get_children():
            tree.delete(row)

    for i, t in enumerate(prod_tasks, 1):
        prod_tree.insert("", tk.END, values=(i, t["name"], t["date"].strftime("%d-%m-%Y"), t["start"], t["end"], format_minutes(t["duration_min"])))
    for i, t in enumerate(nonprod_tasks, 1):
        nonprod_tree.insert("", tk.END, values=(i, t["name"], t["date"].strftime("%d-%m-%Y"), t["start"], t["end"], format_minutes(t["duration_min"])))

# =============================================================================
# INITIALISE
# =============================================================================
refresh_all()
update_week_label()

# =============================================================================
# START APP
# =============================================================================
root.mainloop()
