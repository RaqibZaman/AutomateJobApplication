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
'''
Dev Notes:
* If I use self., it refers to the current instance of a class. If I use window., it refers to a var called "window" that exists outside of class.
* I should not use window. because it breaks if I have multiple instances of "window", for example.
* .mainloop() starts tkinter event loop, and doesn't return until window is closed. That means I need to put this at the very end of my main script, I suppose...
* window is a class. so if I do window(), I am referring to the class. I actually want to refer to the isntance of the class so you call the class and assign it to a variable: ctrl_w = window()
* I'll change class window to Window for consistency...

# note that browser instance must be opened by Selenium for Selenium to work on it
# new problem: I am not logged in...
# Let's see if I can automate logging in?
# Looks like the simplest way is to open up chrome in debug mode and connect it with selenium

# r before a string means "raw string". So \ is not treated as an escape character
# f before a strng means "formatted string literal"
# You can test if newly opened browser is in debug mode with this url: http://localhost:9222/json
# the webdriver/selenium stuff can only run when chrome debugger window is open. Add check
# In selenium webdriver, use driver.find_elements vs .find_element. The one without the s will crash the runtime if element is not found
# use translate() to convert all upper case text to lower case test for case-insensitive text matching.
# XPath: // means look through all elements, for tag[] the [] is ___ 
# I can check what part of the application I am on by either Page title or URL. I'll go with URL
# check to find "Do you consent"
# I can pattern match the URL- it has a hierarchy where the end of the URL is more specific
# Find all buttons & inputs. Filter by visible. They should have an order of what comes first on the page.
# Before any automation occurs, there should be a debug/info output that tells me about the page I am on
# driver.switch_to.window(driver.window_handles[-1])
    # Force correct tab (for people like me who keeps chrome open while initiaing this script.)
    # -1 refers to the last tab opened i.e. newest tab in chrome
'''

# module openpyxl is used by pandas but you don't need to import it
import subprocess
import pandas as pd
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import tkinter as tk

