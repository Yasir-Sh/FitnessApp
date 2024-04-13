import tkinter as tk
from db_oper.db_api import *

class SearchView:
    def __init__(self, search_frame):
        self.search_frame = search_frame
        self.qapi = QueryAPI()
        self.background = '#ebeceb'

        self.search_entry = tk.Entry(search_frame, font=('Helvetica', 11), width=94)
        self.search_entry.insert(0, 'ex: JohnDoe')
        self.search_entry.bind("<FocusIn>", self.temp_search)
        self.search_entry.grid(column=0, row=0, padx=(0, 12))

        button_border = tk.Frame(search_frame, highlightbackground="Blue",  highlightthickness=1, bd=0) 
        button_border.grid(column=1, row=0, padx=(16,0))
        search_button = tk.Button(button_border, text="Search", font=('Helvetica', 12), border=0, bg='#0ab6f5', cursor='hand2', command=self.search_member, anchor='center', activebackground='#66d1f9')
        search_button.pack(anchor='center')
    
    def temp_search(self, e):
        self.search_entry.delete(0,"end")

    def search_member(self):
        member_username = self.search_entry.get()
        if self.qapi.get_member_username_by_username(member_username) != None:
            member_id = self.qapi.get_member_id_by_username(member_username)
            member_profile = tk.Toplevel()
            member_profile.grab_set()
            member_profile.resizable(width=False, height=False)
            member_profile.title("View Member Profile")
            member_profile.geometry("%dx%d+%d+%d" % (300, 300, (member_profile.winfo_screenwidth()/2 - 300/2), (member_profile.winfo_screenheight()/2 - 300/2)))

            self.goals_frame = tk.Frame(member_profile, bg=self.background,  highlightbackground='#7db6b5', highlightthickness=1)
            self.goals_frame.pack(fill='both', expand=True, padx=5, pady=5)

            goals_label = tk.Label(self.goals_frame, text=f"{member_username}'s Profile", font=('Helvetica', 20), anchor='w',bg=self.background)
            goals_label.pack(fill='x', padx=(3,0))

            self.goals_display_frame = tk.Frame(self.goals_frame, bg=self.background)
            self.goals_display_frame.pack(fill='both', expand=False, pady=(5,0))

            self.create_goals_titles(self.goals_display_frame)
            self.populate_goals(self.goals_display_frame, member_id)

    def create_goals_titles(self, goals_display_frame):
        goals_display_frame.columnconfigure(0, minsize=112)
        goals_display_frame.columnconfigure(1, minsize=113)
        goals_display_frame.columnconfigure(2, minsize=172)
        goals_display_frame.columnconfigure(3, minsize=80)

        goal_label = tk.Label(goals_display_frame, text='Goals', font=('Helvetica', 16), bg=self.background)
        goal_label.grid(row=0, column=0, sticky='w', padx=(3,0))

        target_label = tk.Label(goals_display_frame, text='Targets', font=('Helvetica', 16), bg=self.background)
        target_label.grid(row=0, column=1, sticky='w')

    def populate_goals(self, goals_display_frame, member_id):
        goals = self.qapi.get_all_goals_by_id(member_id)
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
        