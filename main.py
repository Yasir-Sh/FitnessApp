import tkinter as tk
from src.app.registration.registration import *

class StartApplication:
    def __init__(self):
        self.root = tk.Tk()
        self.root.geometry("%dx%d+%d+%d" % (350, 250, (self.root.winfo_screenwidth()/2 - 350/2), (self.root.winfo_screenheight()/2 - 250/2)))
        self.root.title("Fitness App")
        self.root.resizable(width=False, height=False)
        self.stop_bit = False

        RegistrationPage(self.root)
        self.root.protocol('WM_DELETE_WINDOW', self.close)
        self.root.mainloop()
    
    def close(self):
        self.stop_bit = True
        self.root.destroy()
    
    def get_stop_bit(self):
        return self.stop_bit

stop_bit = False
while not stop_bit:
    app = StartApplication()
    stop_bit = app.get_stop_bit()
