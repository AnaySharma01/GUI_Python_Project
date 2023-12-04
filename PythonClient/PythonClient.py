import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter import font
from tkinter import messagebox

root = tk.Tk()
root.configure(bg = '#639c8f')
root.geometry('500x500')
root.title('Python Client')
root.resizable(False,False)
display_label1 = Label(root,text="Control Panel: ",bg = '#639c8f',fg='#e21d76',font = 'bold')
display_label1.grid(row = 1, column = 0)
def moveForward():
   msg = messagebox.showinfo("Robot Moved", "Forward")
forward = Button(text ="↑", command = moveForward)
forward.grid(row = 3, column = 1)
def moveLeft():
   msg = messagebox.showinfo("Robot Moved", "Left")
left = Button(text ="←", command = moveLeft)
left.grid(row = 5, column = 0)
def moveRight():
   msg=messagebox.showinfo("Robot Moved", "Right")
right = Button(text ="→", command = moveRight)
right.grid(row = 5, column = 2)
def moveBackward():
   msg=messagebox.showinfo("Robot Moved", "Backward")
backward = Button(text ="↓", command = moveBackward)
backward.grid(row = 8, column = 1)
def Start():
   msg = messagebox.showinfo("Robot", "Started")
start = Button(text ="🟢", command = Start)
start.grid(row = 4, column = 1)

start = Button(text ="")
start.grid(row = 5, column = 1)

def Stop():
   msg=messagebox.showinfo("Robot", "Stopped")
stop = Button(text ="🛑", command = Stop)
stop.grid(row = 6, column = 1)

display_label2 = Label(root,text="Log History: ",bg = '#639c8f',fg='#e21d76',font = 'bold')
display_label2.grid(row = 15, column = 0)

display_label3 = Label(root,text="Video Feed: ",bg = '#639c8f',fg='#e21d76',font = 'bold')
display_label3.grid(row = 1, column = 12)

display_label2 = Label(root,text="Blank Feed: ",bg = '#639c8f',fg='#e21d76',font = 'bold')
display_label2.grid(row = 15, column = 12)

blanklabel = Label(root, text = "", bg = '#639c8f',fg='#e21d76')
blanklabel.grid(row = 15, column = 12)

exit_button = tk.Button(root, text = 'Logout', bg='#A877BA',font = 'bold', command = root.destroy)
exit_button.grid(row = 20, column = 12)

root.mainloop()
