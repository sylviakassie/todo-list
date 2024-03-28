import os
import os.path
import pickle
import ttkbootstrap as ttk
import tkinter as tk
from tkinter import messagebox
from task import Task, TaskManager
from datetime import datetime


class TaskUpdateWindow:
    def __init__(self, master: ttk.Toplevel, listbox: tk.Listbox, index: int, taskmanager: TaskManager):
        self.master = master
        self.master.geometry('300x300')
        self.master.title('Update Task')
        self.master.resizable(False, False)
        self.listbox = listbox
        self.index = index
        self.taskmanager = taskmanager
        self.task = taskmanager._get_task(index)

        self.task_name_label = ttk.Label(
            self.master, text='Task Name', font=('Helvetica', 12))
        self.task_entry = ttk.Entry(self.master, width=20)
        self.due_date_label = ttk.Label(
            self.master, text='Due Date', font=('Helvetica', 12))
        self.due_date = ttk.DateEntry(
            self.master, width=10, startdate=self.task.due_date)
        self.save_button = ttk.Button(
            self.master, text='Save', style='success.TButton', command=self.save)

        # Positions using place
        self.task_name_label.place(x=10, y=14)
        self.task_entry.place(x=100, y=10)
        self.due_date_label.place(x=10, y=74)
        self.due_date.place(x=100, y=70)
        self.save_button.place(x=150, y=120)

        self.task_entry.insert(0, self.task.name)

    def save(self):
        task = self.task_entry.get()
        due = self.due_date.entry.get()
        if task and due:
            self.listbox.delete(self.index)
            self.listbox.insert(self.index, task + ' - ' + due)
            self.listbox.selection_clear(self.index)
            self.taskmanager.update_task(self.index, Task(
                task, datetime.strptime(due, "%x")))

        else:
            messagebox.showerror('Error', 'Task cannot be empty')

        self.master.destroy()


