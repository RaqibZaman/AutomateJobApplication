'''
Objective: Automate the online job application process
Requirements:
    * store data in excel files. Maybe multiple excel files depending on the type of data-relation:
        label to input
    * Like in relational databases, I should have a separate excel "table" for jobsite name and url
    * pull data from excel files into python. Store as a model. Model for each type of form maybe?
    * auto-fill forms on webpage
    * webpage traversal
'''
'''
ChatGPT Prompts:

Overview: I will fill out a job form and I want to automate the process.
Context: I opened my excel sheet in excel. I will use column "A" and "B". "A" is like the label, and "B" is the value that I will put into the input element of the job form. 
Prompt: Generate for me a list of "A" I can use. Maybe if it is in a format I can put into a text file, save it, and open in excel that might be quicker for me.

Take dummy label data from chatGPT, paste into .txt file, save as .csv file, open and save as excel file

'''
'''
Dev Notes:
If I use self., it refers to the current instance of a class.
If I use window., it refers to a var called "window" that exists outside of class.
I should not use window. because it breaks if I have multiple instances of "window", for example.

'''

# module openpyxl is used by pandas but you don't need to import it
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import tkinter as tk


class window:
    def __init__(self):
        self.frame = tk.Tk()
        self.go_signal = tk.BooleanVar(value=False)
        self.frame.title("Auto Job Applier")
        self.frame.geometry("200x100")

        go_btn = tk.Button(self.frame, text="Go", bg="green", fg="white", command=self.go_action)
        go_btn.pack(side=tk.LEFT, expand=True, fill=tk.BOTH, padx=5, pady=10)

        stop_btn = tk.Button(self.frame, text="Stop", bg="red", fg="white", command=self.stop_action)
        stop_btn.pack(side=tk.RIGHT, expand=True, fill=tk.BOTH, padx=5, pady=10)
        self.frame.mainloop()

    def go_action(self):
            print("GO!")
            self.go_signal.set(True)

    def stop_action(self):
            print("STOP!!!")


# import data from excel file. column[A]=Labels column[B]=Values for form input
excel_data = pd.read_excel("excel_files/FormLabels&Inputs.xlsx")    #format req: .xlsx

# show some first rows
print(excel_data.head())

# note that browser instance must be opened by Selenium for Selenium to work on it
driver = webdriver.Chrome()     # launch chrome with selenium attached to it
driver.get("https://www.indeed.com/")

window()
window.after(100, lambda: print("Waiting for Go bnt click"))
window.wait_varialbe(window.go_signal)

print("auto job applying continued...")

'''
pip install pandas openpyxl
pip install selenium
setup github & git
git init
PowerShell
    New-Item -Path . -Name ".gitignore" -ItemType "File"
git add .
git commit -m "Initial commit I guess"
git remote add origin "SSH link or whatever" ???
git remote set-url origin https://github.com/RaqibZaman/AutomateJobApplication.git
'''