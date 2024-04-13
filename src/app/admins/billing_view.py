import tkinter as tk
from db_oper.db_api import *
from tkinter import ttk
import re

class BillingView:
    def __init__(self, button_frame, admin_id):
        self.button_frame = button_frame
        self.qapi = QueryAPI()
        self.background = '#ebeceb'
        self.admin_id = admin_id

        self.button_border = tk.Frame(self.button_frame, highlightbackground="Green",  highlightthickness=1, bd=0) 
        self.button_border.grid(column=0, row=0, sticky='se', pady=5)

        edit_button = tk.Button(self.button_border, text="Billing", font=('Helvetica', 12), border=0, bg='#37c876', cursor='hand2', command=self.billing_page, anchor='center', activebackground='#27d881', width=6)
        edit_button.pack()
    
    def billing_page(self):
        color='#ebeceb'
        modify_bill = tk.Toplevel()
        modify_bill.geometry("%dx%d+%d+%d" % (900, 400, (modify_bill.winfo_screenwidth()/2 - 900/2), (modify_bill.winfo_screenheight()/2 - 400/2)))
        modify_bill.resizable(width=False, height=False)
        modify_bill.grab_set()
        modify_bill.resizable(width=False, height=False)
        modify_bill.title("Update bill")


        self.billing_frame = tk.Frame(modify_bill, bg=color,  highlightbackground='#7db6b5', highlightthickness=1)
        self.billing_frame.pack(fill='both', expand=True, padx=15, pady=15)

        billing_label = tk.Label(self.billing_frame, text="Billings", font=('Helvetica', 20), anchor='w', bg=self.background)
        billing_label.pack(fill='x', padx=(15,0), pady=10)

        self.billing_display_frame = tk.Frame(self.billing_frame, bg=color)
        self.billing_display_frame.pack(fill='x')

        self.create_bill_titles(self.billing_display_frame)
        self.populate_bill(self.billing_display_frame)

        self.seperator = ttk.Separator(self.billing_frame, orient='horizontal')
        self.seperator.pack(fill='x', pady=(10,0))

        self.edit_billing_label = tk.Label(self.billing_frame, text="Edit Billings", font=('Helvetica', 20), anchor='w', bg=self.background)
        self.edit_billing_label.pack(fill='x', padx=(15,0), pady=10)

        self.add_frame = tk.Frame(self.billing_frame, bg=color)
        self.add_frame.pack(fill='x', padx=(15,0), pady=(10,0))

        bill_label = tk.Label(self.add_frame, font=('Helvetica', 14), text='Bill Id:', bg=color)
        bill_label.grid(column=0, row=0, padx=(0,3))
        self.bill_entry = tk.Entry(self.add_frame, font=('Helvetica', 12), width=8, bg='#d1d4d7')
        self.bill_entry.insert(0, 'ex. 1')
        self.bill_entry.bind("<FocusIn>", self.clear_bill)
        self.bill_entry.grid(column=1, row=0, padx=(0,5))

        name_label = tk.Label(self.add_frame, font=('Helvetica', 14), text='Member Name:', bg=color)
        name_label.grid(column=2, row=0, padx=(0,3))
        self.name_entry = tk.Entry(self.add_frame, font=('Helvetica', 12), width=8, bg='#d1d4d7')
        self.name_entry.insert(0, 'ex. Yasir')
        self.name_entry.bind("<FocusIn>", self.clear_name)
        self.name_entry.grid(column=3, row=0,padx=(0,6))
                            
        amount_label = tk.Label(self.add_frame, font=('Helvetica', 14), text='Amount:', bg=color)
        amount_label.grid(column=4, row=0, padx=(0,3))
        self.amount_entry = tk.Entry(self.add_frame, font=('Helvetica', 12), width=8, bg='#d1d4d7')
        self.amount_entry.insert(0, 'ex. 45.50')
        self.amount_entry.bind("<FocusIn>", self.clear_amount)
        self.amount_entry.grid(column=5, row=0, padx=(0,5))

        item_label = tk.Label(self.add_frame, font=('Helvetica', 14), text='Item:', bg=color)
        item_label.grid(column=6, row=0, padx=(0,3))
        self.item_entry = tk.Entry(self.add_frame, font=('Helvetica', 12), width=8, bg='#d1d4d7')
        self.item_entry.insert(0, 'ex. Zumba')
        self.item_entry.bind("<FocusIn>", self.clear_item)
        self.item_entry.grid(column=7, row=0)

        button_border = tk.Frame(self.add_frame, highlightbackground="Green",  highlightthickness=1, bd=0) 
        button_border.grid(column=8, row=0, padx=(15,0))
        add_button = tk.Button(button_border, text="A", font=('Helvetica', 12), border=0, bg='#37c876', cursor='hand2', command=self.add_bill, anchor='center', activebackground='#27d881')
        add_button.pack(anchor='center')

        button_border = tk.Frame(self.add_frame, highlightbackground="Blue",  highlightthickness=1, bd=0) 
        button_border.grid(column=9, row=0, padx=(15,0))
        update_button = tk.Button(button_border, text="U", font=('Helvetica', 12), border=0, bg='#0ab6f5', cursor='hand2', command=self.update_bill, anchor='center', activebackground='#66d1f9')
        update_button.pack(anchor='center')

        button_border = tk.Frame(self.add_frame, highlightbackground="Red",  highlightthickness=1, bd=0) 
        button_border.grid(column=10, row=0, padx=(15,0),)
        delete_button = tk.Button(button_border, text="D", font=('Helvetica', 12), border=0, bg='#e76e72', cursor='hand2', command=self.delete_bill, anchor='center', activebackground='#ee9a9d')
        delete_button.pack(anchor='center')

        self.status = tk.StringVar()
        self.status.set('Status: ')
        self.status_label = tk.Label(self.billing_frame, textvariable=self.status, font=('Helvetica', 14), anchor='w', bg=color)
        self.status_label.pack( fill='x', padx=(15,0), pady=(5,10))

    def create_bill_titles(self, bill_display_frame):
        bill_display_frame.columnconfigure(0, minsize=110)
        bill_display_frame.columnconfigure(1, minsize=143)
        bill_display_frame.columnconfigure(2, minsize=112)

        bill_label = tk.Label(bill_display_frame, text='Bill Id', font=('Helvetica', 14), bg=self.background)
        bill_label.grid(row=0, column=0, sticky='w', padx=(15,0), pady=(0,5))

        name_label = tk.Label(bill_display_frame, text='Name', font=('Helvetica', 14), bg=self.background)
        name_label.grid(row=0, column=1, sticky='w')

        amount_label = tk.Label(bill_display_frame, text='Amount', font=('Helvetica', 14), bg=self.background)
        amount_label.grid(row=0, column=2, sticky='w')

        amount_label = tk.Label(bill_display_frame, text='Item', font=('Helvetica', 14), bg=self.background)
        amount_label.grid(row=0, column=3, sticky='w')

    def populate_bill(self, bill_display_frame):
        bills = self.qapi.get_all_bills()
        bills.sort()
        cur_row = 0

        if len(bills) != 0:
            for bill in bills:
                cur_row += 1
                for i in range(0, len(bill)): 
                    if bill[i] == None:
                        bill_label = tk.Label(bill_display_frame, text='No Use', font=('Helvetica', 12), bg=self.background)
                    elif i == 1:
                        bill_label = tk.Label(bill_display_frame, text=self.qapi.get_member_username_by_id(bill[i])[0], font=('Helvetica', 12), bg=self.background)
                    else:
                        bill_label = tk.Label(bill_display_frame, text=bill[i], font=('Helvetica', 12), bg=self.background)
                    if i == 0:
                        bill_label.grid(row=cur_row, column=i, sticky='w', padx=(15,0))
                    else:
                        bill_label.grid(row=cur_row, column=i, sticky='w')
        

    def clear_bill(self, e):
        if 'ex.' in self.bill_entry.get():
            self.bill_entry.delete(0,"end")

    def clear_name(self, e):
        if 'ex.' in self.name_entry.get():
            self.name_entry.delete(0,"end")

    def clear_amount(self, e):
        if 'ex.' in self.amount_entry.get():
            self.amount_entry.delete(0,"end")

    def clear_item(self, e):
        if 'ex.' in self.item_entry.get():
            self.item_entry.delete(0,"end")

    def add_bill(self):
        bill = self.bill_entry.get()
        name = self.name_entry.get()
        amount = self.amount_entry.get()
        item = self.item_entry.get()

        if 'ex.' in bill or 'ex.' in name or 'ex.' in amount or 'ex' in item:
            self.status.set('Status: Add unsuccessful. Missing fields Bill id/ Member name/ Amount/ Item.')
        elif bill == '' or name == '' or amount == '' or item == '':
            self.status.set('Status: Add unsuccessful. Missing fields Bill id/ Member name/ Amount/ Item.')
        elif self.qapi.get_member_username_by_username(name) == None:
            self.status.set(f'Status: Add unsuccessful. Member \'{name}\' not found.')
        elif re.search(r"^\d*$", bill) == None or re.search(r"^\d*\.\d{2}", amount) == None:
            self.status.set(f'Status: Add unsuccessful. Bill/ Amount format is invalid')
        elif self.qapi.get_bill_by_id(bill) != None:
            self.status.set(f'Status: Add Unsuccessful. Bill id \'{bill}\' already exists, try UPDATE instead.')
        else:
            self.qapi.add_bill_by_id(bill, self.qapi.get_member_id_by_username(name), amount, item)
            self.bill_entry.delete(0, 'end')
            self.name_entry.delete(0, 'end')
            self.amount_entry.delete(0, 'end')
            self.item_entry.delete(0, 'end')
            self.status.set(f'Status: Billing to member \'{name}\' successfully added.')
            self.destroy_and_repopulate()

    def delete_bill(self):
        bill = self.bill_entry.get()

        if 'ex.' in bill:
            self.status.set('Status: Delete unsuccessful. Missing field bill id.')
        elif bill == '':
            self.status.set('Status: Delete unsuccessful. Missing field bill id.')
        elif re.search(r"^\d*$", bill) == None:
            self.status.set(f'Status: Delete unsuccessful. Bill id \'{bill}\' is invalid')
        elif self.qapi.get_bill_by_id(bill) == None:
            self.status.set(f'Status: Delete Unsuccessful. Bill id \'{bill}\' not found.')
        else:
            self.qapi.delete_bill_by_id(bill)
            self.bill_entry.delete(0, 'end')
            self.name_entry.delete(0, 'end')
            self.amount_entry.delete(0, 'end')
            self.item_entry.delete(0, 'end')
            self.status.set(f'Status: Bill id \'{bill}\' successfully deleted.')
            self.destroy_and_repopulate()

    def update_bill(self):
        bill = self.bill_entry.get()
        name = self.name_entry.get()
        amount = self.amount_entry.get()
        item = self.item_entry.get()

        if 'ex.' in bill or ('ex.' in name and 'ex.' in amount and 'ex.' in item):
            self.status.set('Status: Update unsuccessful. Missing fields Bill id/ Member name/ Amount/ Item.')
        elif bill == '' or (name == '' and amount == '' and item == ''):
            self.status.set('Status: Update unsuccessful. Missing fields Bill id/ Member name/ Amount/ Item.')
        elif re.search(r"^\d*$", bill) == None or (re.search(r"^\d*\.\d{2}", amount) == None and ((name == '' or 'ex.' in name) and (item == '' or 'ex.' in item))):
            self.status.set(f'Status: Update unsuccessful. Bill/ Amount format is invalid')
        elif self.qapi.get_bill_by_id(bill) == None:
            self.status.set(f'Status: Update Unsuccessful. Bill id \'{bill}\' not found.')
        elif self.qapi.get_member_username_by_username(name) == None and ((amount == '' or 'ex.' in amount) and (item == '' or 'ex.' in item)):
            self.status.set(f'Status: Update Unsuccessful. Member \'{name}\' not found.')
        else:
            if name == '' or 'ex' in name:
                self.qapi.update_bill_by_id(bill, name, amount, item)
            else:
                self.qapi.update_bill_by_id(bill, self.qapi.get_member_id_by_username(name), amount, item)
            self.bill_entry.delete(0, 'end')
            self.name_entry.delete(0, 'end')
            self.amount_entry.delete(0, 'end')
            self.item_entry.delete(0, 'end')
            self.status.set(f'Status: Bill id \'{bill}\' successfully updated.')
            self.destroy_and_repopulate()
    
    def destroy_and_repopulate(self):
        self.billing_display_frame.destroy()
        self.status_label.pack_forget()
        self.add_frame.pack_forget()
        self.seperator.pack_forget()
        self.edit_billing_label.pack_forget()
        self.billing_display_frame = tk.Frame(self.billing_frame, bg=self.background)
        self.billing_display_frame.pack(fill='x')

        self.create_bill_titles(self.billing_display_frame)
        self.populate_bill(self.billing_display_frame)

        self.seperator.pack(fill='x', pady=(10,0))
        self.edit_billing_label.pack(fill='x', padx=(15,0), pady=10)
        self.add_frame.pack(fill='x', padx=(15,0), pady=(10,0))
        self.status_label.pack( fill='x', padx=(15,0), pady=(5,10))
        
        