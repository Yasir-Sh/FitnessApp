import tkinter as tk
import db_oper.db_api as db
import app.members.members_view as members_view
import app.trainers.trainers_view as trainers_view
import app.admins.admins_view as admins_view


class RegistrationPage:
    def __init__(self, root):
        self.root = root
        self.select_user()
    
    def setup_page(self, user):
        bg_color = '#21c8d7'
        fg_text_color = 'BLACK'
        bg_widget_color = 'WHITE'

        self.select_user_frame.forget()
        self.login_frame = tk.Frame(self.root, bg=bg_color)
        self.login_frame.pack(fill='both', expand=True)

        username_label = tk.Label(self.login_frame, text="Username", font=('Helvetica', 12), anchor="sw", width=18, height=2, bg=bg_color, fg=fg_text_color)
        username_label.pack(padx=20)

        self.username_entry = tk.Entry(self.login_frame, font=('Helvetica', 12), width=18, bg=bg_widget_color)
        self.username_entry.pack(padx=20)

        password_label = tk.Label(self.login_frame, text="Password", font=('Helvetica', 12), anchor="sw", width=18, height=2, bg=bg_color, fg=fg_text_color)
        password_label.pack(padx=20)

        self.password_entry = tk.Entry(self.login_frame, font=('Helvetica', 12), width=18, bg=bg_widget_color, show='*')
        self.password_entry.pack(padx=20)
        
        button_border = tk.Frame(self.login_frame, highlightbackground="Green",  highlightthickness=1, bd=0) 
        button_border.pack(pady=(20,0))
        button = tk.Button(button_border, text="Register", font=('Helvetica', 14, 'bold'), width=11, background='#37c876', activebackground='#27d881', border=0, command= lambda: self.validate_input(user), cursor='hand2')
        button.pack()

        button_border = tk.Frame(self.login_frame, highlightbackground="Blue",  highlightthickness=1, bd=0) 
        button_border.pack(pady=10)
        back_button = tk.Button(button_border, text="Go Back", font=('Helvetica', 14, 'bold'), width=11, bg='#0ab6f5', activebackground='#66d1f9', border=0, command= lambda: self.back_to_select(self.login_frame) , cursor='hand2')
        back_button.pack()

    def validate_input(self, user):
        username, password = self.username_entry.get(), self.password_entry.get()
        if len(username.strip()) == 0 or len(password.strip()) == 0:
            self.invalid_registration("Username or Password", user)
        else:
            self.register_user(user, username, password)


    def invalid_registration(self, error, user):
        self.login_frame.pack_forget()

        error_frame = tk.Frame(self.root)
        error_frame.pack(fill='both', expand=True)

        error_labal = tk.Label(error_frame, text=f"Invalid {error}.", font=('Helvetica', 14))
        error_labal.pack()

        button_border = tk.Frame(error_frame, highlightbackground="Green",  highlightthickness=1, bd=0) 
        button_border.pack(pady=20)
        button = tk.Button(button_border, text="Try Again", font=('Helvetica', 14, 'bold'), width=12, background='#37c876', activebackground='#27d881', border=0, command= lambda: self.back_to_regestration(error_frame, user), cursor='hand2')
        button.pack()

    def back_to_select(self, login_frame):
        login_frame.destroy()
        self.select_user_frame.pack(fill='both', expand=True, pady=5, padx=5)

    def back_to_regestration(self, error_frame, user):
        error_frame.destroy()
        # self.login_frame.destroy()
        self.setup_page(user)

    def select_user(self):
        self.select_user_frame = tk.Frame(self.root, bg='#ebeceb',  highlightbackground='#7db6b5', highlightthickness=1)
        self.select_user_frame.pack(fill='both', expand=True, pady=5, padx=5)

        select_user_label = tk.Label(self.select_user_frame, text="Choose your purpose", font=('Helvetica', 14))
        select_user_label.pack(pady=20)

        button_border = tk.Frame(self.select_user_frame, highlightbackground="Green",  highlightthickness=1, bd=0) 
        button_border.pack(pady=5)
        member_button = tk.Button(button_border, text='Member', font=('Helvetica', 12), border=0, bg='#37c876', activebackground='#27d881', width=20, height=2, command= lambda: self.setup_page('member') , cursor='hand2')
        member_button.pack()

        button_border = tk.Frame(self.select_user_frame, highlightbackground="Blue",  highlightthickness=1, bd=0) 
        button_border.pack(pady=5)
        trainer_button = tk.Button(button_border, text='Trainer', font=('Helvetica', 12), border=0, bg='#0ab6f5', activebackground='#66d1f9', width=20, height=2, command= lambda: self.setup_page('trainer'), cursor='hand2')
        trainer_button.pack()

        button_border = tk.Frame(self.select_user_frame, highlightbackground="#6e7479",  highlightthickness=1, bd=0) 
        button_border.pack(pady=5)
        admin_button = tk.Button(button_border, text='Admin', font=('Helvetica', 12), border=0, bg='#b6b6b6', activebackground='Light Gray',  width=20, height=2, command= lambda: self.setup_page('admin'), cursor='hand2')
        admin_button.pack()
        
    def register_user(self, user, username, password):
        qapi = db.QueryAPI()
        if user == 'member':
            if qapi.get_member_username_by_username(username) == None:
                self.select_user_frame.destroy()
                self.login_frame.destroy()

                qapi.add_member(username, password)
                members_view.MembersView(self.root, qapi.get_member_id_by_username(username))
            elif qapi.get_member_password_by_username(username) == password:
                self.select_user_frame.destroy()
                self.login_frame.destroy()
                members_view.MembersView(self.root, qapi.get_member_id_by_username(username))
            else:  
                self.login_frame.destroy()
                self.invalid_registration("Password", user)
        elif user == 'trainer':
            if qapi.get_trainer_username_by_username(username) == None:
                self.select_user_frame.destroy()
                self.login_frame.destroy()

                qapi.add_trainer_by_username(username, password)
                trainers_view.TrainersView(self.root, qapi.get_trainer_id_by_username(username))
            elif qapi.get_trainer_password_by_username(username) == password:
                self.select_user_frame.destroy()
                self.login_frame.destroy()
                trainers_view.TrainersView(self.root, qapi.get_trainer_id_by_username(username))
            else:  
                self.login_frame.destroy()
                self.invalid_registration("Password", user)
        else:
            if qapi.get_admin_username_by_username(username) == None:
                self.select_user_frame.destroy()
                self.login_frame.destroy()

                qapi.add_admin_by_username(username, password)
                admins_view.AdminView(self.root, qapi.get_admin_id_by_username(username))
            elif qapi.get_admin_password_by_username(username) == password:
                self.select_user_frame.destroy()
                self.login_frame.destroy()
                admins_view.AdminView(self.root, qapi.get_admin_id_by_username(username))
            else:  
                self.login_frame.destroy()
                self.invalid_registration("Password", user)

