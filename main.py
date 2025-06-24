'''

* In case Selenium fails me, remember that it can use jQuery to find the right element e.g.
    driver.execute_script("$('#username').val('FirstNameTxt');")
* I need to make sure that there is a 1 to 1 relationship to interactable web elements and automated action
* I could map the label matches, so I could use that to limit the search range of vis_e_lst
*
* Next Steps:
* I should wrap the automation as one class, perhaps?
* Basically I want to be able to change control flow depending on the type of page I am on
* 
'''

from automate import Automate

# module openpyxl (installed) is used by pandas but you don't need to import it
import logging
import pandas as pd
import requests
import subprocess
# from selenium import webdriver
# from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.common.by import By
# from selenium.webdriver.common.keys import Keys
# from selenium.webdriver.support.ui import Select, WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# import time
import tkinter as tk

logging.basicConfig(level=logging.ERROR)

class Window:
    def __init__(self):
        self.main = tk.Tk()
        self.go_signal = tk.BooleanVar(value=False)
        self.excel_QTV = pd.read_excel("Q_T_V.xlsx")    # Col: Question, Type, Value
        self.excel_PI = pd.read_excel("excel_files/FormLabels&Inputs.xlsx") # Personal Information: Col:: label, input_value
        self.main.title("Auto Job Applier")
        self.keep_alive = True
        self.main.attributes("-topmost", True)

        # put window in the center of the screen, QoL
        win_w = 300
        win_h = 200
        screen_w = self.main.winfo_screenwidth()
        screen_h = self.main.winfo_screenheight()
        x = (screen_w // 2) - (win_w // 2)
        y = (screen_h // 2) - (win_h // 2)
        self.main.geometry(f"{win_w}x{win_h}+{x}+{y}")

        # row 1
        self.r1 = tk.Frame(self.main)
        self.r1.pack(fill=tk.BOTH, expand=True)

        # Stop Go buttons
        go_btn = tk.Button(self.r1, text="Go", bg="green", fg="white", command=self.go_action)
        go_btn.pack(side=tk.LEFT, expand=True, fill=tk.BOTH, padx=5, pady=(10,5))

        stop_btn = tk.Button(self.r1, text="Stop", bg="red", fg="white", command=self.stop_action)
        stop_btn.pack(side=tk.RIGHT, expand=True, fill=tk.BOTH, padx=5, pady=(10,5))

        # row 2
        self.r2 = tk.Frame(self.main)
        self.r2.pack(fill=tk.BOTH, expand=True)

        update_excel_btn = tk.Button(self.r2, text="Update Excel", bg="orange", fg="white", command=self.update_excel)
        update_excel_btn.pack(expand=True, fill=tk.BOTH, padx=5, pady=(5,10))

        # test excel files
        print(self.excel_QTV.head())
        print(self.excel_PI.head())

    def go_action(self):
        print("GO!")
        self.go_signal.set(True)

    def stop_action(self):
        print("STOP!!!")
        self.go_signal.set(True)
        self.keep_alive = False

    def update_excel(self):
        print("updating excel (assuming you added change to excel file and saved)")
        self.excel_QTV = pd.read_excel("Q_T_V.xlsx")
        print(self.excel_QTV.tail())
        # exceldf.to_excel("updated.xlsx", index=False)


# requests: check if chrome window is in debug mode
def is_chrome_debug_mode(port=9222):
    try:
        r= requests.get(f"http://localhost:{port}/json/version", timeout=2)
        print("Chrome is in debug mode")
        print("Note: chrome can be running without being visible, needs to be killed in task manager")
        return r.status_code == 200
    except requests.RequestException:
        print("Chrome is NOT in debug mode!!!")
        return False

# _: launch chrome in debug mode
def launch_chrome_debug_mode():
    chrome_path = r'"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"'
    user_data_dir = r"D:\chrome-dev-profile"
    url = "https://www.indeed.com"
    command = f'{chrome_path} --remote-debugging-port=9222 --user-data-dir="{user_data_dir}" {url}'
    subprocess.Popen(command, shell=True)   # start chrome in debug mode
    # need to test using os instead of subprocess. subprocess keeps closing the window
    print("Chrome Launched in Debug Mode!!!")


### START ###

if not is_chrome_debug_mode():
    launch_chrome_debug_mode()

ctrl_win = Window()    
autobot = Automate()
autobot.run(ctrl_win)



ctrl_win.main.destroy()  # kill gui instead???
ctrl_win.main.mainloop() # keep gui open after script runs

