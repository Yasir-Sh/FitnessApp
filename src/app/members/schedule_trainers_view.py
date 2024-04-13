import tkinter as tk 
from db_oper.db_api import *
from tkinter import ttk
import re

class ScheduleTrainer:
    def __init__(self, update_trainer, member_id):
        self.update_trainer = update_trainer
        self.background = '#ebeceb'
        self.qapi = QueryAPI()
        self.member_id = member_id

        self.trainer_frame = tk.Frame(self.update_trainer, bg=self.background,  highlightbackground='#7db6b5', highlightthickness=1)
        self.trainer_frame.pack(fill='both', expand=True, padx=15, pady=15)

        self.trainer_schedule_label = tk.Label(self.trainer_frame, text="Trainer's Availability", font=('Helvetica', 20), anchor='w', bg=self.background)
        self.trainer_schedule_label.pack(fill='x', padx=(15,0), pady=10)

        self.trainer_schedule_frame = tk.Frame(self.trainer_frame, bg=self.background)
        self.trainer_schedule_frame.pack(fill='x', padx=(15,0))

        self.create_trainer_titles()
        self.populate_trainer()

        self.seperator = ttk.Separator(self.trainer_frame, orient='horizontal')
        self.seperator.pack(fill='x', pady=(10,0))

        self.edit_trainer_label = tk.Label(self.trainer_frame, text="Select Trainer", font=('Helvetica', 20), anchor='w', bg=self.background)
        self.edit_trainer_label.pack(fill='x', padx=(15,0), pady=10)

        self.add_frame = tk.Frame(self.trainer_frame, bg=self.background)
        self.add_frame.pack(fill='x', padx=(15,0))

        session_label = tk.Label(self.add_frame, font=('Helvetica', 14), text='SessionId:', bg=self.background)
        session_label.grid(column=0, row=0, padx=(0,3))
        self.session_entry = tk.Entry(self.add_frame, font=('Helvetica', 12), width=10, bg='#d1d4d7')
        self.session_entry.insert(2, 'ex. training')
        self.session_entry.bind("<FocusIn>", self.clear_session)
        self.session_entry.grid(column=1, row=0)  

        trainer_label = tk.Label(self.add_frame, font=('Helvetica', 14), text='Trainer:', bg=self.background)
        trainer_label.grid(column=2, row=0, padx=(0,3))
        self.trainer_entry = tk.Entry(self.add_frame, font=('Helvetica', 12), width=10, bg='#d1d4d7')
        self.trainer_entry.insert(0, 'ex. yasir')
        self.trainer_entry.bind("<FocusIn>", self.clear_trainer)
        self.trainer_entry.grid(column=3, row=0)                 

        day_label = tk.Label(self.add_frame, font=('Helvetica', 14), text='Day:', bg=self.background)
        day_label.grid(column=4, row=0, padx=(0,3))
        self.day_entry = tk.Entry(self.add_frame, font=('Helvetica', 12), width=12, bg='#d1d4d7')
        self.day_entry.insert(0, 'ex. 2024-04-10')
        self.day_entry.bind("<FocusIn>", self.clear_day)
        self.day_entry.grid(column=5, row=0)

        start_label = tk.Label(self.add_frame, font=('Helvetica', 14), text='Start:', bg=self.background)
        start_label.grid(column=6, row=0, padx=(0,3))
        self.start_entry = tk.Entry(self.add_frame, font=('Helvetica', 12), width=8, bg='#d1d4d7')
        self.start_entry.insert(0, 'ex. 04:05')
        self.start_entry.bind("<FocusIn>", self.clear_start)
        self.start_entry.grid(column=7, row=0)

        end_label = tk.Label(self.add_frame, font=('Helvetica', 14), text='End:', bg=self.background)
        end_label.grid(column=8, row=0, padx=(0,3))
        self.end_entry = tk.Entry(self.add_frame, font=('Helvetica', 12), width=8, bg='#d1d4d7')
        self.end_entry.insert(0, 'ex. 06:05')
        self.end_entry.bind("<FocusIn>", self.clear_end)
        self.end_entry.grid(column=9, row=0)

        button_border = tk.Frame(self.add_frame, highlightbackground="Green",  highlightthickness=1, bd=0) 
        button_border.grid(column=10, row=0, padx=(15,0))
        add_button = tk.Button(button_border, text="A", font=('Helvetica', 12), border=0, bg='#37c876', cursor='hand2', command=self.add_trainer, anchor='center', activebackground='#27d881')
        add_button.pack(anchor='center')

        button_border = tk.Frame(self.add_frame, highlightbackground="Blue",  highlightthickness=1, bd=0) 
        button_border.grid(column=11, row=0, padx=(15,0))
        update_button = tk.Button(button_border, text="U", font=('Helvetica', 12), border=0, bg='#0ab6f5', cursor='hand2', command=self.update_session, anchor='center', activebackground='#66d1f9')
        update_button.pack(anchor='center')

        button_border = tk.Frame(self.add_frame, highlightbackground="Red",  highlightthickness=1, bd=0) 
        button_border.grid(column=12, row=0, padx=(15,0),)
        delete_button = tk.Button(button_border, text="C", font=('Helvetica', 12), border=0, bg='#e76e72', cursor='hand2', command=self.delete_trainer, anchor='center', activebackground='#ee9a9d')
        delete_button.pack(anchor='center')

        self.status = tk.StringVar()
        self.status.set('Status: ')
        self.status_label = tk.Label(self.trainer_frame, textvariable=self.status, font=('Helvetica', 14), anchor='w', bg=self.background)
        self.status_label.pack( fill='x', padx=(15,0), pady=(0,10))

    def clear_trainer(self, e):
        if 'ex.' in self.trainer_entry.get():
            self.trainer_entry.delete(0,"end")

    def clear_session(self, e):
        if 'ex.' in self.session_entry.get():
            self.session_entry.delete(0,"end")

    def clear_day(self, e):
        if 'ex.' in self.day_entry.get():
            self.day_entry.delete(0,"end")

    def clear_start(self, e):
        if 'ex.' in self.start_entry.get():
            self.start_entry.delete(0,"end")

    def clear_end(self, e):
        if 'ex.' in self.end_entry.get():
            self.end_entry.delete(0,"end")

    def add_trainer(self):
        trainer = self.trainer_entry.get()
        session = self.session_entry.get()
        day = self.day_entry.get()
        start = self.start_entry.get()
        end = self.end_entry.get()
        trainer_id = self.qapi.get_trainer_id_by_username(trainer)

        if 'ex.' in trainer or 'ex.' in day or 'ex.' in start or 'ex.' in end:
            self.status.set('Status: Add unsuccessful. Missing fields trainer/ day/ start time/ end time.')
        elif trainer == '' or day == '' or start == '' or end == '':
            self.status.set('Status: Add unsuccessful. Missing fields trainer/ day/ start time/ end time.')
        elif re.search(r"^\d{4}-(0[1-9]|1[0-2])-(0[1-9]|[1-2][0-9]|3[0-1])$", day) == None or re.search(r"^([0-1][0-9]|2[0-4]):[0-5][0-9]$", start) == None or re.search(r"^([0-1][0-9]|2[0-4]):[0-5][0-9]$", end) == None:
            self.status.set(f'Status: Add unsuccessful. Day/ start time/ end time has invalid format')
        elif self.qapi.get_member_schedule_by_time(self.member_id, day, start, end) != None:
            self.status.set(f'Status: Add Unsuccessful. Session already exists, try UPDATE instead.')
        elif trainer_id == None:
            self.status.set(f'Status: Add Unsuccessful. Trainer \'{trainer}\' not found')
        elif self.qapi.get_trainer_schedule_day_by_day(day, trainer_id) == None or self.qapi.get_trainer_schedule_start_by_start(start, trainer_id) == None or self.qapi.get_trainer_schedule_end_by_end(end, trainer_id) == None:
            self.status.set(f'Status: Add Unsuccessful. Trainer \'{trainer}\' is not availble in the chosen time.')
        else:
            self.qapi.add_member_schedule_by_time(self.member_id, trainer_id, day, start, end)
            self.qapi.delete_availability_by_availability(trainer_id, day, start, end)
            self.trainer_entry.delete(0, 'end')
            self.session_entry.delete(0, 'end')
            self.day_entry.delete(0, 'end')
            self.start_entry.delete(0, 'end')
            self.end_entry.delete(0, 'end')
            self.status.set(f'Status: Session successfully added.')
            self.hide_and_repopulate()

    def delete_trainer(self):
        session_id = self.session_entry.get().strip()

        if 'ex.' in session_id:
            self.status.set('Status: Delete unsuccessful. Missing field session id.')
        elif session_id == '':
            self.status.set('Status: Delete unsuccessful. Missing field session id.')
        elif re.search(r"^\d*$", session_id) == None:
            self.status.set(f'Status: Delete unsuccessful. Session id format is invalid.')
        elif self.qapi.get_member_schedule_by_id(self.member_id, session_id) == None:
            self.status.set(f'Status: Delete Unsuccessful. Session not found.')
        else:
            availability = self.qapi.get_trainer_schedule_from_member_by_time(self.member_id, session_id)
            self.qapi.add_availability_by_id(availability[0], availability[1], availability[2], availability[3])
            self.qapi.delete_session_by_time(self.member_id, session_id)
            self.trainer_entry.delete(0, 'end')
            self.session_entry.delete(0, 'end')
            self.day_entry.delete(0, 'end')
            self.start_entry.delete(0, 'end')
            self.end_entry.delete(0, 'end')
            self.status.set(f'Status: Session successfully deleted.')
            self.hide_and_repopulate()

    def update_session(self):
        trainer = self.trainer_entry.get()
        session = self.session_entry.get()
        day = self.day_entry.get()
        start = self.start_entry.get()
        end = self.end_entry.get()
        trainer_id = self.qapi.get_trainer_id_by_username(trainer)

        if 'ex.' in trainer or 'ex.' in session or 'ex.' in day or 'ex.' in start or 'ex.' in end:
            self.status.set('Status: Update unsuccessful. Missing fields session id/ trainer/ day/ start/ end')
        elif trainer == '' or session == '' or day == '' or start == '' or end == '':
            self.status.set('Status: Update unsuccessful. Missing fields session id/ trainer/ day/ start/ end')
        elif re.search(r"^\d*$", session) == None or re.search(r"^\d{4}-(0[1-9]|1[0-2])-(0[1-9]|[1-2][0-9]|3[0-1])$", day) == None or re.search(r"^([0-1][0-9]|2[0-4]):[0-5][0-9]$", start) == None or re.search(r"^([0-1][0-9]|2[0-4]):[0-5][0-9]$", end) == None:
            self.status.set(f'Status: Update unsuccessful. Session id/ day/ start/ end has invalid formatting')
        elif trainer_id == None:
            self.status.set(f'Status: Update Unsuccessful. Trainer \'{trainer}\' not found')
        elif self.qapi.get_trainer_schedule_day_by_day(day, trainer_id) == None or self.qapi.get_trainer_schedule_start_by_start(start, trainer_id) == None or self.qapi.get_trainer_schedule_end_by_end(end, trainer_id) == None:
            self.status.set(f'Status: Update Unsuccessful. Trainer \'{trainer}\' is not availble in the chosen time.')
        elif self.qapi.get_member_schedule_by_id(self.member_id, session) == None:
            self.status.set(f'Status: Update Unsuccessful. Session not found.')
        else:
            availability = self.qapi.get_trainer_schedule_from_member_by_id(self.member_id, session)
            self.qapi.add_availability_by_id(availability[0], availability[1], availability[2], availability[3])
            self.qapi.delete_availability_by_availability(trainer_id, day, start, end)            
            self.qapi.update_session_by_id(self.member_id, trainer_id, session, day, start, end)
            self.trainer_entry.delete(0, 'end')
            self.session_entry.delete(0, 'end')
            self.day_entry.delete(0, 'end')
            self.start_entry.delete(0, 'end')
            self.end_entry.delete(0, 'end')
            self.status.set(f'Status: Session successfully updated.')
            self.hide_and_repopulate()

    def hide_and_repopulate(self):
        self.trainer_schedule_frame.destroy()
        self.status_label.pack_forget()
        self.add_frame.pack_forget()
        self.seperator.pack_forget()
        self.edit_trainer_label.pack_forget()
        self.trainer_schedule_frame = tk.Frame(self.trainer_frame, bg=self.background)
        self.trainer_schedule_frame.pack(fill='x', padx=(15,0))

        self.create_trainer_titles()
        self.populate_trainer()

        self.seperator.pack(fill='x', pady=(10,0))
        self.edit_trainer_label.pack(fill='x', padx=(15,0), pady=10)
        self.add_frame.pack(fill='x', padx=(15,0), pady=(10,0))
        self.status_label.pack( fill='x', padx=(15,0), pady=(5,10))

    def create_trainer_titles(self):
        self.trainer_schedule_frame.columnconfigure(0, minsize=90) #trainer
        self.trainer_schedule_frame.columnconfigure(1, minsize=100) # day
        self.trainer_schedule_frame.columnconfigure(2, minsize=80) # start
        self.trainer_schedule_frame.columnconfigure(3, minsize=80) #end

        trainer_label = tk.Label(self.trainer_schedule_frame, text='Trainer', font=('Helvetica', 14), bg=self.background)
        trainer_label.grid(row=0, column=0, sticky='w')

        day_label = tk.Label(self.trainer_schedule_frame, text='Day', font=('Helvetica', 14), bg=self.background)
        day_label.grid(row=0, column=1, sticky='w')

        start_label = tk.Label(self.trainer_schedule_frame, text='Start', font=('Helvetica', 14), bg=self.background)
        start_label.grid(row=0, column=2, sticky='w')

        end_label = tk.Label(self.trainer_schedule_frame, text='End', font=('Helvetica', 14), bg=self.background)
        end_label.grid(row=0, column=3, sticky='w')

    def populate_trainer(self):
        schedules = self.qapi.get_all_availabilites()
        schedules.sort()
        cur_row = 0

        if len(schedules) != 0:
            for schedule in schedules:
                cur_row += 1
                for i in range(0, len(schedule)): 
                    if schedule[i] == None:
                        schedule_label = tk.Label(self.trainer_schedule_frame, text='No Use', font=('Helvetica', 12), bg=self.background)
                    elif i == 0:
                        schedule_label = tk.Label(self.trainer_schedule_frame, text=self.qapi.get_trainer_username_by_id(schedule[i]), font=('Helvetica', 12), bg=self.background)
                    else:
                        schedule_label = tk.Label(self.trainer_schedule_frame, text=schedule[i], font=('Helvetica', 12), bg=self.background)
                    if i == 0:
                        schedule_label.grid(row=cur_row, column=i, sticky='w', padx=(3,0))
                    else:
                        schedule_label.grid(row=cur_row, column=i, sticky='w')