import tkinter as tk 
from db_oper.db_api import *
from tkinter import ttk
import re

class ClassView:
    def __init__(self, classes_frame, admin_id):
        self.classes_frame = classes_frame
        self.qapi = QueryAPI()
        self.background = '#ebeceb'
        self.admin_id = admin_id

        self.classes_display_frame = tk.Frame(self.classes_frame, bg=self.background)
        self.classes_display_frame.pack(fill='both', expand=True)

        self.create_classes_titles(self.classes_display_frame)
        self.populate_classes(self.classes_display_frame)     

    def create_classes_titles(self, classes_display_frame):
        classes_display_frame.columnconfigure(0, minsize=100) #class
        classes_display_frame.columnconfigure(1, minsize=90) #trainer
        classes_display_frame.columnconfigure(2, minsize=80) #class name
        classes_display_frame.columnconfigure(3, minsize=100) # day
        classes_display_frame.columnconfigure(4, minsize=80) # start
        classes_display_frame.columnconfigure(5, minsize=80) #end

        class_num_label = tk.Label(classes_display_frame, text='ClassID', font=('Helvetica', 14), bg=self.background)
        class_num_label.grid(row=0, column=0, sticky='w', padx=(15,0), pady=(0,5))

        classes_label = tk.Label(classes_display_frame, text='Trainer', font=('Helvetica', 14), bg=self.background)
        classes_label.grid(row=0, column=1, sticky='w')

        trainer_label = tk.Label(classes_display_frame, text='Class', font=('Helvetica', 14), bg=self.background)
        trainer_label.grid(row=0, column=2, sticky='w')

        day_label = tk.Label(classes_display_frame, text='Day', font=('Helvetica', 14), bg=self.background)
        day_label.grid(row=0, column=3, sticky='w')

        start_label = tk.Label(classes_display_frame, text='Start', font=('Helvetica', 14), bg=self.background)
        start_label.grid(row=0, column=4, sticky='w')

        end_label = tk.Label(classes_display_frame, text='End', font=('Helvetica', 14), bg=self.background)
        end_label.grid(row=0, column=5, sticky='w')

    def populate_classes(self, classes_display_frame):
        classess = self.qapi.get_all_classess()
        classess.sort()
        cur_row = 0

        if len(classess) != 0:
            for classes in classess:
                cur_row += 1
                for i in range(0, len(classes)): 
                    if classes[i] == None:
                        classes_label = tk.Label(classes_display_frame, text='No Use', font=('Helvetica', 12), bg=self.background)
                    elif i == 1:
                        classes_label = tk.Label(classes_display_frame, text=self.qapi.get_trainer_username_by_id(classes[i]), font=('Helvetica', 12), bg=self.background)
                    else:
                        classes_label = tk.Label(classes_display_frame, text=classes[i], font=('Helvetica', 12), bg=self.background)
                    if i == 0:
                        classes_label.grid(row=cur_row, column=i, sticky='w', padx=(15,0))
                    else:
                        classes_label.grid(row=cur_row, column=i, sticky='w')
        
        self.button_border = tk.Frame(self.classes_frame, highlightbackground="Blue",  highlightthickness=1, bd=0) 
        self.button_border.pack(anchor='se', padx=(0,15))
        edit_button = tk.Button(self.button_border, text="Edit", font=('Helvetica', 12), border=0, bg='#0ab6f5', cursor='hand2', command=self.edit_class, anchor='center', activebackground='#66d1f9', width=6)
        edit_button.pack()

    def edit_class(self):
        color='#ebeceb'
        update_classes = tk.Toplevel()
        update_classes.geometry("%dx%d+%d+%d" % (1150, 400, (update_classes.winfo_screenwidth()/2 - 1150/2), (update_classes.winfo_screenheight()/2 - 400/2)))
        update_classes.resizable(width=False, height=False)
        update_classes.grab_set()
        update_classes.title("Update classes")

        self.class_frame = tk.Frame(update_classes, bg=color,  highlightbackground='#7db6b5', highlightthickness=1)
        self.class_frame.pack(fill='both', expand=True, padx=15, pady=15)

        self.trainer_schedule_label = tk.Label(self.class_frame, text="Trainer's Availability", font=('Helvetica', 20), anchor='w', bg=self.background)
        self.trainer_schedule_label.pack(fill='x', padx=(15,0), pady=10)

        self.trainer_schedule_frame = tk.Frame(self.class_frame, bg=color)
        self.trainer_schedule_frame.pack(fill='x', padx=(15,0))

        self.create_trainer_titles()
        self.populate_trainers()

        self.seperator = ttk.Separator(self.class_frame, orient='horizontal')
        self.seperator.pack(fill='x', pady=(10,0))

        self.edit_classes_label = tk.Label(self.class_frame, text="Edit Classes", font=('Helvetica', 20), anchor='w', bg=self.background)
        self.edit_classes_label.pack(fill='x', padx=(15,0), pady=10)

        self.add_frame = tk.Frame(self.class_frame, bg=color)
        self.add_frame.pack(fill='x', padx=(15,0))

        classes_label = tk.Label(self.add_frame, font=('Helvetica', 14), text='ClassID:', bg=color)
        classes_label.grid(column=0, row=0, padx=(0,3))
        self.classes_entry = tk.Entry(self.add_frame, font=('Helvetica', 12), width=8, bg='#d1d4d7')
        self.classes_entry.insert(0, 'ex. 1')
        self.classes_entry.bind("<FocusIn>", self.clear_classes)
        self.classes_entry.grid(column=1, row=0)

        trainer_label = tk.Label(self.add_frame, font=('Helvetica', 14), text='Trainer:', bg=color)
        trainer_label.grid(column=2, row=0, padx=(0,3))
        self.trainer_entry = tk.Entry(self.add_frame, font=('Helvetica', 12), width=10, bg='#d1d4d7')
        self.trainer_entry.insert(0, 'ex. yasir')
        self.trainer_entry.bind("<FocusIn>", self.clear_trainer)
        self.trainer_entry.grid(column=3, row=0)
                            
        name_label = tk.Label(self.add_frame, font=('Helvetica', 14), text='Class Name:', bg=color)
        name_label.grid(column=4, row=0, padx=(0,3))
        self.name_entry = tk.Entry(self.add_frame, font=('Helvetica', 12), width=8, bg='#d1d4d7')
        self.name_entry.insert(0, 'ex. Zumba')
        self.name_entry.bind("<FocusIn>", self.clear_name)
        self.name_entry.grid(column=5, row=0)

        day_label = tk.Label(self.add_frame, font=('Helvetica', 14), text='Day:', bg=color)
        day_label.grid(column=6, row=0, padx=(0,3))
        self.day_entry = tk.Entry(self.add_frame, font=('Helvetica', 12), width=12, bg='#d1d4d7')
        self.day_entry.insert(0, 'ex. 2024-04-10')
        self.day_entry.bind("<FocusIn>", self.clear_day)
        self.day_entry.grid(column=7, row=0)

        start_label = tk.Label(self.add_frame, font=('Helvetica', 14), text='Start:', bg=color)
        start_label.grid(column=8, row=0, padx=(0,3))
        self.start_entry = tk.Entry(self.add_frame, font=('Helvetica', 12), width=8, bg='#d1d4d7')
        self.start_entry.insert(0, 'ex. 04:05')
        self.start_entry.bind("<FocusIn>", self.clear_start)
        self.start_entry.grid(column=9, row=0)

        end_label = tk.Label(self.add_frame, font=('Helvetica', 14), text='End:', bg=color)
        end_label.grid(column=10, row=0, padx=(0,3))
        self.end_entry = tk.Entry(self.add_frame, font=('Helvetica', 12), width=8, bg='#d1d4d7')
        self.end_entry.insert(0, 'ex. 06:05')
        self.end_entry.bind("<FocusIn>", self.clear_end)
        self.end_entry.grid(column=11, row=0)

        button_border = tk.Frame(self.add_frame, highlightbackground="Green",  highlightthickness=1, bd=0) 
        button_border.grid(column=13, row=0, padx=(15,0))
        add_button = tk.Button(button_border, text="A", font=('Helvetica', 12), border=0, bg='#37c876', cursor='hand2', command=self.add_classes, anchor='center', activebackground='#27d881')
        add_button.pack(anchor='center')

        button_border = tk.Frame(self.add_frame, highlightbackground="Blue",  highlightthickness=1, bd=0) 
        button_border.grid(column=14, row=0, padx=(15,0))
        update_button = tk.Button(button_border, text="U", font=('Helvetica', 12), border=0, bg='#0ab6f5', cursor='hand2', command=self.update_classes, anchor='center', activebackground='#66d1f9')
        update_button.pack(anchor='center')

        button_border = tk.Frame(self.add_frame, highlightbackground="Red",  highlightthickness=1, bd=0) 
        button_border.grid(column=15, row=0, padx=(15,0),)
        delete_button = tk.Button(button_border, text="D", font=('Helvetica', 12), border=0, bg='#e76e72', cursor='hand2', command=self.delete_classes, anchor='center', activebackground='#ee9a9d')
        delete_button.pack(anchor='center')

        self.status = tk.StringVar()
        self.status.set('Status: ')
        self.status_label = tk.Label(self.class_frame, textvariable=self.status, font=('Helvetica', 14), anchor='w', bg=color)
        self.status_label.pack( fill='x', padx=(15,0), pady=10)

        update_classes.protocol('WM_DELETE_WINDOW', lambda: self.destroy_and_repopulate(update_classes))

    def clear_classes(self, e):
        if 'ex.' in self.classes_entry.get():
            self.classes_entry.delete(0,"end")

    def clear_trainer(self, e):
        if 'ex.' in self.trainer_entry.get():
            self.trainer_entry.delete(0,"end")

    def clear_name(self, e):
        if 'ex.' in self.name_entry.get():
            self.name_entry.delete(0,"end")

    def clear_day(self, e):
        if 'ex.' in self.day_entry.get():
            self.day_entry.delete(0,"end")

    def clear_start(self, e):
        if 'ex.' in self.start_entry.get():
            self.start_entry.delete(0,"end")

    def clear_end(self, e):
        if 'ex.' in self.end_entry.get():
            self.end_entry.delete(0,"end")

    def add_classes(self):
        class_id = self.classes_entry.get()
        trainer = self.trainer_entry.get()
        name = self.name_entry.get()
        day = self.day_entry.get()
        start = self.start_entry.get()
        end = self.end_entry.get()
        trainer_id = self.qapi.get_trainer_id_by_username(trainer)

        if 'ex.' in class_id or 'ex.' in name or 'ex.' in trainer or 'ex.' in day or 'ex.' in start or 'ex.' in end:
            self.status.set('Status: Add unsuccessful. Missing fields class id/ class name/ trainer name/ day/ start time/ end time.')
        elif class_id == '' or name == '' or trainer == '' or day == '' or start == '' or end == '':
            self.status.set('Status: Add unsuccessful. Missing fields class id/ class name/ trainer name/ day/ start time/ end time.')
        elif re.search(r"^\d*$", class_id) == None or re.search(r"^\d{4}-(0[1-9]|1[0-2])-(0[1-9]|[1-2][0-9]|3[0-1])$", day) == None or re.search(r"^([0-1][0-9]|2[0-4]):[0-5][0-9]$", start) == None or re.search(r"^([0-1][0-9]|2[0-4]):[0-5][0-9]$", end) == None:
            self.status.set(f'Status: Add unsuccessful. Class Id/ day/ start time/ end time has invalid format')
        elif self.qapi.get_class_by_id(class_id) != None:
            self.status.set(f'Status: Add Unsuccessful. Class \'{class_id}\' already exists, try UPDATE instead.')
        elif trainer_id == None:
            self.status.set(f'Status: Add Unsuccessful. Trainer \'{trainer}\' not found') 
        elif self.qapi.get_trainer_schedule_day_by_day(day, trainer_id) == None or self.qapi.get_trainer_schedule_start_by_start(start, trainer_id) == None or self.qapi.get_trainer_schedule_end_by_end(end, trainer_id) == None:
            self.status.set(f'Status: Add Unsuccessful. Trainer \'{trainer}\' is not availble in the chosen time.')
        else:
            self.qapi.add_class_by_id(class_id, trainer_id, name, day, start, end)
            self.qapi.delete_availability_by_availability(trainer_id, day, start, end)
            self.classes_entry.delete(0, 'end')
            self.trainer_entry.delete(0, 'end')
            self.name_entry.delete(0, 'end')
            self.day_entry.delete(0, 'end')
            self.start_entry.delete(0, 'end')
            self.end_entry.delete(0, 'end')
            self.status.set(f'Status: Class \'{name}\' successfully added.')
            self.hide_and_repopulate()

    def delete_classes(self):
        class_id = self.classes_entry.get()

        if 'ex.' in class_id:
            self.status.set('Status: Delete unsuccessful. Missing field class id.')
        elif class_id == '':
            self.status.set('Status: Delete unsuccessful. Missing field class id.')
        elif re.search(r"^\d*$", class_id) == None:
            self.status.set(f'Status: Delete unsuccessful. Class id \'{class_id}\' is invalid')
        elif self.qapi.get_class_by_id(class_id) == None:
            self.status.set(f'Status: Delete Unsuccessful. Class id \'{class_id}\' not found.')
        else:
            availability = self.qapi.get_trainer_schedule_from_class_by_id(class_id)
            self.qapi.add_availability_by_id(availability[0], availability[1], availability[2], availability[3])
            self.qapi.delete_class_by_id(class_id)
            self.classes_entry.delete(0, 'end')
            self.trainer_entry.delete(0, 'end')
            self.name_entry.delete(0, 'end')
            self.day_entry.delete(0, 'end')
            self.start_entry.delete(0, 'end')
            self.end_entry.delete(0, 'end')
            self.status.set(f'Status: Class id \'{class_id}\' successfully deleted.')
            self.hide_and_repopulate()

    def update_classes(self):
        class_id = self.classes_entry.get()
        trainer = self.trainer_entry.get()
        name = self.name_entry.get()
        day = self.day_entry.get()
        start = self.start_entry.get()
        end = self.end_entry.get()
        trainer_id = self.qapi.get_trainer_id_by_username(trainer)

        if 'ex.' in class_id or ('ex.' in name and ('ex.' in trainer or 'ex.' in day or 'ex.' in start or 'ex.' in end)):
            self.status.set('Status: Update unsuccessful. Missing fields class id/ class name/ trainer/ day/ start/ end')
        elif class_id == '' or (name == '' and (trainer == '' or day == '' or start == '' or end == '')):
            self.status.set('Status: Update unsuccessful. Missing fields class id/ class name/ trainer/ day/ start/ end')
        elif re.search(r"^\d*$", class_id) == None or re.search(r"^\d{4}-(0[1-9]|1[0-2])-(0[1-9]|[1-2][0-9]|3[0-1])$", day) == None or re.search(r"^([0-1][0-9]|2[0-4]):[0-5][0-9]$", start) == None or re.search(r"^([0-1][0-9]|2[0-4]):[0-5][0-9]$", end) == None:
            self.status.set(f'Status: Update unsuccessful. Class id/ day/ start/ end has invalid formatting')
        elif trainer_id == None:
            self.status.set(f'Status: Update Unsuccessful. Trainer \'{trainer}\' not found')
        elif self.qapi.get_trainer_schedule_day_by_day(day, trainer_id) == None or self.qapi.get_trainer_schedule_start_by_start(start, trainer_id) == None or self.qapi.get_trainer_schedule_end_by_end(end, trainer_id) == None:
            self.status.set(f'Status: Update Unsuccessful. Trainer \'{trainer}\' is not availble in the chosen time.')
        elif self.qapi.get_class_by_id(class_id) == None:
            self.status.set(f'Status: Update Unsuccessful. Class id \'{class_id}\' not found.')
        else:
            if name == '' or 'ex.' in name or ((name != '' or 'ex.' not in name) and (day != '' or 'ex.' not in day) and (start != '' or 'ex.' not in start) and (end != '' or 'ex.' not in end)):
                old_availability = self.qapi.get_trainer_schedule_from_class_by_id(class_id)
                self.qapi.delete_availability_by_availability(trainer_id, day, start, end)
                self.qapi.add_availability_by_id(old_availability[0], old_availability[1], old_availability[2], old_availability[3])
            
            self.qapi.update_class_by_id(class_id, trainer_id, name, day, start, end)
            self.classes_entry.delete(0, 'end')
            self.trainer_entry.delete(0, 'end')
            self.name_entry.delete(0, 'end')
            self.day_entry.delete(0, 'end')
            self.start_entry.delete(0, 'end')
            self.end_entry.delete(0, 'end')
            self.status.set(f'Status: classes \'{class_id}\' successfully updated.')
            self.hide_and_repopulate()

    def destroy_and_repopulate(self, update_classes):
        update_classes.destroy()
        self.classes_display_frame.destroy()
        self.button_border.destroy()
        self.classes_display_frame = tk.Frame(self.classes_frame, bg=self.background)
        self.classes_display_frame.pack(fill='x')

        self.create_classes_titles(self.classes_display_frame)
        self.populate_classes(self.classes_display_frame)

    def hide_and_repopulate(self):
        self.trainer_schedule_frame.destroy()
        self.status_label.pack_forget()
        self.add_frame.pack_forget()
        self.seperator.pack_forget()
        self.edit_classes_label.pack_forget()
        self.trainer_schedule_frame = tk.Frame(self.class_frame, bg=self.background)
        self.trainer_schedule_frame.pack(fill='x', padx=(15,0))

        self.create_trainer_titles()
        self.populate_trainers()

        self.seperator.pack(fill='x', pady=(10,0))
        self.edit_classes_label.pack(fill='x', padx=(15,0), pady=10)
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

    def populate_trainers(self):
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