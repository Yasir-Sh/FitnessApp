import tkinter as tk
from db_oper.db_api import *
from tkinter import ttk
from app.members.schedule_trainers_view import *
from app.members.schedule_class_view import *

class ScheduleView:
    def __init__(self, root, parent_frame, schedule_frame, member_id):
        self.root = root
        self.parent_frame = parent_frame
        self.schedule_frame = schedule_frame
        self.member_id = member_id
        self.background = '#ebeceb'
        self.qapi = QueryAPI()

        schedule_label = tk.Label(schedule_frame, text="Schedule", font=('Helvetica', 20), anchor='nw', bg=self.background)
        schedule_label.pack(fill='x', padx=(3,0))

        self.schedule_display_frame = tk.Frame(self.schedule_frame, bg=self.background)
        self.schedule_display_frame.pack(fill='x', pady=(15,0))

        self.create_schedule_titles(self.schedule_display_frame)
        self.populate_schedule(self.schedule_display_frame)

    
    def create_schedule_titles(self, schedule_display_frame):
        schedule_display_frame.columnconfigure(0, minsize=110)
        schedule_display_frame.columnconfigure(1, minsize=90)
        schedule_display_frame.columnconfigure(2, minsize=90)

        schedule_label = tk.Label(schedule_display_frame, text='Date', font=('Helvetica', 14), bg=self.background)
        schedule_label.grid(row=0, column=0, sticky='w', padx=(5,0))

        date_label = tk.Label(schedule_display_frame, text='Session', font=('Helvetica', 14), bg=self.background)
        date_label.grid(row=0, column=1, sticky='w')

        time_label = tk.Label(schedule_display_frame, text='Time', font=('Helvetica', 14), bg=self.background)
        time_label.grid(row=0, column=2, sticky='w')

    def populate_schedule(self, schedule_display_frame):
        schedules = self.qapi.get_member_schedule(self.member_id)
        schedules.sort()
        cur_row = 0

        if len(schedules) != 0:
            for schedule in schedules:
                cur_row += 1
                for i in range(0, len(schedule)): 
                    if schedule[i] == None:
                        schedule_label = tk.Label(schedule_display_frame, text='No Use', font=('Helvetica', 12), bg=self.background)
                    elif i == 1:
                        schedule_label = tk.Label(schedule_display_frame, text=str(schedule[i]) + ': 1 on 1', font=('Helvetica', 12), bg=self.background)
                    else:
                        schedule_label = tk.Label(schedule_display_frame, text=schedule[i], font=('Helvetica', 12), bg=self.background)
                    if i == 0:
                        schedule_label.grid(row=cur_row, column=i, sticky='w', padx=(5,0))
                    else:
                        schedule_label.grid(row=cur_row, column=i, sticky='w')

        class_ids = self.qapi.get_member_class_schedule(self.member_id)
        class_ids.sort()

        if len(class_ids) != 0:
            for class_id in class_ids:
                session = self.qapi.get_class_time_by_id(class_id)
                cur_row += 1
                for i in session: 
                    for j in range(0, len(i)):
                        if i[j] == None:
                            schedule_label = tk.Label(schedule_display_frame, text='No Use', font=('Helvetica', 12), bg=self.background)
                        else:
                            schedule_label = tk.Label(schedule_display_frame, text=i[j], font=('Helvetica', 12), bg=self.background)
                        if j == 0:
                            schedule_label.grid(row=cur_row, column=j, sticky='w', padx=(5,0))
                        else:
                            schedule_label.grid(row=cur_row, column=j, sticky='w')
        
        self.buttons_frame = tk.Frame(self.schedule_frame, bg=self.background) 
        self.buttons_frame.pack(expand=True, anchor='se')

        self.button_border = tk.Frame(self.buttons_frame, highlightbackground="Blue",  highlightthickness=1, bd=0) 
        self.button_border.grid(row=0, column=0, padx=(0,10), pady=(0,15))
        edit_button = tk.Button(self.button_border, text="Class", font=('Helvetica', 12), border=0, bg='#0ab6f5', cursor='hand2', command=self.edit_class, anchor='center', activebackground='#66d1f9', width=6)
        edit_button.pack()

        self.button_border = tk.Frame(self.buttons_frame, highlightbackground="Green",  highlightthickness=1, bd=0) 
        self.button_border.grid(row=0, column=1, padx=(0,10), pady=(0,15))
        edit_button = tk.Button(self.button_border, text="Trainer", font=('Helvetica', 12), border=0, bg='#37c876', cursor='hand2', command=self.edit_trainer, anchor='center', activebackground='#27d881', width=6)
        edit_button.pack()

    def destroy_and_repopulate(self, update_trainer):
        update_trainer.destroy()
        self.schedule_display_frame.destroy()
        self.buttons_frame.destroy()
        self.schedule_display_frame = tk.Frame(self.schedule_frame, bg=self.background)
        self.schedule_display_frame.pack(fill='x', pady=(15, 0))

        self.create_schedule_titles(self.schedule_display_frame)
        self.populate_schedule(self.schedule_display_frame)

    def edit_trainer(self):
        update_trainer = tk.Toplevel()
        update_trainer.geometry("%dx%d+%d+%d" % (1150, 400, (self.root.winfo_screenwidth()/2 - 1150/2), (self.root.winfo_screenheight()/2 - 400/2)))
        update_trainer.resizable(width=False, height=False)
        update_trainer.grab_set()
        update_trainer.title("Update Schedule")
        ScheduleTrainer(update_trainer, self.member_id)
        update_trainer.protocol('WM_DELETE_WINDOW', lambda: self.destroy_and_repopulate(update_trainer))

    def edit_class(self):
        update_trainer = tk.Toplevel()
        update_trainer.geometry("%dx%d+%d+%d" % (800, 400, (self.root.winfo_screenwidth()/2 - 800/2), (self.root.winfo_screenheight()/2 - 400/2)))
        update_trainer.resizable(width=False, height=False)
        update_trainer.grab_set()
        update_trainer.title("Update Class")
        ScheduleClass(update_trainer, self.member_id)
        update_trainer.protocol('WM_DELETE_WINDOW', lambda: self.destroy_and_repopulate(update_trainer))

   