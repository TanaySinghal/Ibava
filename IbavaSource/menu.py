__author__ = 'cook'
import Tkinter as tk
import tkFileDialog as filedialog

class Editor:

    def __init__(self, root):
        self.root = root
        self.text = ""
        self.filename = ""

        self.menubar = tk.Menu(root, tearoff=0)
        self.filemenu = tk.Menu(self.menubar, tearoff=0)
        # underline only appears when alt is pressed
        self.filemenu.add_command(label='New', accelerator='Command+n', underline=0, command=self.new)
        self.filemenu.add_command(label='Open', accelerator='Command+o', underline=0, command=self.open)
        self.filemenu.add_command(label='Save', accelerator='Command+s', underline=0, command=self.save)
        self.filemenu.add_command(label='Save As', accelerator='Command-Shift-s', underline=5, command=self.save_as)
        self.filemenu.add_command(label='Quit', accelerator='Command+q', underline=0, command=root.quit)
        self.menubar.add_cascade(label="File", underline=0, menu=self.filemenu)
        root.config(menu=self.menubar)

        self.edit = tk.Text(root, height=40, width=100)

        root.bind_all("<Command-n>", self.new)
        root.bind_all("<Command-o>", self.open)
        root.bind_all("<Command-s>", self.save)
        root.bind_all("<Command-Shift-s>", self.save_as)
        root.bind_all("<Command-q>", root.quit)

    def new(self, event=None):  # we need an optional event in case new is called by a hot key
        self.text = ""         # update the text stored in RAM
        self.edit.delete(1.0, tk.END)  # update the window
        self.root.title("")  # Display the filename in window

    def open(self, event=None):
        self.filename = filedialog.askopenfilename(defaultextension='txt',
                                                   filetypes=[('text files', '.txt'), ('python', '.py')])
        with open(self.filename, 'r') as f:
            self.text = f.read()
        # update the window
        self.edit.delete(1.0, tk.END)
        self.edit.insert(1.0, self.text)
        self.root.title(self.filename)  # Display the filename in window

    def save(self, event=None):
        self.text = self.edit.get(1.0, tk.END)
        with open(self.filename, 'w+') as f:
            f.write(self.text)
            f.flush()

    def save_as(self, event=None):
        self.text = self.edit.get(1.0, tk.END)
        self.filename = filedialog.asksaveasfilename(defaultextension='txt',
                                                                filetypes=[('ibava', '.ibava')])
        with open(self.filename, 'w+') as f:
            f.write(self.text)
            f.flush()
        self.root.title(self.filename)  # Display the filename in window


#root = tk.Tk()

#edit = Editor(root)

#root.mainloop()