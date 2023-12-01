import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter import font
from tkinter import messagebox
import requests

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        SERVER_URL = "http://192.168.1.17:4444/";
        url1 = requests.get("http://192.168.1.17:4444/forward/")
        url2 = requests.get("http://192.168.1.17:4444/left/")
        url3 = requests.get("http://192.168.1.17:4444/right/")
        url4 = requests.get("http://192.168.1.17:4444/backward/")
        url5 = requests.get("http://192.168.1.17:4444/stop/")
        self.configure(bg='#639c8f')
        self.geometry('500x500')
        self.title('Python Client')
        self.resizable(False, False)

        display_label1 = Label(self, text="Control Panel: ", bg='#639c8f', fg='#e21d76', font='bold')
        display_label1.grid(row=1, column=0, sticky=tk.NW, padx=0, pady=0)

        def moveForward():
            forward = url1.json()
            return forward
            msg = messagebox.showinfo("Robot Moved", "Forward")

        forward = Button(text="↑", command=moveForward)
        forward.grid(row=3, column=1)

        def moveLeft():
            left = url2.json()
            return left
            msg = messagebox.showinfo("Robot Moved", "Left")

        left = Button(text="←", command=moveLeft)
        left.grid(row=5, column=0)

        def moveRight():
            right = url3.json()
            return right
            msg = messagebox.showinfo("Robot Moved", "Right")

        right = Button(text="→", command=moveRight)
        right.grid(row=5, column=2)

        def moveBackward():
            backward = url4.json()
            return backward
            msg = messagebox.showinfo("Robot Moved", "Backward")

        backward = Button(text="↓", command=moveBackward)
        backward.grid(row=8, column=1)

        def Start():
            msg = messagebox.showinfo("Robot", "Started")

        start = Button(text="🟢", command=Start)
        start.grid(row=4, column=1)

        start = Button(text="")
        start.grid(row=5, column=1)

        def Stop():
            stop = url5.json()
            return stop
            msg = messagebox.showinfo("Robot", "Stopped")

        stop = Button(text="🛑", command=Stop)
        stop.grid(row=6, column=1)

        blanklabel = Label(self, text="", bg='#639c8f', fg='#e21d76')
        blanklabel.grid(row=15, column=12)

        display_label2 = Label(self, text="Log History: ", bg='#639c8f', fg='#e21d76', font='bold')
        display_label2.grid(row=15, column=0, sticky=tk.NE, ipadx=5, ipady=0)

        display_label3 = Label(self, text="Video Feed: ", bg='#639c8f', fg='#e21d76', font='bold')
        display_label3.grid(row=1, column=12, sticky=tk.SW, ipadx=0, ipady=5)

        display_label4 = Label(self, text="Blank Feed: ", bg='#639c8f', fg='#e21d76', font='bold')
        display_label4.grid(row=15, column=12, sticky=tk.SE, ipadx=5, ipady=5)

        exit_button = tk.Button(self, text='Logout', bg='#A877BA', font='bold', command=self.destroy)
        exit_button.grid(row=20, column=12)


if __name__ == "__main__":
    app = App()
    app.mainloop()
