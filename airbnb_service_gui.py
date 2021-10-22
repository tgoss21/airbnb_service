import tkinter as tk
from tkinter import *
from tkinter import messagebox
import tkinter
from airbnb_service import calculate_total

window = Tk()
window.geometry("500x500")
window.title("Airbnb Service")
frame = Frame(window)

label1 = Label(window, text="Airbnb Services", pady=25, font=("arial", 16, "bold",)).pack()


def helloCallBack():
       msg = messagebox.showinfo( "Text")
       
def calculate():
    calulationFee = calculate_total()
    messagebox.showinfo("Calculation", calulationFee)

B1 = Button(window, text = "Calculate Cleaning Fee", width=20, height=2, pady=1, command = calculate)
# B1.place(x = 20,y = -20)
B1.pack()

B2 = Button(window, text = "Update Calendar", width=20, height=2, pady=1, command = helloCallBack)
# B2.place(x = 50,y = 50)
B2.pack()

B3 = Button(window, text = "Notify Cleaners", width=20, height=2, pady=1, command = helloCallBack)
# B1.place(x = 20,y = -20)
B3.pack()

B4 = Button(window, text = "Edit Cleaning", width=20, height=2, pady=1, command = helloCallBack)
# B2.place(x = 50,y = 50)
B4.pack()

window.mainloop()
