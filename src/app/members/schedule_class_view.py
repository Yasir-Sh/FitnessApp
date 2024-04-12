import tkinter as tk
from tkinter import ttk
from src.db_oper.db_api import *
import re

class ScheduleClass:
    def __init__(self, update_class, member_id):
        self.update_class = update_class
        self.background = '#ebeceb'
        self.qapi = QueryAPI()
        self.member_id = member_id

        self.class_frame = tk.Frame(self.update_class, bg=self.background,  highlightbackground='#7db6b5', highlightthickness=1)
        self.class_frame.pack(fill='both', expand=True, padx=15, pady=15)

        self.class_schedule_label = tk.Label(self.class_frame, text="Classes", font=('Helvetica', 20), anchor='w', bg=self.background)
        self.class_schedule_label.pack(fill='x', padx=(15,0), pady=10)

        self.class_schedule_frame = tk.Frame(self.class_frame, bg=self.background)
        self.class_schedule_frame.pack(fill='x', padx=(15,0))

        self.create_class_titles()
        self.populate_class()

        self.seperator = ttk.Separator(self.class_frame, orient='horizontal')
        self.seperator.pack(fill='x', pady=(10,0))

        self.edit_class_label = tk.Label(self.class_frame, text="Select class", font=('Helvetica', 20), anchor='w', bg=self.background)
        self.edit_class_label.pack(fill='x', padx=(15,0), pady=10)

        self.add_frame = tk.Frame(self.class_frame, bg=self.background)
        self.add_frame.pack(fill='x', padx=(15,0))

        class_label = tk.Label(self.add_frame, font=('Helvetica', 14), text='ClassId:', bg=self.background)
        class_label.grid(column=0, row=0, padx=(0,3))
        self.class_entry = tk.Entry(self.add_frame, font=('Helvetica', 12), width=10, bg='#d1d4d7')
        self.class_entry.insert(0, 'ex. 1')
        self.class_entry.bind("<FocusIn>", self.clear_class)
        self.class_entry.grid(column=1, row=0)     

        button_border = tk.Frame(self.add_frame, highlightbackground="Green",  highlightthickness=1, bd=0) 
        button_border.grid(column=12, row=0, padx=(15,0))
        add_button = tk.Button(button_border, text="A", font=('Helvetica', 12), border=0, bg='#37c876', cursor='hand2', command=self.add_class, anchor='center', activebackground='#27d881')
        add_button.pack(anchor='center')

        button_border = tk.Frame(self.add_frame, highlightbackground="Red",  highlightthickness=1, bd=0) 
        button_border.grid(column=13, row=0, padx=(15,0),)
        delete_button = tk.Button(button_border, text="D", font=('Helvetica', 12), border=0, bg='#e76e72', cursor='hand2', command=self.delete_class, anchor='center', activebackground='#ee9a9d')
        delete_button.pack(anchor='center')

        self.status = tk.StringVar()
        self.status.set('Status: ')
        self.status_label = tk.Label(self.class_frame, textvariable=self.status, font=('Helvetica', 14), anchor='w', bg=self.background)
        self.status_label.pack( fill='x', padx=(15,0), pady=(0,10))

    def clear_class(self, e):
        if 'ex.' in self.class_entry.get():
            self.class_entry.delete(0,"end")

    def add_class(self):
        class_id = self.class_entry.get()

        if 'ex.' in class_id:
            self.status.set('Status: Add unsuccessful. Missing fields class id/ trainer/ class name/ day/ start time/ end time.')
        elif class_id == '':
            self.status.set('Status: Add unsuccessful. Missing fields class id/ trainer/ class name/ day/ start time/ end time.')
        elif re.search(r"^\d*$", class_id) == None:
            self.status.set(f'Status: Add unsuccessful. Class id/ day/ start time/ end time has invalid format')
        elif self.qapi.get_member_class_by_id(self.member_id, class_id) != None:
            self.status.set(f'Status: Add Unsuccessful. Already regiestred to \'{self.qapi.get_class_by_id(class_id)[2]}\' class')
        elif self.qapi.get_class_by_id(class_id) == None:
            self.status.set(f'Status: Add Unsuccessful. Class \'{class_id}\' not found')
        else:
            self.qapi.add_member_to_class_by_id(self.member_id, class_id)
            self.class_entry.delete(0, 'end')
            self.status.set(f'Status: Registered to \'{self.qapi.get_class_by_id(class_id)[2]}\' Class Successfully.')
            self.hide_and_repopulate()

    def delete_class(self):
        class_id = self.class_entry.get()

        if 'ex.' in class_id:
            self.status.set('Status: Delete unsuccessful. Missing field class id.')
        elif class_id == '':
            self.status.set('Status: Delete unsuccessful. Missing field class id.')
        elif re.search(r"^\d*$", class_id) == None:
            self.status.set(f'Status: Delete unsuccessful. Class id \'{class_id}\' is invalid')
        elif self.qapi.get_class_regestry_by_id(class_id, self.member_id) == None:
            self.status.set(f'Status: Delete Unsuccessful. Class regestration not found.')
        else:
            self.qapi.delete_class_regestry_by_id(class_id, self.member_id)
            self.class_entry.delete(0, 'end')
            self.status.set(f'Status: Class \'{self.qapi.get_class_by_id(class_id)[2]}\' regestration deleted.')
            self.hide_and_repopulate()

    def hide_and_repopulate(self):
        self.class_schedule_frame.destroy()
        self.status_label.pack_forget()
        self.add_frame.pack_forget()
        self.seperator.pack_forget()
        self.edit_class_label.pack_forget()
        self.class_schedule_frame = tk.Frame(self.class_frame, bg=self.background)
        self.class_schedule_frame.pack(fill='x', padx=(15,0))

        self.create_class_titles()
        self.populate_class()

        self.seperator.pack(fill='x', pady=(10,0))
        self.edit_class_label.pack(fill='x', padx=(15,0), pady=10)
        self.add_frame.pack(fill='x', padx=(15,0))
        self.status_label.pack( fill='x', padx=(15,0), pady=(5,10))

    def create_class_titles(self):
        self.class_schedule_frame.columnconfigure(0, minsize=80) #class id
        self.class_schedule_frame.columnconfigure(1, minsize=80) # trainer
        self.class_schedule_frame.columnconfigure(2, minsize=80) # name
        self.class_schedule_frame.columnconfigure(3, minsize=100) # day
        self.class_schedule_frame.columnconfigure(4, minsize=80) #start
        self.class_schedule_frame.columnconfigure(5, minsize=80) #end

        class_label = tk.Label(self.class_schedule_frame, text='ClassId', font=('Helvetica', 14), bg=self.background)
        class_label.grid(row=0, column=0, sticky='w')

        trainer_label = tk.Label(self.class_schedule_frame, text='Trainer', font=('Helvetica', 14), bg=self.background)
        trainer_label.grid(row=0, column=1, sticky='w')

        trainer_label = tk.Label(self.class_schedule_frame, text='Class', font=('Helvetica', 14), bg=self.background)
        trainer_label.grid(row=0, column=2, sticky='w')

        day_label = tk.Label(self.class_schedule_frame, text='Day', font=('Helvetica', 14), bg=self.background)
        day_label.grid(row=0, column=3, sticky='w')

        start_label = tk.Label(self.class_schedule_frame, text='Start', font=('Helvetica', 14), bg=self.background)
        start_label.grid(row=0, column=4, sticky='w')

        end_label = tk.Label(self.class_schedule_frame, text='End', font=('Helvetica', 14), bg=self.background)
        end_label.grid(row=0, column=5, sticky='w')

    def populate_class(self):
        schedules = self.qapi.get_all_classess()
        schedules.sort()
        cur_row = 0

        if len(schedules) != 0:
            for schedule in schedules:
                cur_row += 1
                for i in range(0, len(schedule)): 
                    if schedule[i] == None:
                        schedule_label = tk.Label(self.class_schedule_frame, text='No Use', font=('Helvetica', 12), bg=self.background)
                    elif i == 1:
                        schedule_label = tk.Label(self.class_schedule_frame, text=self.qapi.get_trainer_username_by_id(schedule[i]), font=('Helvetica', 12), bg=self.background)
                    else:
                        schedule_label = tk.Label(self.class_schedule_frame, text=schedule[i], font=('Helvetica', 12), bg=self.background)
                    if i == 0:
                        schedule_label.grid(row=cur_row, column=i, sticky='w', padx=(3,0))
                    else:
                        schedule_label.grid(row=cur_row, column=i, sticky='w')