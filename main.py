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
# look for visible element patterns, and use index to crawl back up and find associations between input and label 
# I could associate labels with inputs,
# Label is key... I don't want to throw away the label. Let's use tuples
#driver.implicitly_wait(10)      # apparently I just need to call this 1 time per session... ok, let's see. For when quickly going through webpages automatically
# Just want to wait the minimum time so time.sleep(10) isn't exactly the right solution

# How to detect when page is fully loaded? requests or websocket library? So if selenium library doesn't have exactly what I am looking for, I can look at a different library
# Also consider that when you select a radio button, the page dynamically loads in other radio button elements... are they just hidden i.e. not-visible
# put click continue btn by url match, for those pages put ontop of keep alive loop. Break it, reloop, use webdriver wait on finding the next button. Don't execute code for checking page for web elements, need to hange on wait_variable
# Should add error handing for selenium incase of staleness

# You should check the load order of the DOM in terms of first/last. And put the expected condition (EC) as what loads close to last, I suppose.
#wait = WebDriverWait(driver, 30)
#wait.until(EC.)
# map() func executes a function for each item in an iterable/list. so its map(func, iterable), takes 2 params. You don't need to add () to func in the map.
# rem, a =+ 5 is same as a= +5, so positive int. Not what I want.
# I tried WebDriverWait().until() for an expected condition, but it seems like I would have to individually find one for each page, otherwise I get a stale error or the like for webdriver. For the sake of simplicity, I'll use time.sleep() until I want to optimize the app later on.
'''

# module openpyxl (installed) is used by pandas but you don't need to import it
import logging
import pandas as pd
import requests
import subprocess
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
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
        # exceldf.to_excel("updated.xlsx", index=False)


### Helper Functions ###

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

# webdriver: Look at the webpage through the eyes of a robot
def page_visible_info(driver):
    print("Tab webdriver is on:", driver.title)
    print("Page URL:", driver.current_url)
    # Find the visible actionable UI elements of webpage
    gui_ele = driver.find_elements(
        By.XPATH,
        # "//input | //button//span | //select | //label"
        "//input | //button | //select | //label"
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
        
        # if tag == "span":
        #     txt = e.text.strip()
        #     print(f"Text: {txt}")

        if tag == "button":
            txt = e.text.strip()
            print(f"Text: {txt}")
            type = e.get_attribute("type")
            val = e.get_attribute("value")
            name = e.get_attribute("name")
            print(f"Type: {type}, Value: {val}, \nName: {name}")

        if tag == "label":
            print(f"Label text: {e.text.strip()}")

        if tag == "select":
            type = e.get_attribute("type")
            val = e.get_attribute("value")
            name = e.get_attribute("name")
            print(f"Type: {type}, Value: {val}, \nName: {name}")

    return visible

# input: list of visible elements
# output: a list of tuples, with the label as key and list of associated elements following label as value. Consider that each label in list of visible elements as a delimiter.
# type:: input: [visible_elements] output: [(label, [elements]),...]
def get_label_elist_pairs(vis_elements):
    label_elst_pairs = []
    cur_label = None
    ass_eles = []   # elements associated with label
    for e in vis_elements:
        # this hits with every instance of label. So upon next triggering, it will be a new label
        if e.get_attribute("type") == "label":
            # append with every instance of label except initial one
            if cur_label is not None:
                label_elst_pairs.append((cur_label, ass_eles))
            # start new tuple by label
            cur_label = e
            ass_eles = []
        # if next element is not a label
        else:
            ass_eles.append(e)
    # for the last label, it is not yet added to associated_elements list. Add it
    if cur_label is not None:
        label_elst_pairs.append((cur_label, ass_eles))
    return label_elst_pairs

# webdriver: print text, class, and outerHTML of buttons
def wbdr_print(btns):
    for i, b in enumerate(btns):
        text = b.text.strip()
        btn_class = b.get_attribute("class")
        print(f"{i}. text: '{text}' | class: '{btn_class}'")
        #print(f"{i}. {b.get_attribute('outerHTML')}")

# webdriver: click button
def skip_clk(driver):
    # if target text is in span
    # make case insensitive for find_elements
    # list of key words to click?

    # I need a list of keywords to check for like Continue or Submit, if its there, then click it
    
    btns = driver.find_elements(By.XPATH, "//button")
    visible = [b for b in btns if b.is_displayed()]    # go through each item and apply a boolean-return function
    print(f"{len(visible)} buttons are visible")
    clk_keywords = ["continue", "submit", "return to job search"]
    for v in visible:
        txt = v.text.strip().lower()
        print(f"button text: {txt}")
        if any(keyword in txt for keyword in clk_keywords):
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

### START ###
ctrl_win = Window()

if not is_chrome_debug_mode():
    launch_chrome_debug_mode()
    
options = Options()
options.add_experimental_option("debuggerAddress", "localhost:9222")  # align selenium to that chrome window
driver = webdriver.Chrome(options=options)     # launch chrome with selenium attached to it
skip = False

# control flow
# 1. check if url is automatable
# 2. if automation button (start) is executed, keep automating until return to job search is reached?
# 3. if no valid value to input into input element found, stop automation.

while ctrl_win.keep_alive:
    if ctrl_win.keep_alive == False:
        print("I'm dying!!! argh...")
        break

    if skip:
            # Let webdriver catch up, otherwise driver.current_url uses previous url
            time.sleep(1)   # chrome dev tools > network > ~ indeed page takes about 5-7 secs to load...
    
    just_clk_part = ["form/review", "form/resume", "form/commute-check", "form/post-apply"]
    if any(part in driver.current_url for part in just_clk_part):
        skip_clk(driver)
        skip = True
        continue
    else:
        skip = False
        print("No URL match")
    
    ctrl_win.main.wait_variable(ctrl_win.go_signal)    # wait_variable checks variable modified not value
    print("continue auto filling forms")

    driver.switch_to.window(driver.window_handles[-1])  # Focus on lasted tab (debugged)
    #print(driver.window_handles)

    # A label may follow a label, and then the relevant input. So filtering by label doesn't always work
    vis_e_lst = page_visible_info(driver)    # reads last window in focus, so must follow .switch_to
    vis_len = len(vis_e_lst)    
    for idx, e in enumerate(vis_e_lst):
        # 1. load information into excel_QTV: Question/prompt, type, value
        # 2. check if Questions column of dataframe matches WebElement label text

        e_txt = e.text.strip().lower()
        # element tag_names in page_visible_info(): input, button, label, select
            # I have a current index of vis_e_lst, check if its an input.
            # If not, check next element in vis_e_lst. Up to 2
            # don't go outside of list, range starts at 0. range(2) = 0, 1
        a_match = ctrl_win.excel_QTV[ctrl_win.excel_QTV.iloc[:,0].apply(
            lambda quest: str(quest).lower() in e_txt.lower()
        )]

        if not a_match.empty:
            print("It's a match!")
            # .iloc[row, col]
            type = str(a_match.iloc[0,1]).lower().strip()
            value = str(a_match.iloc[0,2]).strip()  # case-sensitive i.e. "Weekday" for select's option val

            for i in range(3):
                if idx + i > vis_len:
                    print("out of vis_len range")
                    break
                
                ee = vis_e_lst[idx + i] # I matched the label txt, now I am going to the next input element
                # input: radio
                test0 = e_txt
                test1 = ee.tag_name
                test2 = ee.text.strip().lower()
                test3 = ee.get_attribute("type")
                test4 = ee.get_attribute("value")
                test5 = type
                test6 = value
                if (
                    ee.tag_name == "input" and
                    ee.get_attribute("type") == "radio" == type and
                ):
                    # indeed has val 1:yes, 0:no
                    y_n_map = {"yes": 1, "no": 0}
                    if (ee.get_attribute("value") == y_n_map[value]):
                        ee.click()
                        break
                # select: select-one
                if (
                    ee.tag_name == "select" and
                    ee.get_attribute("type") == "select-one" == type
                ):
                    print("test")
                    Select(ee).select_by_value(value)
                    break
                # button: 
                if (
                    ee.tag_name == "button" == type and
                    ee.text.strip() == value
                    #ee.get_attribute("type") == type and
                    #ee.get_attribute("value") == value  # yes/no
                ):
                    ee.click()
                    skip = True     # delay automation to let the page load for skip_clk()
                    break
                print("checked for entering input")
        else:
            pass
            #print("no label match")

ctrl_win.main.destroy()  # kill gui instead???
ctrl_win.main.mainloop() # keep gui open after script runs

