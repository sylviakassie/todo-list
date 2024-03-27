import ttkbootstrap as ttk
import tkinter as tk
from tkinter import messagebox
from task import Task, TaskManager


class TaskUpdateWindow:
    def __init__(self, master: ttk.Toplevel, listbox: tk.Listbox, index: int):
        self.master = master
        self.master.geometry('300x300')
        self.master.title('Update Task')
        self.master.resizable(False, False)
        self.listbox = listbox
        self.index = index

        self.task_name_label = ttk.Label(
            self.master, text='Task Name', font=('Helvetica', 12))
        self.task_entry = ttk.Entry(self.master, width=20)
        self.due_date_label = ttk.Label(
            self.master, text='Due Date', font=('Helvetica', 12))
        self.due_date = ttk.DateEntry(self.master, width=10)
        self.save_button = ttk.Button(
            self.master, text='Save', style='success.TButton', command=self.save)

        # Positions using place
        self.task_name_label.place(x=10, y=14)
        self.task_entry.place(x=100, y=10)
        self.due_date_label.place(x=10, y=74)
        self.due_date.place(x=100, y=70)
        self.save_button.place(x=150, y=120)

        self.set_task()

    def set_task(self):
        task = self.listbox.get(self.index)
        self.task_entry.insert(0, task)

    def save(self):
        task = self.task_entry.get()
        if task:
            self.listbox.delete(self.index)
            self.listbox.insert(self.index, task)

        else:
            messagebox.showerror('Error', 'Task cannot be empty')

        self.master.destroy()


class ToDoListTest:

    def __init__(self, master: ttk.Window):
        self.master = master
        self.master.geometry('500x600')
        self.master.resizable(False, False)

        self.tasks = TaskManager()

        self.label = ttk.Label(
            self.master, text='To Do List', font='Helvetica 20 bold')
        self.label.pack(pady=10)

        self.task_entry_container = ttk.Frame(master=master, padding=5)
        self.task_entry = ttk.Entry(self.task_entry_container, width=40)
        self.due_date = ttk.DateEntry(
            self.task_entry_container, width=10)

        self.task_entry_container.pack()
        self.task_entry.pack(side='left', padx=2)
        self.due_date.pack(side='right', padx=2)

        self.buttons_container = ttk.Frame(master=master, padding=5)
        self.add_button = ttk.Button(
            self.buttons_container, text='Add Task', style='success.TButton', command=self.add_task, width=10)
        self.drop_button = ttk.Button(
            self.buttons_container, text='Drop Task', style='danger.TButton', command=self.drop, width=10)
        self.update_button = ttk.Button(
            self.buttons_container, text='Update Task', style='info.TButton', width=10, command=self.update)
        self.done_button = ttk.Button(
            self.buttons_container, text='Mark Done', style='warning.TButton', width=10)

        self.add_button.pack(side='left', padx=2)
        self.drop_button.pack(side='left', padx=2)
        self.update_button.pack(side='left', padx=2)
        self.done_button.pack(side='left', padx=2)

        self.buttons_container.pack()

        # ListBox
        self.task_list = tk.Listbox(
            self.master, selectbackground="blue", activestyle='none', fg='red', width=50, font=("Comic Sans MS", 25))
        self.task_list.pack(pady=20, padx=20, side='left', fill='y')
        self.task_list.config(highlightbackground='black',
                              highlightthickness=1, selectbackground='blue')

    def add_task(self):
        task = self.task_entry.get()
        due = self.due_date.entry.get()
        if task and due:
            self.task_entry.delete(0, ttk.END)
            self.due_date.entry.delete(0, ttk.END)

            task = Task(task, due)
            self.tasks.add_task(task)

            self.task_list.insert(0, task.name + ' - ' +
                                  task.due_date)

        elif not task:
            messagebox.showerror('Error', 'Task cannot be empty')

        elif not due:
            messagebox.showerror('Error', 'Due date cannot be empty')

    def drop(self):
        selected_task = self.task_list.curselection()
        if selected_task:
            self.task_list.delete(selected_task)

        else:
            messagebox.showerror('Error', 'Select a task to drop')

    def update(self):
        selected_task = self.task_list.curselection()

        if selected_task:
            self.open_update_window(selected_task[0])

    def open_update_window(self, index: int):
        form_master = ttk.Toplevel(self.master)
        form = TaskUpdateWindow(form_master, self.task_list, index)

        form_master.wait_window(form.master)


if __name__ == '__main__':
    app = ttk.Window('ToDo List', 'vapor')
    ToDoListTest(app)
    app.mainloop()