class Window:
    def __init__(self):
        self.frame = tk.Tk()
        self.go_signal = tk.BooleanVar(value=False)
        self.frame.title("Auto Job Applier")
        self.keep_alive = True
        self.frame.attributes("-topmost", True)

        # put window in the center of the screen, QoL
        win_w = 200
        win_h = 100
        screen_w = self.frame.winfo_screenwidth()
        screen_h = self.frame.winfo_screenheight()
        x = (screen_w // 2) - (win_w // 2)
        y = (screen_h // 2) - (win_h // 2)
        # self.frame.geometry("200x100")
        self.frame.geometry(f"{win_w}x{win_h}+{x}+{y}")


        # Stop Go buttons
        go_btn = tk.Button(self.frame, text="Go", bg="green", fg="white", command=self.go_action)
        go_btn.pack(side=tk.LEFT, expand=True, fill=tk.BOTH, padx=5, pady=10)

        stop_btn = tk.Button(self.frame, text="Stop", bg="red", fg="white", command=self.stop_action)
        stop_btn.pack(side=tk.RIGHT, expand=True, fill=tk.BOTH, padx=5, pady=10)
        #self.frame.mainloop()

    def go_action(self):
        print("GO!")
        self.go_signal.set(True)

    def stop_action(self):
        print("STOP!!!")
        self.go_signal.set(True)
        self.keep_alive = False


### Helper Functions ###

# requests: check if chrome window is in debug mode
def is_chr_debug_act(port=9222):
    try:
        r= requests.get(f"http://localhost:{port}/json/version", timeout=2)
        print("Chrome is in debug mode")
        print("Note: chrome can be running without being visible, needs to be killed in task manager")
        return r.status_code == 200
    except requests.RequestException:
        print("Chrome is NOT in debug mode!!!")
        return False

# _: launch chrome in debug mode
def act_chr_debug():
    chrome_path = r'"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"'
    user_data_dir = r"D:\chrome-dev-profile"
    url = "https://www.indeed.com"
    command = f'{chrome_path} --remote-debugging-port=9222 --user-data-dir="{user_data_dir}" {url}'
    subprocess.Popen(command, shell=True)   # start chrome in debug mode
    # need to test using os instead of subprocess. subprocess keeps closing the window
    print("Chrome Launched in Debug Mode!!!")

# webdriver: Look at the webpage through the eyes of a robot
def page_visible_info(driver):
    print("Tab webdriver is on:", driver.title)
    print("Page URL:", driver.current_url)
    # Find the visible actionable UI elements of webpage
    gui_ele = driver.find_elements(
        By.XPATH,
        "//input | //button//span | //select | //label"
    )
    visible = [e for e in gui_ele if e.is_displayed()]

    # debug info: honestly I need to know about what is on the page, in order to know what to do with it
    for index, e in enumerate(visible):
        tag = e.tag_name
        print(f"\nTag[{index}]: {tag}")

        if tag == "input":
            type = e.get_attribute("type")
            val = e.get_attribute("value")
            name = e.get_attribute("name")
            print(f"Type: {type}, Value: {val}, \nName: {name}")
        
        if tag == "span":
            txt = e.text.strip()
            print(f"Text: {txt}")

        if tag == "label":
            print(f"Label text: {e.text.strip()}")

    return visible

# webdriver: print text, class, and outerHTML of buttons
def wbdr_print(btns):
    for i, b in enumerate(btns):
        text = b.text.strip()
        btn_class = b.get_attribute("class")
        print(f"{i}. text: '{text}' | class: '{btn_class}'")
        #print(f"{i}. {b.get_attribute('outerHTML')}")

# webdriver: click button
def next_click(driver):
    # if target text is in span
    # make case insensitive for find_elements
    # list of key words to click?

    # if tag == "span":
    #     txt = e.text.strip()
    #     print(f"Text: {txt}")

    # I need a list of keywords to check for like Continue or Submit, if its there, then click it

    # spans = driver.find_elements(By.XPATH, "//span[contains(text(),'Continue')]")
    clk_keywords = ["continue", "submit"]
    spans = driver.find_elements(By.XPATH, "//button//span")
    print(f"Found {len(spans)} spans with 'Continue'")
    visible = [s for s in spans if s.is_displayed()]    # go through each item and apply a boolean-return function
    print(f"{len(visible)} are visible")
    for v in visible:
        txt = v.text.strip().lower()
        print(f"span text: {txt}")
        if txt in clk_keywords:
            print("clicked", v.text)
            v.click()
            break

    # check contents of span

    # if visible:
    #     visible[0].click()

# ...
def wb_radio_click(driver):
    # Find radio buttons
    radios = driver.find_elements(By.XPATH, "//input[@type='radio']")
    print(f"Found {len(radios)} radios")
    visible = [x for x in radios if x.is_displayed()]
    print(f"{len(visible)} are visible")
    # Find description associated with radio buttons
    
    # Identify radios by the name/value
    # click the one that is relevant
    if visible:
        visible[0].click()


# import data from excel file. column[A]=Labels column[B]=Values for form input
excel_data = pd.read_excel("excel_files/FormLabels&Inputs.xlsx")    #format req: .xlsx
# show some first rows
#print(excel_data.head())

ctrl_w = Window()

if not is_chr_debug_act():
    act_chr_debug()
    
options = Options()
options.add_experimental_option("debuggerAddress", "localhost:9222")  # align selenium to that chrome window
driver = webdriver.Chrome(options=options)     # launch chrome with selenium attached to it

while ctrl_w.keep_alive:
    
    ctrl_w.frame.wait_variable(ctrl_w.go_signal)
    if ctrl_w.keep_alive == False:
        break
    print("continue auto filling forms")

    driver.switch_to.window(driver.window_handles[-1])  # Focus on lasted tab (debugged)
    vis_elements = page_visible_info(driver)    # get page info on last window in focus, so must follow .switch_to
        
    # look for visible element patterns, and use index to crawl back up and find associations between input and label 
    for index, e in enumerate(vis_elements):
        
        if e.get_attribute("type") == "label":
            # if element is a label, I want to check the conents of label text
            yes_txt = ["Are you a US Citizen","Do you have a Bachelor's Degree", "Do you have the necessary experience"]
            yes_txt = list(map(str.lower, yes_txt)) # lower case yes_txt XD
            label_txt = e.text.strip().lower()
            if any(txt in label_txt for txt in yes_txt):
                print("It's a match!")
                # found a label that I want to say yes to! find associated input val (radio for now)
                chk_idx = index + 2
                if chk_idx < len(vis_elements):
                    
                    # consider checking the tag_name for input, it includes multiple types e.g. radio
                    if vis_elements[chk_idx].get_attribute("type") == "radio":
                        if vis_elements[chk_idx].get_attribute("value") == "yes":
                            vis_elements[chk_idx].click()
            else:
                print("no label match")

    just_clk_part = ["form/review", "form/resume"]
    if any(part in driver.current_url for part in just_clk_part):
        next_click(driver)
    
    # if "form/review" in driver.current_url:
    #     wb_btn_click(driver)

    


ctrl_w.frame.destroy()  # kill gui instead???
ctrl_w.frame.mainloop() # keep gui open after script runs

