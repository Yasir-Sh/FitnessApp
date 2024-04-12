import tkinter as tk
from src.db_oper.db_api import *
import re

class AvailabilityView:
    def __init__(self, availability_frame, trainer_id):
        self.availability_frame = availability_frame
        self.qapi = QueryAPI()
        self.background = '#ebeceb'
        self.trainer_id = trainer_id

        self.availability_display_frame = tk.Frame(self.availability_frame, bg=self.background)
        self.availability_display_frame.pack(fill='x')

        self.create_availability_titles(self.availability_display_frame)
        self.populate_availability(self.availability_display_frame)     

    def create_availability_titles(self, availability_display_frame):
        availability_display_frame.columnconfigure(0, minsize=70)
        availability_display_frame.columnconfigure(1, minsize=113)
        availability_display_frame.columnconfigure(2, minsize=112)

        date_label = tk.Label(availability_display_frame, text='Date', font=('Helvetica', 14), bg=self.background)
        date_label.grid(row=0, column=0, sticky='w', padx=(15,0), pady=(0,5))

        start_label = tk.Label(availability_display_frame, text='Start Time', font=('Helvetica', 14), bg=self.background)
        start_label.grid(row=0, column=1, sticky='w')

        end_label = tk.Label(availability_display_frame, text='End Time', font=('Helvetica', 14), bg=self.background)
        end_label.grid(row=0, column=2, sticky='w')

    def populate_availability(self, availability_display_frame):
        availabilities = self.qapi.get_availability_by_id(self.trainer_id)
        availabilities.sort()
        cur_row = 0

        if len(availabilities) != 0:
            for availability in availabilities:
                cur_row += 1
                for i in range(1, len(availability)): 
                    if availability[i] == None:
                        availability_label = tk.Label(availability_display_frame, text='N/A', font=('Helvetica', 12), bg=self.background)
                    else:
                        availability_label = tk.Label(availability_display_frame, text=availability[i], font=('Helvetica', 12), bg=self.background)
                    availability_label.grid(row=cur_row, column=i-1, sticky='w', padx=(15,0))
        
        self.button_border = tk.Frame(self.availability_frame, highlightbackground="Blue",  highlightthickness=1, bd=0) 
        self.button_border.pack(anchor='se', padx=(0,15))
        add_button = tk.Button(self.button_border, text="Edit", font=('Helvetica', 12), border=0, bg='#0ab6f5', cursor='hand2', command=self.add_availability, anchor='center', activebackground='#66d1f9', width=6)
        add_button.pack()
    
    def add_availability(self):
        color='#ebeceb'
        add_available = tk.Toplevel()
        add_available.geometry("%dx%d+%d+%d" % (700, 150, (add_available.winfo_screenwidth()/2 - 700/2), (add_available.winfo_screenheight()/2 - 70/2)))
        add_available.resizable(width=False, height=False)
        add_available.grab_set()
        add_available.title("Add Availability")

        self.available_frame = tk.Frame(add_available, bg=color,  highlightbackground='#7db6b5', highlightthickness=1)
        self.available_frame.pack(fill='both', expand=True, padx=5, pady=10)

        available_label = tk.Label(self.available_frame, text=f"Add Availability", font=('Helvetica', 20), anchor='w', bg=color)
        available_label.pack(fill='x', padx=(15,0), pady=(0, 5))

        add_frame = tk.Frame(self.available_frame, bg=color)
        add_frame.pack(fill='x', padx=(15,0))

        date_label = tk.Label(add_frame, font=('Helvetica', 14), text='Date:', bg=color)
        date_label.grid(column=0, row=0, padx=(0,3))
        self.date_entry = tk.Entry(add_frame, font=('Helvetica', 12), width=10, bg='#d1d4d7')
        self.date_entry.insert(0, 'yyyy-mm-dd')
        self.date_entry.bind("<FocusIn>", self.clear_date)
        self.date_entry.grid(column=1, row=0)

        start_label = tk.Label(add_frame, font=('Helvetica', 14), text='Start Time:', bg=color)
        start_label.grid(column=2, row=0, padx=(0,3))
        self.start_entry = tk.Entry(add_frame, font=('Helvetica', 12), width=10, bg='#d1d4d7')
        self.start_entry.insert(0, 'hh:mm')
        self.start_entry.bind("<FocusIn>", self.clear_start)
        self.start_entry.grid(column=3, row=0)
                            
        end_label = tk.Label(add_frame, font=('Helvetica', 14), text='End Time:', bg=color)
        end_label.grid(column=4, row=0, padx=(0,3))
        self.end_entry = tk.Entry(add_frame, font=('Helvetica', 12), width=10, bg='#d1d4d7')
        self.end_entry.insert(0, 'hh:mm')
        self.end_entry.bind("<FocusIn>", self.clear_end)
        self.end_entry.grid(column=5, row=0)

        button_border = tk.Frame(add_frame, highlightbackground="Green",  highlightthickness=1, bd=0) 
        button_border.grid(column=8, row=0, padx=(15,0))
        add_button = tk.Button(button_border, text="A", font=('Helvetica', 12), border=0, bg='#37c876', cursor='hand2', command=self.add_interval, anchor='center', activebackground='#27d881')
        add_button.pack(anchor='center')

        button_border = tk.Frame(add_frame, highlightbackground="Red",  highlightthickness=1, bd=0) 
        button_border.grid(column=10, row=0, padx=(15,0),)
        delete_button = tk.Button(button_border, text="D", font=('Helvetica', 12), border=0, bg='#e76e72', cursor='hand2', command=self.delete_interval, anchor='center', activebackground='#ee9a9d')
        delete_button.pack(anchor='center')

        self.status = tk.StringVar()
        self.status.set('Status: ')
        status_label = tk.Label(self.available_frame, textvariable=self.status, font=('Helvetica', 14), anchor='w', bg=color)
        status_label.pack( fill='x', padx=(15,0), pady=10)

        add_available.protocol('WM_DELETE_WINDOW', lambda: self.destroy_and_repopulate(add_available))

    def clear_date(self, e):
        if self.date_entry.get() == 'yyyy-mm-dd':
            self.date_entry.delete(0,"end")

    def clear_start(self, e):
        if self.start_entry.get() == 'hh:mm':
            self.start_entry.delete(0,"end")

    def clear_end(self, e):
        if self.end_entry.get() == 'hh:mm':
            self.end_entry.delete(0,"end")

    def add_interval(self):
        date = self.date_entry.get()
        start_time = self.start_entry.get()
        end_time = self.end_entry.get()

        if date == 'yyyy-mm-dd' or start_time == 'hh:mm' or end_time == 'hh:mm':
            self.status.set('Status: Add unsuccessful. Missing fields date/ start time/ end time.')
        elif date == '' or start_time == '' or end_time == '':
            self.status.set('Status: Add unsuccessful. Missing fields date/ start time/ end time.')
        elif re.search(r"^\d{4}-(0[1-9]|1[0-2])-(0[1-9]|[1-2][0-9]|3[0-1])$", date) == None or re.search(r"^([0-1][0-9]|2[0-4]):[0-5][0-9]$", start_time) == None or re.search(r"^([0-1][0-9]|2[0-4]):[0-5][0-9]$", end_time) == None:
            self.status.set('Status: Add unsuccessful. Incorrect date/ time format.')
        elif self.qapi.get_availability_by_interval(self.trainer_id, date, start_time, end_time) != None:   
            self.status.set(f'Status: Add unsuccessful. Interval already exists.')
        elif self.qapi.get_trainer_schedule_from_member_by_time_and_id(self.trainer_id, date, start_time, end_time) != None:
            self.status.set(f'Status: Add unsuccessful. Interval already assigned')
        else:
            self.qapi.add_availability_by_id(self.trainer_id, date, start_time, end_time)
            self.date_entry.delete(0, 'end')
            self.start_entry.delete(0, 'end')
            self.end_entry.delete(0, 'end')
            self.status.set(f'Status: Interval successfullly added.')

    def delete_interval(self):
        date = self.date_entry.get()
        start_time = self.start_entry.get()
        end_time = self.end_entry.get()

        if date == 'yyyy-mm-dd' or start_time == 'hh:mm' or end_time == 'hh:mm':
            self.status.set('Status: Delete unsuccessful. Missing fields date/ start time/ end time.')
        elif date == '' or start_time == '' or end_time == '':
            self.status.set('Status: Delete unsuccessful. Missing fields date/ start time/ end time.')
        elif re.search(r"^\d{4}-(0[1-9]|1[0-2])-(0[1-9]|[1-2][0-9]|3[0-1])$", date) == None or re.search(r"^([0-1][0-9]|2[0-4]):[0-5][0-9]$", start_time) == None or re.search(r"^([0-1][0-9]|2[0-4]):[0-5][0-9]$", end_time) == None:
            self.status.set('Status: Delete unsuccessful. Invalid date/ time formart.')
        elif self.qapi.get_availability_by_interval(self.trainer_id, date, start_time, end_time) == None:   
            self.status.set(f'Status: Delete unsuccessful. Interval not found.')
        else:
            self.qapi.delete_availability_by_availability(self.trainer_id, date, start_time, end_time)
            self.date_entry.delete(0, 'end')
            self.start_entry.delete(0, 'end')
            self.end_entry.delete(0, 'end')
            self.status.set(f'Status: Interval successfully deleted.')

    def destroy_and_repopulate(self, add_available):
        add_available.destroy()
        self.availability_display_frame.destroy()
        self.button_border.destroy()
        self.availability_display_frame = tk.Frame(self.availability_frame, bg=self.background)
        self.availability_display_frame.pack(fill='x')

        self.create_availability_titles(self.availability_display_frame)
        self.populate_availability(self.availability_display_frame)

    