import tkinter as tk
from tkinter import messagebox, ttk
import sqlite3
import matplotlib.pyplot as plt

# Database setup
def init_db():
    conn = sqlite3.connect('health_app.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS goals (
            id INTEGER PRIMARY KEY,
            description TEXT,
            target_date TEXT,
            metric TEXT
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS training_plans (
            id INTEGER PRIMARY KEY,
            exercise_name TEXT,
            exercise_type TEXT,
            repetitions INTEGER,
            sets INTEGER,
            schedule TEXT
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS progress (
            id INTEGER PRIMARY KEY,
            goal_id INTEGER,
            date TEXT,
            completed_reps INTEGER,
            duration TEXT
        )
    ''')
    conn.commit()
    conn.close()

# GUI setup
class HealthApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Health Training Application")
        
        # Menu
        menubar = tk.Menu(root)
        root.config(menu=menubar)
        
        goal_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Goals", menu=goal_menu)
        goal_menu.add_command(label="Set Goals", command=self.set_goals)
        goal_menu.add_command(label="View Goals", command=self.view_goals)
        
        plan_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Training Plans", menu=plan_menu)
        plan_menu.add_command(label="Create Training Plan", command=self.create_training_plan)
        
        progress_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Progress", menu=progress_menu)
        progress_menu.add_command(label="Track Progress", command=self.track_progress)
    
    def set_goals(self):
        set_goal_window = tk.Toplevel(self.root)
        set_goal_window.title("Set Goals")
        
        tk.Label(set_goal_window, text="Goal Description").grid(row=0, column=0)
        goal_desc = tk.Entry(set_goal_window)
        goal_desc.grid(row=0, column=1)
        
        tk.Label(set_goal_window, text="Target Date").grid(row=1, column=0)
        target_date = tk.Entry(set_goal_window)
        target_date.grid(row=1, column=1)
        
        tk.Label(set_goal_window, text="Metric").grid(row=2, column=0)
        metric = tk.Entry(set_goal_window)
        metric.grid(row=2, column=1)
        
        def save_goal():
            desc = goal_desc.get()
            date = target_date.get()
            met = metric.get()
            
            conn = sqlite3.connect('health_app.db')
            cursor = conn.cursor()
            cursor.execute('INSERT INTO goals (description, target_date, metric) VALUES (?, ?, ?)', (desc, date, met))
            conn.commit()
            conn.close()
            messagebox.showinfo("Success", "Goal saved successfully!")
            set_goal_window.destroy()
        
        tk.Button(set_goal_window, text="Save Goal", command=save_goal).grid(row=3, column=0, columnspan=2)
    
    def view_goals(self):
        view_goals_window = tk.Toplevel(self.root)
        view_goals_window.title("View Goals")
        
        conn = sqlite3.connect('health_app.db')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM goals')
        goals = cursor.fetchall()
        conn.close()
        
        columns = ('ID', 'Description', 'Target Date', 'Metric')
        goals_tree = ttk.Treeview(view_goals_window, columns=columns, show='headings')
        
        for col in columns:
            goals_tree.heading(col, text=col)
            goals_tree.column(col, width=100)
        
        for goal in goals:
            goals_tree.insert('', tk.END, values=goal)
        
        goals_tree.pack(fill=tk.BOTH, expand=True)
    
    def create_training_plan(self):
        create_plan_window = tk.Toplevel(self.root)
        create_plan_window.title("Create Training Plan")
        
        tk.Label(create_plan_window, text="Exercise Name").grid(row=0, column=0)
        exercise_name = tk.Entry(create_plan_window)
        exercise_name.grid(row=0, column=1)
        
        tk.Label(create_plan_window, text="Exercise Type").grid(row=1, column=0)
        exercise_type = tk.Entry(create_plan_window)
        exercise_type.grid(row=1, column=1)
        
        tk.Label(create_plan_window, text="Repetitions").grid(row=2, column=0)
        repetitions = tk.Entry(create_plan_window)
        repetitions.grid(row=2, column=1)
        
        tk.Label(create_plan_window, text="Sets").grid(row=3, column=0)
        sets = tk.Entry(create_plan_window)
        sets.grid(row=3, column=1)
        
        tk.Label(create_plan_window, text="Schedule").grid(row=4, column=0)
        schedule = tk.Entry(create_plan_window)
        schedule.grid(row=4, column=1)
        
        def save_plan():
            name = exercise_name.get()
            type_ = exercise_type.get()
            reps = repetitions.get()
            sets_ = sets.get()
            sched = schedule.get()
            
            conn = sqlite3.connect('health_app.db')
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO training_plans (exercise_name, exercise_type, repetitions, sets, schedule) 
                VALUES (?, ?, ?, ?, ?)
            ''', (name, type_, reps, sets_, sched))
            conn.commit()
            conn.close()
            messagebox.showinfo("Success", "Training plan saved successfully!")
            create_plan_window.destroy()
        
        tk.Button(create_plan_window, text="Save Plan", command=save_plan).grid(row=5, column=0, columnspan=2)
    
    def track_progress(self):
        track_progress_window = tk.Toplevel(self.root)
        track_progress_window.title("Track Progress")
        
        tk.Label(track_progress_window, text="Goal ID").grid(row=0, column=0)
        goal_id = tk.Entry(track_progress_window)
        goal_id.grid(row=0, column=1)
        
        tk.Label(track_progress_window, text="Date").grid(row=1, column=0)
        date = tk.Entry(track_progress_window)
        date.grid(row=1, column=1)
        
        tk.Label(track_progress_window, text="Completed Repetitions").grid(row=2, column=0)
        completed_reps = tk.Entry(track_progress_window)
        completed_reps.grid(row=2, column=1)
        
        tk.Label(track_progress_window, text="Duration").grid(row=3, column=0)
        duration = tk.Entry(track_progress_window)
        duration.grid(row=3, column=1)
        
        def save_progress():
            g_id = goal_id.get()
            date_ = date.get()
            reps = completed_reps.get()
            dur = duration.get()
            
            conn = sqlite3.connect('health_app.db')
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO progress (goal_id, date, completed_reps, duration) 
                VALUES (?, ?, ?, ?)
            ''', (g_id, date_, reps, dur))
            conn.commit()
            conn.close()
            messagebox.showinfo("Success", "Progress saved successfully!")
            track_progress_window.destroy()
        
        tk.Button(track_progress_window, text="Save Progress", command=save_progress).grid(row=4, column=0, columnspan=2)

if __name__ == "__main__":
    init_db()
    root = tk.Tk()
    app = HealthApp(root)
    root.mainloop()
