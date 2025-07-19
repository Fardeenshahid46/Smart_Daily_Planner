import tkinter as tk
from tkinter import messagebox, ttk
import json
from datetime import datetime

#To store tasks in a json file
file= "tasks.json"

#This class add user tasks in dictionary
class UserTask:
    def __init__(self, name, deadline, priority, completed=False):
        self.name = name
        self.deadline = deadline
        self.priority = priority
        self.completed = completed

    def to_dict(self):
        return {
            'name': self.name,
            'deadline': self.deadline,
            'priority': self.priority,
            'completed': self.completed
        }
#This class add,sort,save and load tasks in the file
class TaskManager:
    def __init__(self):
        self.tasks = []

    def add_task(self, task: UserTask):
        self.tasks.append(task)
        self.sort_tasks()

    def sort_tasks(self):
        self.tasks.sort(key=lambda t: (t.deadline, {"Urgent:1": 1, "Normal:2": 2, "Relaxed:3": 3}[t.priority]))


    def save_tasks(self):
        with open(file, 'w') as f:
            json.dump([t.to_dict() for t in self.tasks], f, indent=4)

    def load_tasks(self):
       try:
        with open(file, 'r') as f:
            content = f.read().strip()
            if not content:
                self.tasks = []
                return
            data = json.loads(content)
            self.tasks = [UserTask(**item) for item in data]
       except (FileNotFoundError, json.JSONDecodeError):
        self.tasks = []

#class for GUI
class TaskPlanner_App:
    def __init__(self, root):
        self.root = root
        self.root.title("Smart Daily Planner with Task Prioritization")
        self.task_manager = TaskManager()
        self.task_manager.load_tasks()

        # Section to collect task details from the user (task name, due date, and priority)
        tk.Label(root, text="Task:").grid(row=0, column=0)
        self.input_task_field = tk.Entry(root, width=30)
        self.input_task_field.grid(row=0, column=1)

        tk.Label(root, text="Deadline (YYYY-MM-DD):").grid(row=1, column=0)
        self.due_date_input = tk.Entry(root)
        self.due_date_input.grid(row=1, column=1)

        tk.Label(root, text="Priority:").grid(row=2, column=0)
        self.priority_selection = tk.StringVar()
        self.priority_menu = ttk.Combobox(root, textvariable=self.priority_selection, values=["Urgent:1", "Normal:2", "Relaxed:3"])
        self.priority_menu.grid(row=2, column=1)
        self.priority_menu.current(1)

        tk.Button(root, text="Add Task", command=self.insert_new_task).grid(row=3, column=1)

        self.task_display_list = tk.Listbox(root, width=80)
        self.task_display_list.grid(row=5, column=0, columnspan=3)

        tk.Button(root, text="Mark as Done", command=self.set_task_as_done).grid(row=6, column=0)
        tk.Button(root, text="Save Tasks", command=self.save_tasks).grid(row=6, column=2)
        tk.Button(root, text="Clear Tasks", command=self.clear_tasks).grid(row=7, column=1)

        self.reload_task_display()

    def insert_new_task(self):
        name = self.input_task_field.get()
        deadline = self.due_date_input.get()
        priority = self.priority_selection.get()

        if not name or not deadline:
            messagebox.showwarning( "Please enter your task and deadline.")
            return

        try:
            datetime.strptime(deadline, "%Y-%m-%d")
        except ValueError:
            messagebox.showerror("Invalid Date","Please use YYYY-MM-DD format.")
            return

        task = UserTask(name, deadline, priority)
        self.task_manager.add_task(task)
        self.reload_task_display()

    def set_task_as_done(self):
        selection = self.task_display_list.curselection()
        if selection:
            index = selection[0]
            self.task_manager.tasks[index].completed = True
            self.task_manager.save_tasks()
            self.reload_task_display()

    def reload_task_display(self):
        self.task_display_list.delete(0, tk.END)
        for task in self.task_manager.tasks:
            status = "✅" if task.completed else "❌"
            self.task_display_list.insert(tk.END, f"{status} {task.name} | {task.deadline} | {task.priority}")

    def save_tasks(self):
           self.task_manager.save_tasks()
           save_tasks = messagebox.askyesno("Save All Tasks", "Are you sure you want to save all tasks?")
           if save_tasks:
                self.task_manager.save_tasks()
                self.status_label.config(text="Tasks saved successfully!")
                self.root.after(3000, lambda: self.status_label.config(text=""))
                messagebox.showinfo("Done", "✅ Tasks have been saved.")
           else:
               messagebox.showinfo("Cancelled", "❌ Tasks were not saved.")     
           messagebox.showinfo( "Tasks are saved successfully.")
    
    def clear_tasks(self):
         confirmation = messagebox.askyesno("Clear All Tasks", "Are you sure you want to clear all tasks?")
         if confirmation:
            self.task_manager.tasks.clear()
            self.task_manager.save_tasks() 
            self.reload_task_display()
            messagebox.showinfo("Cleared", "All tasks have been cleared.")
            
            

if __name__ == "__main__":
    root = tk.Tk()
    app = TaskPlanner_App(root)
    root.mainloop()