class ToDoListGUI:

    def __init__(self, master: ttk.Window):
        self.app_file_path = os.path.dirname(__file__)
        self.main_path = os.path.dirname(self.app_file_path)

        self.master = master
        self.master.geometry('500x600')
        self.master.resizable(False, False)

        self.menu = ttk.Menu(self.master)

        self.tasks = TaskManager()

        self.label = ttk.Label(
            self.master, text='To Do List', font='Helvetica 20 bold')
        self.label.pack(pady=10)

        self.task_entry_container = ttk.Frame(master=master, padding=5)
        self.task_entry = ttk.Entry(self.task_entry_container, width=40)
        self.due_date = ttk.DateEntry(
            self.task_entry_container, width=10)

        self.task_entry_container.pack(pady=10)
        self.task_entry.pack(side='left', padx=2)
        self.due_date.pack(side='right', padx=2)

        self.buttons_container = ttk.Frame(master=master, padding=5)
        self.add_button = ttk.Button(
            self.buttons_container, text='Add Task', style='success.TButton', command=self.add_task, width=10)
        self.drop_button = ttk.Button(
            self.buttons_container, text='Drop Task', style='danger.TButton', command=self.drop, width=10, state='disabled')
        self.update_button = ttk.Button(
            self.buttons_container, text='Update Task', style='info.TButton', width=10, command=self.update, state='disabled')
        self.done_button = ttk.Button(
            self.buttons_container, text='Task Done', style='warning.TButton', width=10, command=self.mark_done, state='disabled')

        self.add_button.pack(side='left', padx=2)
        self.drop_button.pack(side='left', padx=2)
        self.update_button.pack(side='left', padx=2)
        self.done_button.pack(side='left', padx=2)

        self.buttons_container.pack(fill='x', pady=10, padx=20)

        # ListBox
        self.task_list = tk.Listbox(self.master, fg="red", activestyle='none',
                                    width=50, font=("Comic Sans MS", 25))
        self.task_list.pack(pady=10, padx=20, side='left', fill='y')
        self.task_list.bind('<<ListboxSelect>>', self.on_select)

        self.load_from_file()
        self.master.protocol('WM_DELETE_WINDOW', self.save_to_file)

    def on_select(self, event):
        selected_task = self.task_list.get(self.task_list.curselection())

        if selected_task:
            task = self.tasks._get_task(self.task_list.curselection()[0])
            self.drop_button.config(state='normal')
            self.update_button.config(state='normal')
            self.done_button.config(state='normal')

            if task.is_done:
                self.done_button.config(text='Uncheck Task', width=11)
                self.update_button.config(state='disable')
            elif not task.is_done:
                self.done_button.config(text='Task Done')

    def add_task(self):
        task = self.task_entry.get()
        due = self.due_date.entry.get()

        if task and due:
            self.task_entry.delete(0, ttk.END)

            due = datetime.strptime(due, "%x")
            task = Task(task, due)
            self.tasks.add_task(task)

            self.task_list.insert(ttk.END, task.name + ' - ' +
                                  task.due_date.strftime('%x'))

        elif not task:
            messagebox.showerror('Error', 'Task cannot be empty')

        elif not due:
            messagebox.showerror('Error', 'Due date cannot be empty')

    def drop(self):
        selected_task = self.task_list.curselection()
        if selected_task:
            self.task_list.delete(selected_task)
            self.tasks.delete_task(self.tasks._get_task(selected_task[0]))

        else:
            messagebox.showerror('Error', 'Select a task to drop')

    def mark_done(self):
        selected_task = self.task_list.curselection()
        if selected_task:
            task = self.tasks._get_task(selected_task[0])

            if task.is_done:
                task_entry = self.task_list.get(selected_task)
                self.task_list.delete(selected_task)
                new_task_entry = task_entry[2:]
                self.task_list.insert(selected_task[0], new_task_entry)
                self.task_list.itemconfig(selected_task, fg='#f288d4')
                self.task_list.selection_clear(selected_task)
                task.is_done = False
                self.done_button.config(text='Task Done', width=11)
                self.update_button.config(state='normal')

            elif not task.is_done:
                task_entry = self.task_list.get(selected_task)
                self.task_list.delete(selected_task)
                task_entry = '\u2713 ' + task_entry
                self.task_list.insert(selected_task, task_entry)
                self.task_list.itemconfig(selected_task, fg='gray')
                self.task_list.selection_clear(selected_task)
                task.is_done = True
                self.done_button.config(text='Task Done')

    def update(self):
        selected_task = self.task_list.curselection()

        if selected_task:
            self.open_update_window(selected_task[0])

    def open_update_window(self, index: int):
        form_master = ttk.Toplevel(self.master)
        form = TaskUpdateWindow(form_master, self.task_list, index, self.tasks)

        form_master.wait_window(form.master)

    def save_to_file(self):
        file_path = os.path.join(self.main_path, 'data', 'app_data')
        file = 'app_data.dat'

        for task in self.tasks.get_tasks():
            if task.is_done:
                self.tasks.delete_task(task)

        if os.path.isdir(file_path):

            with open(os.path.join(file_path, file), 'wb') as f:
                pickle.dump(self.tasks, file=f)

        else:

            os.makedirs(file_path)
            with open(os.path.join(file_path, file), 'wb') as f:
                pickle.dump(self.tasks.get_tasks(), file=f)

        self.master.destroy()

    def load_from_file(self):
        file_path = os.path.join(self.main_path, 'data', 'app_data')
        file = 'app_data.dat'

        if os.path.exists(file_path) and os.path.isfile(os.path.join(file_path, file)):
            with open(os.path.join(file_path, file), 'rb') as f:
                self.tasks: TaskManager = pickle.load(f)

                for task in self.tasks.get_tasks():
                    if task.is_done:
                        self.task_list.insert(ttk.END, '\u2713 ' + task.name +
                                              ' - ' + task.due_date.strftime('%x'))
                        self.task_list.itemconfig(ttk.END, fg='gray')
                    elif not task.is_done:
                        self.task_list.insert(ttk.END, task.name + ' - ' +
                                              task.due_date.strftime('%x'))

        else:
            pass


if __name__ == '__main__':
    app = ttk.Window('ToDo List', 'vapor')
    ToDoListGUI(app)
    app.mainloop()
