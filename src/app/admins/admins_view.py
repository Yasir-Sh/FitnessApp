import tkinter as tk
from src.db_oper.db_api import *
from tkinter import ttk
from src.app.admins.room_view import *
from src.app.admins.equipment_view import *
from src.app.admins.class_view import *
from src.app.admins.billing_view import *


class AdminView:
    def __init__(self, root, admin_id):
        self.root = root
        self.root.geometry("%dx%d+%d+%d" % (700, 800, (self.root.winfo_screenwidth()/2 - 700/2), (self.root.winfo_screenheight()/2 - 800/2)))
        self.admin_id = admin_id
        self.qapi = QueryAPI()
        self.background = '#ebeceb'

        admin_view_frame = tk.Frame(self.root, bg=self.background, highlightbackground='#7db6b5', highlightthickness=1)
        admin_view_frame.pack(fill='both', expand=True, padx=10, pady=10)

        room_label = tk.Label(admin_view_frame, text="Rooms", font=('Helvetica', 20), anchor='w', bg=self.background)
        room_label.pack(fill='x', padx=(15,0), pady=10)

        room_frame = tk.Frame(admin_view_frame, bg=self.background)
        room_frame.pack(fill='x')
        RoomView(room_frame, self.admin_id)

        seperator = ttk.Separator(admin_view_frame, orient='horizontal')
        seperator.pack(fill='x', pady=(20,0))

        equipment_label = tk.Label(admin_view_frame, text="Equipment", font=('Helvetica', 20), anchor='w', bg=self.background)
        equipment_label.pack(fill='x', padx=(15,0), pady=10)

        equipment_frame = tk.Frame(admin_view_frame, bg=self.background, height=200)
        equipment_frame.pack(fill='x')
        EquipmentView(equipment_frame, self.admin_id)

        seperator = ttk.Separator(admin_view_frame, orient='horizontal')
        seperator.pack(fill='x', pady=(10,0))

        class_label = tk.Label(admin_view_frame, text="Class Schedule", font=('Helvetica', 20), anchor='w', bg=self.background)
        class_label.pack(fill='x', padx=(15,0), pady=(10,5))

        class_frame = tk.Frame(admin_view_frame, bg=self.background)
        class_frame.pack(fill='x')
        ClassView(class_frame, admin_id)

        buttons_frame = tk.Frame(admin_view_frame, bg=self.background)
        buttons_frame.pack(fill='both', expand=True)

        buttons_frame.columnconfigure(0, weight=400)
        buttons_frame.rowconfigure(0, weight=400)

        BillingView(buttons_frame, self.admin_id)

        button_border = tk.Frame(buttons_frame, highlightbackground="Red",  highlightthickness=1, bd=0) 
        button_border.grid(column=1, row=0, padx=10, pady=5, sticky='se')
        logout_button = tk.Button(button_border, text="Logout", font=('Helvetica', 12), border=0, bg='#e76e72', cursor='hand2', anchor='center', activebackground='#ee9a9d', command=self.logout)
        logout_button.pack()

    def logout(self):
        self.root.destroy()
        