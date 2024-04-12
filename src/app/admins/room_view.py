import tkinter as tk
import re
from src.db_oper.db_api import *

class RoomView:
    def __init__(self, room_frame, admin_id):
        self.room_frame = room_frame
        self.qapi = QueryAPI()
        self.background = '#ebeceb'
        self.admin_id = admin_id

        self.room_display_frame = tk.Frame(self.room_frame, bg=self.background)
        self.room_display_frame.pack(fill='x')

        self.create_room_titles(self.room_display_frame)
        self.populate_room(self.room_display_frame)     

    def create_room_titles(self, room_display_frame):
        room_display_frame.columnconfigure(0, minsize=110)
        room_display_frame.columnconfigure(1, minsize=143)
        room_display_frame.columnconfigure(2, minsize=112)

        room_label = tk.Label(room_display_frame, text='Room', font=('Helvetica', 14), bg=self.background)
        room_label.grid(row=0, column=0, sticky='w', padx=(15,0), pady=(0,5))

        availability_label = tk.Label(room_display_frame, text='Availability', font=('Helvetica', 14), bg=self.background)
        availability_label.grid(row=0, column=1, sticky='w')

        usage_label = tk.Label(room_display_frame, text='Usage', font=('Helvetica', 14), bg=self.background)
        usage_label.grid(row=0, column=2, sticky='w')

    def populate_room(self, room_display_frame):
        rooms = self.qapi.get_all_rooms()
        rooms.sort()
        cur_row = 0

        if len(rooms) != 0:
            for room in rooms:
                cur_row += 1
                for i in range(0, len(room)): 
                    if room[i] == None:
                        room_label = tk.Label(room_display_frame, text='No Use', font=('Helvetica', 12), bg=self.background)
                    else:
                        room_label = tk.Label(room_display_frame, text=room[i], font=('Helvetica', 12), bg=self.background)
                    if i == 0:
                        room_label.grid(row=cur_row, column=i, sticky='w', padx=(15,0))
                    else:
                        room_label.grid(row=cur_row, column=i, sticky='w')
        
        self.button_border = tk.Frame(self.room_frame, highlightbackground="Blue",  highlightthickness=1, bd=0) 
        self.button_border.pack(anchor='se', padx=(0,15))
        edit_button = tk.Button(self.button_border, text="Edit", font=('Helvetica', 12), border=0, bg='#0ab6f5', cursor='hand2', command=self.edit_room, anchor='center', activebackground='#66d1f9', width=6)
        edit_button.pack()

    def edit_room(self):
        color='#ebeceb'
        update_room = tk.Toplevel()
        update_room.geometry("%dx%d+%d+%d" % (700, 150, (update_room.winfo_screenwidth()/2 - 700/2), (update_room.winfo_screenheight()/2 - 70/2)))
        update_room.resizable(width=False, height=False)
        update_room.grab_set()
        update_room.title("Update Room")

        self.room_edit_frame = tk.Frame(update_room, bg=color,  highlightbackground='#7db6b5', highlightthickness=1)
        self.room_edit_frame.pack(fill='both', expand=True, padx=5, pady=10)

        room_edit_label = tk.Label(self.room_edit_frame, text=f"Edit Rooms", font=('Helvetica', 20), anchor='w', bg=color)
        room_edit_label.pack(fill='x', padx=(15,0), pady=(0, 5))

        add_frame = tk.Frame(self.room_edit_frame, bg=color)
        add_frame.pack(fill='x', padx=(15,0))

        room_label = tk.Label(add_frame, font=('Helvetica', 14), text='Room:', bg=color)
        room_label.grid(column=0, row=0, padx=(0,3))
        self.room_entry = tk.Entry(add_frame, font=('Helvetica', 12), width=12, bg='#d1d4d7')
        self.room_entry.insert(0, 'ex. 1')
        self.room_entry.bind("<FocusIn>", self.clear_room)
        self.room_entry.grid(column=1, row=0)

        availability_label = tk.Label(add_frame, font=('Helvetica', 14), text='Availability:', bg=color)
        availability_label.grid(column=2, row=0, padx=(0,3))
        self.availability_entry = tk.Entry(add_frame, font=('Helvetica', 12), width=12, bg='#d1d4d7')
        self.availability_entry.insert(0, 'ex. Occupied')
        self.availability_entry.bind("<FocusIn>", self.clear_availability)
        self.availability_entry.grid(column=3, row=0)
                            
        usage_label = tk.Label(add_frame, font=('Helvetica', 14), text='Usage:', bg=color)
        usage_label.grid(column=4, row=0, padx=(0,3))
        self.usage_entry = tk.Entry(add_frame, font=('Helvetica', 12), width=12, bg='#d1d4d7')
        self.usage_entry.insert(0, 'ex. Zumba')
        self.usage_entry.bind("<FocusIn>", self.clear_usage)
        self.usage_entry.grid(column=5, row=0)

        button_border = tk.Frame(add_frame, highlightbackground="Blue",  highlightthickness=1, bd=0) 
        button_border.grid(column=9, row=0, padx=(15,0))
        update_button = tk.Button(button_border, text="U", font=('Helvetica', 12), border=0, bg='#0ab6f5', cursor='hand2', command=self.update_room, anchor='center', activebackground='#66d1f9')
        update_button.pack(anchor='center')

        self.status = tk.StringVar()
        self.status.set('Status: ')
        status_label = tk.Label(self.room_edit_frame, textvariable=self.status, font=('Helvetica', 14), anchor='w', bg=color)
        status_label.pack( fill='x', padx=(15,0), pady=10)

        update_room.protocol('WM_DELETE_WINDOW', lambda: self.destroy_and_repopulate(update_room))

    def clear_room(self, e):
        if 'ex.' in self.room_entry.get():
            self.room_entry.delete(0,"end")

    def clear_availability(self, e):
        if 'ex.' in self.availability_entry.get():
            self.availability_entry.delete(0,"end")

    def clear_usage(self, e):
        if 'ex.' in self.usage_entry.get():
            self.usage_entry.delete(0,"end")

    def update_room(self):
        room = self.room_entry.get()
        availability = self.availability_entry.get()
        usage = self.usage_entry.get()

        if 'ex.' in room or ('ex.' in availability and 'ex.' in usage):
            self.status.set('Status: Update unsuccessful. Missing fields room/ availability/ usage.')
        elif room == '' or (availability == '' and usage == ''):
            self.status.set('Status: Update unsuccessful. Missing fields room/ availability/ usage.')
        elif re.search(r"^\d*$", room) == None:
            self.status.set(f'Status: Update unsuccessful. Room \'{room}\' is invalid')
        elif self.qapi.get_room_by_id(room) == None:
            self.status.set(f'Status: Update Unsuccessful. Room \'{room}\' not found.')
        else:
            self.qapi.update_room_by_id(room, availability, usage)
            self.room_entry.delete(0, 'end')
            self.availability_entry.delete(0, 'end')
            self.usage_entry.delete(0, 'end')
            self.status.set(f'Status: room \'{room}\' successfully updated.')

    def destroy_and_repopulate(self, update_room):
        update_room.destroy()
        self.room_display_frame.destroy()
        self.button_border.destroy()
        self.room_display_frame = tk.Frame(self.room_frame, bg=self.background)
        self.room_display_frame.pack(fill='x')

        self.create_room_titles(self.room_display_frame)
        self.populate_room(self.room_display_frame)