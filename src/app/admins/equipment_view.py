import tkinter as tk 
from src.db_oper.db_api import *
import re

class EquipmentView:
    def __init__(self, equipment_frame, admin_id):
        self.equipment_frame = equipment_frame
        self.qapi = QueryAPI()
        self.background = '#ebeceb'
        self.admin_id = admin_id

        self.equipment_display_frame = tk.Frame(self.equipment_frame, bg=self.background)
        self.equipment_display_frame.pack(fill='x')

        self.create_equipment_titles(self.equipment_display_frame)
        self.populate_equipment(self.equipment_display_frame)     

    def create_equipment_titles(self, equipment_display_frame):
        equipment_display_frame.columnconfigure(0, minsize=110)
        equipment_display_frame.columnconfigure(1, minsize=143)
        equipment_display_frame.columnconfigure(2, minsize=112)

        equipment_label = tk.Label(equipment_display_frame, text='Id', font=('Helvetica', 14), bg=self.background)
        equipment_label.grid(row=0, column=0, sticky='w', padx=(15,0), pady=(0,5))

        name_label = tk.Label(equipment_display_frame, text='Name', font=('Helvetica', 14), bg=self.background)
        name_label.grid(row=0, column=1, sticky='w')

        status_label = tk.Label(equipment_display_frame, text='Status', font=('Helvetica', 14), bg=self.background)
        status_label.grid(row=0, column=2, sticky='w')

    def populate_equipment(self, equipment_display_frame):
        equipments = self.qapi.get_all_equipments()
        equipments.sort()
        cur_row = 0

        if len(equipments) != 0:
            for equipment in equipments:
                cur_row += 1
                for i in range(0, len(equipment)): 
                    if equipment[i] == None:
                        equipment_label = tk.Label(equipment_display_frame, text='No Use', font=('Helvetica', 12), bg=self.background)
                    else:
                        equipment_label = tk.Label(equipment_display_frame, text=equipment[i], font=('Helvetica', 12), bg=self.background)
                    if i == 0:
                        equipment_label.grid(row=cur_row, column=i, sticky='w', padx=(15,0))
                    else:
                        equipment_label.grid(row=cur_row, column=i, sticky='w')
        
        self.button_border = tk.Frame(self.equipment_frame, highlightbackground="Blue",  highlightthickness=1, bd=0) 
        self.button_border.pack(anchor='se', padx=(0,15))
        edit_button = tk.Button(self.button_border, text="Edit", font=('Helvetica', 12), border=0, bg='#0ab6f5', cursor='hand2', command=self.edit_equipment, anchor='center', activebackground='#66d1f9', width=6)
        edit_button.pack()

    def edit_equipment(self):
        color='#ebeceb'
        update_equipment = tk.Toplevel()
        update_equipment.geometry("%dx%d+%d+%d" % (750, 150, (update_equipment.winfo_screenwidth()/2 - 750/2), (update_equipment.winfo_screenheight()/2 - 70/2)))
        update_equipment.resizable(width=False, height=False)
        update_equipment.grab_set()
        update_equipment.title("Update equipment")

        self.equipment_edit_frame = tk.Frame(update_equipment, bg=color,  highlightbackground='#7db6b5', highlightthickness=1)
        self.equipment_edit_frame.pack(fill='both', expand=True, padx=5, pady=10)

        equipment_edit_label = tk.Label(self.equipment_edit_frame, text=f"Edit Equipment", font=('Helvetica', 20), anchor='w', bg=color)
        equipment_edit_label.pack(fill='x', padx=(15,0), pady=(0, 5))

        add_frame = tk.Frame(self.equipment_edit_frame, bg=color)
        add_frame.pack(fill='x', padx=(15,0))

        equipment_label = tk.Label(add_frame, font=('Helvetica', 14), text='Equipment Id:', bg=color)
        equipment_label.grid(column=0, row=0, padx=(0,3))
        self.equipment_entry = tk.Entry(add_frame, font=('Helvetica', 12), width=12, bg='#d1d4d7')
        self.equipment_entry.insert(0, 'ex. 1')
        self.equipment_entry.bind("<FocusIn>", self.clear_equipment)
        self.equipment_entry.grid(column=1, row=0)

        name_label = tk.Label(add_frame, font=('Helvetica', 14), text='Name:', bg=color)
        name_label.grid(column=2, row=0, padx=(0,3))
        self.name_entry = tk.Entry(add_frame, font=('Helvetica', 12), width=12, bg='#d1d4d7')
        self.name_entry.insert(0, 'ex. Dumbells')
        self.name_entry.bind("<FocusIn>", self.clear_name)
        self.name_entry.grid(column=3, row=0)
                            
        status_label = tk.Label(add_frame, font=('Helvetica', 14), text='Status:', bg=color)
        status_label.grid(column=4, row=0, padx=(0,3))
        self.status_entry = tk.Entry(add_frame, font=('Helvetica', 12), width=12, bg='#d1d4d7')
        self.status_entry.insert(0, 'ex. Damaged')
        self.status_entry.bind("<FocusIn>", self.clear_status)
        self.status_entry.grid(column=5, row=0)

        button_border = tk.Frame(add_frame, highlightbackground="Green",  highlightthickness=1, bd=0) 
        button_border.grid(column=8, row=0, padx=(15,0))
        add_button = tk.Button(button_border, text="A", font=('Helvetica', 12), border=0, bg='#37c876', cursor='hand2', command=self.add_equipment, anchor='center', activebackground='#27d881')
        add_button.pack(anchor='center')

        button_border = tk.Frame(add_frame, highlightbackground="Blue",  highlightthickness=1, bd=0) 
        button_border.grid(column=9, row=0, padx=(15,0))
        update_button = tk.Button(button_border, text="U", font=('Helvetica', 12), border=0, bg='#0ab6f5', cursor='hand2', command=self.update_equipment, anchor='center', activebackground='#66d1f9')
        update_button.pack(anchor='center')

        button_border = tk.Frame(add_frame, highlightbackground="Red",  highlightthickness=1, bd=0) 
        button_border.grid(column=10, row=0, padx=(15,0),)
        delete_button = tk.Button(button_border, text="D", font=('Helvetica', 12), border=0, bg='#e76e72', cursor='hand2', command=self.delete_equipment, anchor='center', activebackground='#ee9a9d')
        delete_button.pack(anchor='center')

        self.status = tk.StringVar()
        self.status.set('Status: ')
        status_label = tk.Label(self.equipment_edit_frame, textvariable=self.status, font=('Helvetica', 14), anchor='w', bg=color)
        status_label.pack( fill='x', padx=(15,0), pady=10)

        update_equipment.protocol('WM_DELETE_WINDOW', lambda: self.destroy_and_repopulate(update_equipment))

    def clear_equipment(self, e):
        if 'ex.' in self.equipment_entry.get():
            self.equipment_entry.delete(0,"end")

    def clear_name(self, e):
        if 'ex.' in self.name_entry.get():
            self.name_entry.delete(0,"end")

    def clear_status(self, e):
        if 'ex.' in self.status_entry.get():
            self.status_entry.delete(0,"end")

    def add_equipment(self):
        equipment = self.equipment_entry.get()
        name = self.name_entry.get()
        status = self.status_entry.get()

        if 'ex.' in equipment or 'ex.' in name:
            self.status.set('Status: Add unsuccessful. Missing fields equipment id/ name.')
        elif equipment == '' or name == '':
            self.status.set('Status: Add unsuccessful. Missing fields equipment id/ name.')
        elif re.search(r"^\d*$", equipment) == None:
            self.status.set(f'Status: Add unsuccessful. Equipment Id \'{equipment}\' is invalid')
        elif self.qapi.get_equipment_by_id(equipment) != None:
            self.status.set(f'Status: Add Unsuccessful. Equipment \'{name}\' already exists, try UPDATE instead.')
        else:
            self.qapi.add_equipment_by_id(equipment, name, status)
            self.equipment_entry.delete(0, 'end')
            self.name_entry.delete(0, 'end')
            self.status_entry.delete(0, 'end')
            self.status.set(f'Status: Equipment \'{name}\' successfully added.')

    def delete_equipment(self):
        equipment = self.equipment_entry.get()

        if 'ex.' in equipment:
            self.status.set('Status: Delete unsuccessful. Missing fieldsequipment id.')
        elif equipment == '':
            self.status.set('Status: Delete unsuccessful. Missing field equipment id.')
        elif re.search(r"^\d*$", equipment) == None:
            self.status.set(f'Status: Delete unsuccessful. Equipment id \'{equipment}\' is invalid')
        elif self.qapi.get_equipment_by_id(equipment) == None:
            self.status.set(f'Status: Delete Unsuccessful. Equipment id \'{equipment}\' not found.')
        else:
            self.qapi.delete_equipment_by_id(equipment)
            self.equipment_entry.delete(0, 'end')
            self.name_entry.delete(0, 'end')
            self.status_entry.delete(0, 'end')
            self.status.set(f'Status: Equipment Id \'{equipment}\' successfully deleted.')

    def update_equipment(self):
        equipment = self.equipment_entry.get()
        name = self.name_entry.get()
        status = self.status_entry.get()

        if 'ex.' in equipment or ('ex.' in name and 'ex.' in status):
            self.status.set('Status: Update unsuccessful. Missing fields equipment id/ name.')
        elif equipment == '' or (name == '' and status == ''):
            self.status.set('Status: Update unsuccessful. Missing fields equipment id/ name.')
        elif re.search(r"^\d*$", equipment) == None:
            self.status.set(f'Status: Update unsuccessful. Equipment id \'{equipment}\' is invalidd')
        elif self.qapi.get_equipment_by_id(equipment) == None:
            self.status.set(f'Status: Update Unsuccessful. Equipment id \'{equipment}\' not found.')
        else:
            self.qapi.update_equipment_by_id(equipment, name, status)
            self.equipment_entry.delete(0, 'end')
            self.name_entry.delete(0, 'end')
            self.status_entry.delete(0, 'end')
            self.status.set(f'Status: equipment \'{equipment}\' successfully updated.')

    def destroy_and_repopulate(self, update_equipment):
        update_equipment.destroy()
        self.equipment_display_frame.destroy()
        self.button_border.destroy()
        self.equipment_display_frame = tk.Frame(self.equipment_frame, bg=self.background)
        self.equipment_display_frame.pack(fill='x')

        self.create_equipment_titles(self.equipment_display_frame)
        self.populate_equipment(self.equipment_display_frame)