import tkinter as tk
from tkinter import ttk
from tkinter import simpledialog
from src.db_oper.db_api import *

class SettingView:
    def __init__(self, root, dashboard_view, goals_view, parent_frame, member_id) -> None:
        self.root = root
        self.member_id = member_id
        self.qapi = QueryAPI()
        self.settings_color='#eff0f1'
        self.parent_frame = parent_frame
        self.goals_view = goals_view
        self.dashboard_view = dashboard_view

        edit_window = tk.Toplevel()
        edit_window.geometry("%dx%d+%d+%d" % (900, 600, (self.root.winfo_screenwidth()/2 - 900/2), (self.root.winfo_screenheight()/2 - 600/2)))
        edit_window.resizable(width=False, height=False)
        edit_window.grab_set()
        edit_window.title("Update Home Page")
        edit_window.protocol('WM_DELETE_WINDOW', lambda: self.back_to_dashboard(edit_window))

        settings_frame = tk.Frame(edit_window, bg=self.settings_color, highlightbackground='#7db6b5', highlightthickness=1)
        settings_frame.pack(fill='both', expand=True, padx=10, pady=10)

        self.account_panel(settings_frame)
        seperator = ttk.Separator(settings_frame, orient='horizontal')
        seperator.pack(fill='x', pady=(20,0))

        self.dashboard_panel(settings_frame)
        seperator = ttk.Separator(settings_frame, orient='horizontal')
        seperator.pack(fill='x', pady=(20,0))

        self.goals_panel(settings_frame)

    def back_to_dashboard(self, edit_window):
        edit_window.destroy()
        self.dashboard_view.destroy_and_repopulate()
        self.goals_view.destroy_and_repopulate()
    
    def account_panel(self, settings_frame):
        edit_account_label = tk.Label(settings_frame,text="Edit Account", font=('Helvetica', 24), anchor='w', bg=self.settings_color)
        edit_account_label.pack(fill='x', pady=15, padx=15)

        username_label = tk.Label(settings_frame, text="Username:", font=('Helvetica', 14), anchor='w', bg=self.settings_color)
        username_label.pack(fill='x', padx=15, pady=(0,15))

        username =  tk.StringVar()
        username.set(self.qapi.get_member_username_by_id(self.member_id))
        username_button = tk.Button(settings_frame, text=username.get(), textvariable=username, font=('Helvetica', 14), border=0, command=lambda: self.update_username(username), cursor='hand2', bg=self.settings_color)
        username_button.place(x=108, y=69)
        
        edit_password_label = tk.Label(settings_frame, text="Password:", font=('Helvetica', 14), anchor='sw', bg=self.settings_color)
        edit_password_label.pack(fill='x', padx=15, pady=(0,15) )

        password = tk.StringVar()
        password.set(self.qapi.get_member_password_by_id(self.member_id))
        password_button = tk.Button(settings_frame, text=password.get(), textvariable=password, font=('Helvetica', 14), border=0, command= lambda: self.update_password(password), cursor='hand2', bg=self.settings_color)
        password_button.place(x=105, y=112)

    def dashboard_panel(self, settings_frame):
        edit_dashboard_label = tk.Label(settings_frame, text="Edit Dashboard", font=('Helvetica', 24), anchor='sw', bg=self.settings_color)
        edit_dashboard_label.pack(fill='x', pady=15, padx=15)

        add_exercise_frame = tk.Frame(settings_frame, bg=self.settings_color)
        add_exercise_frame.pack(fill='x', padx=(15,0), pady=(0, 15))

        exercise_label = tk.Label(add_exercise_frame, font=('Helvetica', 14), text='Exercise:', bg=self.settings_color)
        exercise_label.grid(column=0, row=0, padx=(0,3))
        self.exercise_entry = tk.Entry(add_exercise_frame, font=('Helvetica', 12), width=8, bg='#d1d4d7')
        self.exercise_entry.grid(column=1, row=0)

        routine_label = tk.Label(add_exercise_frame, font=('Helvetica', 14), text='Routine:', bg=self.settings_color)
        routine_label.grid(column=2, row=0, padx=(0,3))
        self.routine_entry = tk.Entry(add_exercise_frame, font=('Helvetica', 12), width=8, bg='#d1d4d7')
        self.routine_entry.grid(column=3, row=0)
                            
        personal_best_label = tk.Label(add_exercise_frame, font=('Helvetica', 14), text='Personal Best:', bg=self.settings_color)
        personal_best_label.grid(column=4, row=0, padx=(0,3))
        self.personal_best_entry = tk.Entry(add_exercise_frame, font=('Helvetica', 12), width=8, bg='#d1d4d7')
        self.personal_best_entry.grid(column=5, row=0)

        body_weight_label = tk.Label(add_exercise_frame, font=('Helvetica', 14), text='Body Weight:', bg=self.settings_color)
        body_weight_label.grid(column=6, row=0, padx=(0,3))
        self.body_weight_entry = tk.Entry(add_exercise_frame, font=('Helvetica', 12), width=8, bg='#d1d4d7')
        self.body_weight_entry.grid(column=7, row=0)

        button_border = tk.Frame(add_exercise_frame, highlightbackground="Green",  highlightthickness=1, bd=0) 
        button_border.grid(column=8, row=0, padx=(15,0))
        add_button = tk.Button(button_border, text="A", font=('Helvetica', 12), border=0, bg='#37c876', cursor='hand2', command=self.add_exercise, anchor='center', activebackground='#27d881')
        add_button.pack(anchor='center')

        button_border = tk.Frame(add_exercise_frame, highlightbackground="Blue",  highlightthickness=1, bd=0) 
        button_border.grid(column=9, row=0, padx=(15,0))
        update_button = tk.Button(button_border, text="U", font=('Helvetica', 12), border=0, bg='#0ab6f5', cursor='hand2', command=self.update_exercise, anchor='center', activebackground='#66d1f9')
        update_button.pack(anchor='center')

        button_border = tk.Frame(add_exercise_frame, highlightbackground="Red",  highlightthickness=1, bd=0) 
        button_border.grid(column=10, row=0, padx=(15,0),)
        delete_button = tk.Button(button_border, text="D", font=('Helvetica', 12), border=0, bg='#e76e72', cursor='hand2', command=self.delete_exercise_group, anchor='center', activebackground='#ee9a9d')
        delete_button.pack(anchor='center')

        self.status = tk.StringVar()
        self.status.set('Status: ')
        status_label = tk.Label(settings_frame, textvariable=self.status, font=('Helvetica', 14), anchor='w', bg=self.settings_color)
        status_label.pack(fill='x', padx=(15,0), pady=(0,10))

    def goals_panel(self, settings_frame):
        edit_goals_label = tk.Label(settings_frame, text="Edit Goals", font=('Helvetica', 24), anchor='sw', bg=self.settings_color)
        edit_goals_label.pack(fill='x', pady=15, padx=15)

        add_goals_frame = tk.Frame(settings_frame, bg=self.settings_color)
        add_goals_frame.pack(fill='x', padx=(15,0), pady=(0, 15))

        goal_label = tk.Label(add_goals_frame, font=('Helvetica', 14), text='Goal:', bg=self.settings_color)
        goal_label.grid(column=0, row=0, padx=(0,3))
        self.goal_entry = tk.Entry(add_goals_frame, font=('Helvetica', 12), width=8, bg='#d1d4d7')
        self.goal_entry.grid(column=1, row=0)

        target_label = tk.Label(add_goals_frame, font=('Helvetica', 14), text='Target:', bg=self.settings_color)
        target_label.grid(column=2, row=0, padx=(15,3))
        self.target_entry = tk.Entry(add_goals_frame, font=('Helvetica', 12), width=8, bg='#d1d4d7')
        self.target_entry.grid(column=3, row=0)

        button_border = tk.Frame(add_goals_frame, highlightbackground="Green",  highlightthickness=1, bd=0) 
        button_border.grid(column=4, row=0, padx=(453,0))
        add_button = tk.Button(button_border, text="A", font=('Helvetica', 12), border=0, bg='#37c876', cursor='hand2', command=self.add_goal, anchor='center', activebackground='#27d881')
        add_button.pack(anchor='center')

        button_border = tk.Frame(add_goals_frame, highlightbackground="Blue",  highlightthickness=1, bd=0) 
        button_border.grid(column=5, row=0, padx=(15,0))
        update_button = tk.Button(button_border, text="U", font=('Helvetica', 12), border=0, bg='#0ab6f5', cursor='hand2', command=self.update_goal, anchor='center', activebackground='#66d1f9')
        update_button.pack(anchor='center')

        button_border = tk.Frame(add_goals_frame, highlightbackground="Red",  highlightthickness=1, bd=0) 
        button_border.grid(column=6, row=0, padx=(15,0))
        delete_button = tk.Button(button_border, text="D", font=('Helvetica', 12), border=0, bg='#e76e72', cursor='hand2', command=self.delete_goal, anchor='center', activebackground='#ee9a9d')
        delete_button.pack(anchor='center')

        self.goal_status = tk.StringVar()
        self.goal_status.set('Status: ')
        status_label = tk.Label(settings_frame, textvariable=self.goal_status, font=('Helvetica', 14), anchor='w', bg=self.settings_color)
        status_label.pack(fill='x', padx=(15,0), pady=(0,10))

    def update_username(self, username):
        new_username = simpledialog.askstring(title="Update Username", prompt="What's your new username?\t\t\t\t",)
        if new_username != None and len(new_username.strip()) != 0:
            if self.qapi.get_member_username_by_username(new_username) == None:
                self.qapi.update_member_username_by_id(new_username, self.member_id)
                username.set(new_username)

    def update_password(self, password):
        new_password = simpledialog.askstring(title="Update Password", prompt="What's your new password?\t\t\t\t",)
        if new_password != None and len(new_password.strip()) != 0:
            self.qapi.update_member_password_by_id(new_password, self.member_id)
            password.set(new_password)

    def add_exercise(self):
        exercise = self.exercise_entry.get().strip()
        routine = self.routine_entry.get().strip()
        personal_best = self.personal_best_entry.get().strip()
        body_weight = self.body_weight_entry.get().strip()

        if exercise == '' or routine == '':
            self.status.set('Status: Add unsuccessful. Missing fields exercise/ routine.')
        elif self.qapi.get_exercise_by_exercise(self.member_id, exercise) != None:   
            self.status.set(f'Status: Add unsuccessful. Exercise \'{exercise}\' already exists, try UPDATE instead.')
        else:
            self.qapi.add_exercise_entry_by_id(self.member_id, exercise, routine, personal_best, body_weight)
            self.exercise_entry.delete(0, 'end')
            self.routine_entry.delete(0, 'end')
            self.personal_best_entry.delete(0, 'end')
            self.body_weight_entry.delete(0, 'end')
            self.status.set(f'Status: Exercise \'{exercise}, {routine}\' successfullly added.')

    def delete_exercise_group(self):
        exercise = self.exercise_entry.get().strip()
        if exercise == '':
            self.status.set('Status: Delete Unsuccessful. Missing field exercise.')
        elif self.qapi.get_exercise_by_exercise(self.member_id, exercise) == None:
            self.status.set(f'Status: Delete Unsuccessful. Exercise \'{exercise}\' not found.')
        else:
            self.qapi.delete_exercise_by_exercise(self.member_id, exercise)
            self.exercise_entry.delete(0, 'end')
            self.routine_entry.delete(0, 'end')
            self.personal_best_entry.delete(0, 'end')
            self.body_weight_entry.delete(0, 'end')
            self.status.set(f'Status: Exercise \'{exercise} \' successfully deleted.')

    def update_exercise(self):
        exercise = self.exercise_entry.get().strip()
        routine = self.routine_entry.get().strip()
        personal_best = self.personal_best_entry.get().strip()
        body_weight = self.body_weight_entry.get().strip()

        if exercise == '' or routine == '':
            self.status.set('Status: Update unsuccessful. Missing fields exercise/ routine.')
        elif self.qapi.get_exercise_by_exercise(self.member_id, exercise) == None:
            self.status.set(f'Status: Update Unsuccessful. Exercise \'{exercise}\' not found.')
        else:
            self.qapi.update_exercise_by_exercise(self.member_id, exercise, routine, personal_best, body_weight)
            self.exercise_entry.delete(0, 'end')
            self.routine_entry.delete(0, 'end')
            self.personal_best_entry.delete(0, 'end')
            self.body_weight_entry.delete(0, 'end')
            self.status.set(f'Status: Exercise \'{exercise}\' successfully updated.')

    def add_goal(self):
        goal = self.goal_entry.get()
        target = self.target_entry.get()

        if goal == '' or target == '':
            self.goal_status.set('Status: Add unsuccessful. Missing fields goal/ target.')
        elif self.qapi.get_goal_by_goal(self.member_id, goal) != None:
            self.goal_status.set(f'Status: Add unsuccessful. Goal \' {goal}\' already exists, try UPDATE instead.')
        else:
            self.qapi.add_goal_by_goal(self.member_id, goal, target)
            self.goal_entry.delete(0, 'end')
            self.target_entry.delete(0, 'end')
            self.goal_status.set(f'Status: Goal \'{goal}, {target}\' successfully added')
            

    def delete_goal(self):
        goal = self.goal_entry.get()
        if goal == '':
            self.goal_status.set('Status: Delete unsuccessful. Missing field goal.')
        elif self.qapi.get_goal_by_goal(self.member_id, goal) == None:
            self.goal_status.set(f'Status: Delete unsuccessful. Goal \'{goal}\' not found.')
        else:
            self.qapi.delete_goal_by_goal(self.member_id, goal)
            self.goal_entry.delete(0, 'end')
            self.target_entry.delete(0, 'end')
            self.goal_status.set(f'Status: Goal \'{goal}\' successfully deleted')

    def update_goal(self):
        goal = self.goal_entry.get()
        target = self.target_entry.get()

        if goal == '' or target == '':
            self.goal_status.set('Status: Update unsuccessful. Missing fields goal/ target.')
        elif self.qapi.get_goal_by_goal(self.member_id, goal) == None:
            self.goal_status.set(f'Status: Update unsuccessful. Goal \'{goal}\' not found.')
        else:
            self.qapi.update_goal_by_goal(self.member_id, goal, target)
            self.goal_entry.delete(0, 'end')
            self.target_entry.delete(0, 'end')
            self.goal_status.set(f'Status: Goal \'{goal}\' successfully updated')