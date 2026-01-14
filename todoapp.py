import customtkinter as ctk
import json
import os
from datetime import datetime

# Basic Settings
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class ProManagerApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("ProManager v1.0")
        self.geometry("1000x600")
        
        # Data Initialization
        self.db_file = "tasks_data.json"
        self.tasks = self.load_data()

        # Layout Configuration (1x2 grid)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # --- SIDEBAR NAVIGATION ---
        self.sidebar_frame = ctk.CTkFrame(self, corner_radius=0, width=200)
        self.sidebar_frame.grid(row=0, column=0, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(4, weight=1)

        self.logo_label = ctk.CTkLabel(self.sidebar_frame, text="PRO MANAGER", 
                                      font=ctk.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))

        self.btn_dash = ctk.CTkButton(self.sidebar_frame, text="Dashboard", command=self.show_dash, 
                                     corner_radius=0, height=40, fg_color="transparent")
        self.btn_dash.grid(row=1, column=0, sticky="ew")

        self.btn_tasks = ctk.CTkButton(self.sidebar_frame, text="Tasks", command=self.show_tasks, 
                                      corner_radius=0, height=40, fg_color="transparent")
        self.btn_tasks.grid(row=2, column=0, sticky="ew")

        self.appearance_mode_label = ctk.CTkLabel(self.sidebar_frame, text="Appearance Mode:", anchor="w")
        self.appearance_mode_label.grid(row=5, column=0, padx=20, pady=(10, 0))
        self.mode_menu = ctk.CTkOptionMenu(self.sidebar_frame, values=["Dark", "Light", "System"], 
                                          command=self.change_appearance)
        self.mode_menu.grid(row=6, column=0, padx=20, pady=(10, 20))

        # --- CONTENT AREAS ---
        # 1. Dashboard Frame
        self.dash_frame = ctk.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.setup_dash_ui()

        # 2. Tasks Frame
        self.tasks_frame = ctk.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.setup_tasks_ui()

        # Default Page
        self.show_dash()

    # --- DATA ENGINE ---
    def load_data(self):
        if os.path.exists(self.db_file):
            with open(self.db_file, "r") as f:
                return json.load(f)
        return []

    def save_data(self):
        with open(self.db_file, "w") as f:
            json.dump(self.tasks, f)
        self.update_dash_stats()

    # --- UI SETUP ---
    def setup_dash_ui(self):
        self.dash_frame.grid_columnconfigure((0, 1), weight=1)
        
        self.dash_title = ctk.CTkLabel(self.dash_frame, text="Performance Dashboard", font=("Arial", 24, "bold"))
        self.dash_title.grid(row=0, column=0, columnspan=2, padx=20, pady=20)

        self.stat_total = ctk.CTkLabel(self.dash_frame, text="Total Tasks: 0", font=("Arial", 16), 
                                      fg_color="#2b2b2b", corner_radius=10, height=100)
        self.stat_total.grid(row=1, column=0, padx=20, pady=10, sticky="nsew")

        self.stat_done = ctk.CTkLabel(self.dash_frame, text="Completed: 0", font=("Arial", 16), 
                                     fg_color="#2b2b2b", corner_radius=10, height=100)
        self.stat_done.grid(row=1, column=1, padx=20, pady=10, sticky="nsew")

    def setup_tasks_ui(self):
        self.tasks_frame.grid_columnconfigure(0, weight=1)
        
        # Entry Area
        self.entry_frame = ctk.CTkFrame(self.tasks_frame)
        self.entry_frame.grid(row=0, column=0, padx=20, pady=20, sticky="ew")
        
        self.task_entry = ctk.CTkEntry(self.entry_frame, placeholder_text="Enter a new task...")
        self.task_entry.pack(side="left", fill="x", expand=True, padx=10, pady=10)
        
        self.add_btn = ctk.CTkButton(self.entry_frame, text="Add Task", width=100, command=self.add_task)
        self.add_btn.pack(side="right", padx=10)

        # Scrollable Task List
        self.scrollable_tasks = ctk.CTkScrollableFrame(self.tasks_frame, label_text="Your Active Tasks")
        self.scrollable_tasks.grid(row=1, column=0, padx=20, pady=10, sticky="nsew")
        self.tasks_frame.grid_rowconfigure(1, weight=1)
        
        self.refresh_task_list()

    # --- LOGIC ---
    def show_dash(self):
        self.update_dash_stats()
        self.tasks_frame.grid_forget()
        self.dash_frame.grid(row=0, column=1, sticky="nsew")
        self.btn_dash.configure(fg_color=("gray75", "gray25"))
        self.btn_tasks.configure(fg_color="transparent")

    def show_tasks(self):
        self.dash_frame.grid_forget()
        self.tasks_frame.grid(row=0, column=1, sticky="nsew")
        self.btn_tasks.configure(fg_color=("gray75", "gray25"))
        self.btn_dash.configure(fg_color="transparent")

    def add_task(self):
        task_text = self.task_entry.get()
        if task_text:
            new_task = {"id": len(self.tasks), "text": task_text, "status": "Pending"}
            self.tasks.append(new_task)
            self.save_data()
            self.task_entry.delete(0, 'end')
            self.refresh_task_list()

    def refresh_task_list(self):
        for widget in self.scrollable_tasks.winfo_children():
            widget.destroy()

        for i, task in enumerate(self.tasks):
            f = ctk.CTkFrame(self.scrollable_tasks)
            f.pack(fill="x", pady=5)
            
            status_color = "green" if task["status"] == "Done" else "white"
            ctk.CTkLabel(f, text=task["text"], text_color=status_color).pack(side="left", padx=10)
            
            ctk.CTkButton(f, text="✓", width=30, fg_color="green", 
                          command=lambda t=task: self.mark_done(t)).pack(side="right", padx=5)
            ctk.CTkButton(f, text="X", width=30, fg_color="red", 
                          command=lambda t=task: self.delete_task(t)).pack(side="right", padx=5)

    def mark_done(self, task):
        task["status"] = "Done"
        self.save_data()
        self.refresh_task_list()

    def delete_task(self, task):
        self.tasks.remove(task)
        self.save_data()
        self.refresh_task_list()

    def update_dash_stats(self):
        total = len(self.tasks)
        done = len([t for t in self.tasks if t["status"] == "Done"])
        self.stat_total.configure(text=f"Total Tasks\n\n{total}")
        self.stat_done.configure(text=f"Completed\n\n{done}")

    def change_appearance(self, mode):
        ctk.set_appearance_mode(mode)

if __name__ == "__main__":
    app = ProManagerApp()
    app.mainloop()
