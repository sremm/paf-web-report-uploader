
from  Tkinter import *
import Tkinter, Tkconstants, tkFileDialog
import parserUploader

class App:
    def __init__(self, root):
        self.frame = Frame(root, borderwidth = 5)
        self.frame.pack()

        self.folder = StringVar(root)
        self.folder.trace_variable("w", self.callback)

        self.labelframe = LabelFrame(self.frame, text="Data folder")
        self.labelframe.pack(fill="both", expand="yes", padx=5, pady=5)

        self.entry = Entry(self.labelframe, textvariable=self.folder, state="readonly", width=80)
        self.entry.pack(side=LEFT, padx=5, pady=5)
        
        self.setPathButton = Button(self.labelframe, text="Browse...", command=self.setPath)
        self.setPathButton.pack(side=LEFT, padx=5, pady=5)

        self.label = Label(self.frame, text="This folder should contain c3d files and any related files such as videos and metadata.", width=80)
        self.label.pack(padx=5, pady=5)

        self.processButton = Button(self.frame, text="Create report", command=self.processAndUpload)
        self.processButton.pack(side=BOTTOM,padx=5, pady=5)
                 
    def setPath(self):
        directory = tkFileDialog.askdirectory()
        self.folder.set(directory)
        
    def callback(self, name, index, mode):
        if self.folder.get():
            self.processButton.config(state='normal')
        else:
            self.processButton.config(state='disabled')
    
    def processAndUpload(self):
        workingDirectory = str(self.folder.get())
        workingDirectory = workingDirectory.replace('/','\\')
        workingDirectory = workingDirectory + '\\'
        
        processing = parserUploader.ParserUploader(workingDirectory)
        processing.Upload()

if __name__=="__main__":
    root = Tk()
    root.title("Qualisys Gait Report - C3D import")
    app = App(root)
    root.mainloop()
    



