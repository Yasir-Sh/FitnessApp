import tkinter as tk
import src.app.members.edit_view as ev
import src.app.members.dashboard_view as dv
import src.app.members.goals_view as gv
from src.app.members.schedule_view import *

class MembersView:
    def __init__(self, root, member_id):
        self.root = root
        self.root.geometry("%dx%d+%d+%d" % (900, 700, (self.root.winfo_screenwidth()/2 - 900/2), (self.root.winfo_screenheight()/2 - 700/2)))
        self.member_id = member_id
        
        parent_frame = tk.Frame(self.root)
        parent_frame.pack(fill='both', expand=True)

        parent_frame.columnconfigure(0, weight=1)
        parent_frame.rowconfigure(0, weight=2)
        parent_frame.columnconfigure(1, weight=2)
        parent_frame.rowconfigure(1, weight=1)

        dashboard_frame = tk.Frame(parent_frame, width=650, height=450, bg='#ebeceb', highlightthickness=1, highlightbackground='Light Gray')
        dashboard_frame.grid(row=0, column=0, sticky='nsew', padx=(10,5), pady=(10,5))

        goals_frame = tk.Frame(parent_frame, width=650, height=250, bg='#ebeceb', highlightthickness=1, highlightbackground='Light Gray')
        goals_frame.grid(row=1, column=0, sticky='nsew',  padx=(10,5), pady=(5,10))

        schedule_frame = tk.Frame(parent_frame, width=250, height=450, bg='#ebeceb', highlightthickness=1, highlightbackground='Light Gray')
        schedule_frame.grid(row=0, column=1, sticky='nsew', padx=(5,10), pady=(10,5))
        
        profile_frame = tk.Frame(parent_frame, width=250, height=250, bg='#ebeceb', highlightthickness=1, highlightbackground='Light Gray')
        profile_frame.grid(row=1, column=1, sticky='nsew', padx=(5,10), pady=(5,10))

        dashboard_view = dv.DashboardView(root, parent_frame, dashboard_frame, self.member_id)

        goals_view = gv.GoalsView(root, parent_frame, goals_frame, self.member_id)

        ScheduleView(root, parent_frame, schedule_frame, self.member_id)

        ev.EditView(root, parent_frame, profile_frame, dashboard_view, goals_view, self.member_id)




