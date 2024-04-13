import tkinter as tk
from db_oper.db_api import *

class GoalsView:
    def __init__(self, root, parent_frame, goals_frame, member_id):
        self.root = root
        self.parent_frame = parent_frame
        self.goals_frame = goals_frame
        self.member_id = member_id
        self.qapi = QueryAPI()
        self.background = '#ebeceb'

        goals_label = tk.Label(goals_frame, text="Goals", font=('Helvetica', 20), anchor='w',bg='#ebeceb')
        goals_label.pack(fill='x', padx=(3,0))

        self.goals_display_frame = tk.Frame(self.goals_frame, bg=self.background)
        self.goals_display_frame.pack(fill='both', expand=False, pady=(15,0))

        self.create_goals_titles(self.goals_display_frame)
        self.populate_goals(self.goals_display_frame)

    def create_goals_titles(self, goals_display_frame):
        goals_display_frame.columnconfigure(0, minsize=112)
        goals_display_frame.columnconfigure(1, minsize=113)
        goals_display_frame.columnconfigure(2, minsize=172)
        goals_display_frame.columnconfigure(3, minsize=80)

        goal_label = tk.Label(goals_display_frame, text='Goals', font=('Helvetica', 16), bg=self.background)
        goal_label.grid(row=0, column=0, sticky='w', padx=(3,0))

        target_label = tk.Label(goals_display_frame, text='Targets', font=('Helvetica', 16), bg=self.background)
        target_label.grid(row=0, column=1, sticky='w')

    def populate_goals(self, goals_display_frame):
        goals = self.qapi.get_all_goals_by_id(self.member_id)
        goals.sort()
        cur_row = 0

        if len(goals) != 0:
            for goal in goals:
                cur_row += 1
                for i in range(1, len(goal)): 
                    if goal[i] == None:
                        goal_label = tk.Label(goals_display_frame, text='N/A', font=('Helvetica', 12), bg=self.background)
                    else:
                        goal_label = tk.Label(goals_display_frame, text=goal[i], font=('Helvetica', 12), bg=self.background)
                    goal_label.grid(row=cur_row, column=i-1, sticky='w', padx=(3,0))

    def destroy_and_repopulate(self):
        self.goals_display_frame.destroy()
        self.goals_display_frame = tk.Frame(self.goals_frame, bg=self.background)
        self.goals_display_frame.pack(fill='both', expand=False, pady=(15,0))

        self.create_goals_titles(self.goals_display_frame)
        self.populate_goals(self.goals_display_frame)

        