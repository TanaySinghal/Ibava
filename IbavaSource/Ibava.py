from Tkinter import *
import tkFileDialog as filedialog

root = Tk()
root.title("Ibava - IB Pseudocode")
root.configure(bg = "#3366cc")

runButton = 'Run'

#Create method for button action (found in example)
action = lambda x = runButton: click_event()

#create input display
inputTextField = Text(root, width = 80, height = 20, bg = "#ffffcc", bd=0, highlightthickness=0)
inputTextField.grid(row = 0, column = 0, columnspan = 5, padx = 20, pady = (20,5))

#create button
button_style = 'raised'
button = Button(root, text = runButton, width = 5, height = 1, command = action)
button.grid(row = 1, column = 2, sticky = 'nesw')

#create output display
outputTextField = Text(root, width = 80, height = 10, bg = "#ffffcc", bd=0, highlightthickness=0)
outputTextField.grid(row = 2, column = 0, columnspan = 5, padx = 20, pady = (5,20))

#This is the menu bar class
class MenuBar:
    def __init__(self, root):
        self.root = root
        self.text = ""
        self.filename = ""

        self.menubar = Menu(root, tearoff=0)
        self.filemenu = Menu(self.menubar, tearoff=0)
        # underline only appears when alt is pressed
        self.filemenu.add_command(label='New', accelerator='Command+n', underline=0, command=self.new)
        self.filemenu.add_command(label='Open', accelerator='Command+o', underline=0, command=self.open)
        self.filemenu.add_command(label='Save', accelerator='Command+s', underline=0, command=self.save)
        self.filemenu.add_command(label='Save As', accelerator='Command-Shift-s', underline=5, command=self.save_as)
        self.filemenu.add_command(label='Quit', accelerator='Command+q', underline=0, command=root.quit)
        self.menubar.add_cascade(label="File", underline=0, menu=self.filemenu)
        root.config(menu=self.menubar)

        root.bind_all("<Command-n>", self.new)
        root.bind_all("<Command-o>", self.open)
        root.bind_all("<Command-s>", self.save)
        root.bind_all("<Command-Shift-s>", self.save_as)
        root.bind_all("<Command-q>", root.quit)

    def new(self, event=None):  # we need an optional event in case new is called by a hot key
        self.text = ""         # update the text stored in RAM
        inputTextField.delete(1.0, END)  # update the window
        self.root.title("")  # Display the filename in window

    def open(self, event=None):
        self.filename = filedialog.askopenfilename(defaultextension='.ibava', filetypes=[('ibava', '.ibava'), ('text', '.txt')])
        with open(self.filename, 'r') as f:
            self.text = f.read()
        # update the window
        
        #need to print somewhere else
        inputTextField.delete(1.0, END)
        inputTextField.insert(END, self.text)
        self.root.title(self.filename)  # Display the filename in window

    def save(self, event=None):
        self.text = inputTextField.get(1.0, END)
        with open(self.filename, 'w+') as f:
            f.write(self.text)
            f.flush()

    def save_as(self, event=None):
        self.text = inputTextField.get(1.0, END)
        self.filename = filedialog.asksaveasfilename(defaultextension='.ibava', filetypes=[('ibava', '.ibava')])
        with open(self.filename, 'w+') as f:
            f.write(self.text)
            f.flush()
        self.root.title(self.filename)  # Display the filename in window

menu = MenuBar(root)

#This method runs when button is clicked
def click_event():
	import run as pseudocode
	#print what you input
	inputText = str(inputTextField.get("1.0",END))
	#run the entire code
	#you might have to reset global line_number.. needs to reset
	output = pseudocode.runCode(inputText)

	#return a string, rather than printing, and put it here

	#print new ouput
	outputTextField.delete("1.0", END)
	outputTextField.insert(END, output)		

# Loops app. Must be at the end like this.
mainloop()

