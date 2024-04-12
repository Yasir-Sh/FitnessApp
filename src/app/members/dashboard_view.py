import tkinter as tk
from src.db_oper.db_api import *

class DashboardView:
    def __init__(self, root, parent_frame, dashboard_frame, member_id) -> None:
        self.root = root
        self.parent_frame = parent_frame
        self.dashboard_frame = dashboard_frame
        self.member_id = member_id
        self.qapi = QueryAPI()
        self.background = '#ebeceb'

        dashboard_label = tk.Label(dashboard_frame, text=self.qapi.get_member_username_by_id(self.member_id)[0] + "'s Dashboard", font=('Helvetica', 20), anchor='w',bg='#ebeceb')
        dashboard_label.pack(fill='x', padx=(3,0))

        self.dashboard_display_frame = tk.Frame(self.dashboard_frame, bg=self.background)
        self.dashboard_display_frame.pack(fill='both', expand=False, pady=(15,0))

        self.create_dashboard_titles(self.dashboard_display_frame)
        self.populate_dashboard(self.dashboard_display_frame)

    def create_dashboard_titles(self, dashboard_display_frame):
        dashboard_display_frame.columnconfigure(0, minsize=112)
        dashboard_display_frame.columnconfigure(1, minsize=113)
        dashboard_display_frame.columnconfigure(2, minsize=172)
        dashboard_display_frame.columnconfigure(3, minsize=80)

        exercise_label = tk.Label(dashboard_display_frame, text='Exercise', font=('Helvetica', 16), bg=self.background)
        exercise_label.grid(row=0, column=0, sticky='w', padx=(3,0))

        exercise_label = tk.Label(dashboard_display_frame, text='Routine', font=('Helvetica', 16), bg=self.background)
        exercise_label.grid(row=0, column=1, sticky='w')

        exercise_label = tk.Label(dashboard_display_frame, text='Personal Best', font=('Helvetica', 16), bg=self.background)
        exercise_label.grid(row=0, column=2, sticky='w')

        exercise_label = tk.Label(dashboard_display_frame, text='Body Weight', font=('Helvetica', 16), bg=self.background)
        exercise_label.grid(row=0, column=3, sticky='e')

    def populate_dashboard(self, dashboard_display_frame):
        exercises = self.qapi.get_all_exercises_by_id(self.member_id)
        exercises.sort()
        cur_row = 0

        if len(exercises) != 0:
            for exercise in exercises:
                cur_row += 1
                for i in range(1, len(exercise)): 
                    if exercise[i] == None:
                        exercise_label = tk.Label(dashboard_display_frame, text='N/A', font=('Helvetica', 12), bg=self.background)
                    elif i == 4:
                        exercise_label = tk.Label(dashboard_display_frame, text=str(exercise[i]) + " kgs", font=('Helvetica', 12), bg=self.background)
                    else:
                        exercise_label = tk.Label(dashboard_display_frame, text=exercise[i], font=('Helvetica', 12), bg=self.background)
                    exercise_label.grid(row=cur_row, column=i-1, sticky='w', padx=(3,0))

    def destroy_and_repopulate(self):
        self.dashboard_display_frame.destroy()
        self.dashboard_display_frame = tk.Frame(self.dashboard_frame, bg=self.background)
        self.dashboard_display_frame.pack(fill='both', expand=False, pady=(15,0))

        self.create_dashboard_titles(self.dashboard_display_frame)
        self.populate_dashboard(self.dashboard_display_frame)


        