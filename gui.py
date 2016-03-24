from tkinter import *
from tkinter import ttk
# import tkinter
import new_project


def clearText(event):
	filename_entry.delete(0,END)
	filename_entry.config(foreground="black")

lbl = None

def run():
	if(len(filename.get())>0 and filename.get()!='Enter the complete file path'):
		new_project.run(filename = filename.get())
	else:
		new_project.run(Code = text.get("1.0",END))
	text.grid_remove()
	global lbl
	lbl = ttk.Label(mainframe,text=new_project.S)
	lbl.grid(column=4,row=1,sticky=E)

		

def clr():

	if lbl!=None: lbl.grid_remove()
	text.grid()
	text.delete('0.0',END)
	filename_entry.delete(0,END)
	filename_entry.config(foreground="gray")
	filename_entry.insert(0,"Enter the complete file path")
	new_project.S = "\tID \tLINENUMBER\n"
	lbl['text'] = ""

def quit():
	exit(0)

root = Tk()
root.geometry("700x700+300+200")
root.title("Lexer")


mainframe = ttk.Frame(root,padding="3 3 12 12")
mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
mainframe.columnconfigure(0, weight=1)
mainframe.rowconfigure(0, weight=1)
filename = StringVar()

filename_entry = ttk.Entry(mainframe, width=30,textvariable=filename)
filename_entry.grid(column=1, row=1, sticky=E)
filename_entry.insert(0,"Enter the complete file path")
filename_entry.config(foreground="gray")
filename_entry.bind("<Button-1>",clearText)


tokenize_button = ttk.Button(mainframe, text="Tokenize", command=run).grid(column=2, row=2, sticky=W)
clear_button = ttk.Button(mainframe, text="Clear", command=clr).grid(column=2, row=3, sticky=W)
clear_button = ttk.Button(mainframe, text="Exit", command=quit).grid(column=2, row=4, sticky=W)

text = Text(mainframe, width=40, height=10, wrap= 'word')
text.grid(column = 10, row = 1, sticky = W)
text.insert(END,"Paste your code here...")
text.bind('<Button-1>',clearText)

for child in mainframe.winfo_children(): child.grid_configure(padx=5, pady=5)

root.mainloop()