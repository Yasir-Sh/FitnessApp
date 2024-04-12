import tkinter as tk
from src.db_oper.db_api import *
from src.app.members.settings_view import *

class EditView:
    def __init__(self, root, parent_frame, profile_frame, dashboard_view, goals_view, member_id):
        self.root = root
        self.parent_frame = parent_frame
        self.profile_frame = profile_frame
        self.member_id = member_id
        self.dashboard_view = dashboard_view
        self.goals_view = goals_view

        edit_label = tk.Label(self.profile_frame, text="Edit Account", font=('Helvetica', 20), anchor='w', bg='#ebeceb')
        edit_label.pack(fill='x', padx=(3,0))

        button_border = tk.Frame(self.profile_frame, highlightbackground="#515559",  highlightthickness=1, bd=0) 
        button_border.place(x=100, y=50)
        edit_button = tk.Button(button_border, text="Edit Prolfile", font=('Helvetica', 14), bg='Gray', activebackground='Light Gray', border=0, width=10, height=1, command=self.settings_page, cursor='hand2')
        edit_button.pack()

        button_border = tk.Frame(self.profile_frame, highlightbackground="Red",  highlightthickness=1, bd=0) 
        button_border.place(x=100, y=120)
        logout_button = tk.Button(button_border, text="Logout", font=('Helvetica', 14), bg='#f07373', activebackground='#f5a3a2', border=0, width=10, height=1, cursor='hand2', command=self.logout)
        logout_button.pack()

    def settings_page(self):
       SettingView(self.root, self.dashboard_view, self.goals_view, self.parent_frame, self.member_id)

    def logout(self):
        self.root.destroy()

    
        