import tkinter as tk
from src.db_oper.db_api import *
from tkinter import ttk
from src.app.trainers.search_view import *
from src.app.trainers.availability_view import *
from src.app.trainers.assignment_view import *
from src.app.registration.registration import *


class TrainersView:
    def __init__(self, root, trainer_id):
        self.root = root
        self.root.geometry("%dx%d+%d+%d" % (900, 700, (self.root.winfo_screenwidth()/2 - 900/2), (self.root.winfo_screenheight()/2 - 700/2)))
        self.trainer_id = trainer_id
        self.qapi = QueryAPI()
        self.background = '#ebeceb'

        trainer_view_frame = tk.Frame(self.root, bg=self.background, highlightbackground='#7db6b5', highlightthickness=1)
        trainer_view_frame.pack(fill='both', expand=True, padx=10, pady=10)

        search_label = tk.Label(trainer_view_frame, text="Search Member Profiles", font=('Helvetica', 20), anchor='w', bg=self.background)
        search_label.pack(fill='x', padx=(15,0), pady=10)

        search_frame = tk.Frame(trainer_view_frame, bg=self.background)
        search_frame.pack()
        SearchView(search_frame)

        seperator = ttk.Separator(trainer_view_frame, orient='horizontal')
        seperator.pack(fill='x', pady=(20,0))

        availability_label = tk.Label(trainer_view_frame, text="Trainer Availability", font=('Helvetica', 20), anchor='w', bg=self.background)
        availability_label.pack(fill='x', padx=(15,0), pady=10)

        availability_frame = tk.Frame(trainer_view_frame, bg=self.background, height=200)
        availability_frame.pack(fill='x')
        AvailabilityView(availability_frame, self.trainer_id)

        seperator = ttk.Separator(trainer_view_frame, orient='horizontal')
        seperator.pack(fill='x', pady=(10,0))

        assignments_label = tk.Label(trainer_view_frame, text="Trainer Assignments", font=('Helvetica', 20), anchor='w', bg=self.background)
        assignments_label.pack(fill='x', padx=(15,0), pady=(10,5))

        assignments_frame = tk.Frame(trainer_view_frame, bg=self.background)
        assignments_frame.pack(fill='x', padx=(15,0))
        AssignmentView(assignments_frame, self.trainer_id)

        buttons_frame = tk.Frame(trainer_view_frame, bg=self.background)
        buttons_frame.pack(fill='both', expand=True)

        buttons_frame.columnconfigure(0, weight=400)
        buttons_frame.rowconfigure(0, weight=400)

        button_border = tk.Frame(buttons_frame, highlightbackground="Red",  highlightthickness=1, bd=0) 
        button_border.grid(column=1, row=0, padx=10, pady=5, sticky='se')
        logout_button = tk.Button(button_border, text="Logout", font=('Helvetica', 12), border=0, bg='#e76e72', cursor='hand2', anchor='center', activebackground='#ee9a9d', command=self.logout)
        logout_button.pack()
    
    def logout(self):
        self.root.destroy()




    

        




