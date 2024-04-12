import tkinter as tk
from src.db_oper.db_api import *

class AssignmentView:
    def __init__(self, assignment_frame, trainer_id):
        self.assignment_frame = assignment_frame
        self.trainer_id = trainer_id
        self.qapi = QueryAPI()
        self.background = '#ebeceb'

        self.create_titles()
        self.populate_assignments()

    def create_titles(self):

        self.assignment_frame.columnconfigure(0, minsize=80) #class id
        self.assignment_frame.columnconfigure(1, minsize=80) # trainer
        self.assignment_frame.columnconfigure(2, minsize=80) # name
        self.assignment_frame.columnconfigure(3, minsize=100) # day
        self.assignment_frame.columnconfigure(4, minsize=80) #start
        self.assignment_frame.columnconfigure(5, minsize=80) #end

        class_label = tk.Label(self.assignment_frame, text='ClassId', font=('Helvetica', 14), bg=self.background)
        class_label.grid(row=0, column=0, sticky='w')

        trainer_label = tk.Label(self.assignment_frame, text='Trainer', font=('Helvetica', 14), bg=self.background)
        trainer_label.grid(row=0, column=1, sticky='w')

        trainer_label = tk.Label(self.assignment_frame, text='Class', font=('Helvetica', 14), bg=self.background)
        trainer_label.grid(row=0, column=2, sticky='w')

        day_label = tk.Label(self.assignment_frame, text='Day', font=('Helvetica', 14), bg=self.background)
        day_label.grid(row=0, column=3, sticky='w')

        start_label = tk.Label(self.assignment_frame, text='Start', font=('Helvetica', 14), bg=self.background)
        start_label.grid(row=0, column=4, sticky='w')

        end_label = tk.Label(self.assignment_frame, text='End', font=('Helvetica', 14), bg=self.background)
        end_label.grid(row=0, column=5, sticky='w')

    def populate_assignments(self):
        schedules = self.qapi.get_all_classess()
        schedules.sort()
        cur_row = 0

        if len(schedules) != 0:
            for schedule in schedules:
                cur_row += 1
                for i in range(0, len(schedule)): 
                    if schedule[i] == None:
                        schedule_label = tk.Label(self.assignment_frame, text='No Use', font=('Helvetica', 12), bg=self.background)
                    elif i == 1:
                        schedule_label = tk.Label(self.assignment_frame, text=self.qapi.get_trainer_username_by_id(schedule[i]), font=('Helvetica', 12), bg=self.background)
                    else:
                        schedule_label = tk.Label(self.assignment_frame, text=schedule[i], font=('Helvetica', 12), bg=self.background)
                    if i == 0:
                        schedule_label.grid(row=cur_row, column=i, sticky='w', padx=(3,0))
                    else:
                        schedule_label.grid(row=cur_row, column=i, sticky='w')


        
        