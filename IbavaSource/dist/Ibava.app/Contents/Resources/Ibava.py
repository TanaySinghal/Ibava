from Tkinter import *
import menu

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

menu = menu.Editor(root)

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


# RUNTIME
mainloop()