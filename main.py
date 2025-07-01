'''

* In case Selenium fails me, remember that it can use jQuery to find the right element e.g.
    driver.execute_script("$('#username').val('FirstNameTxt');")
* I need to make sure that there is a 1 to 1 relationship to interactable web elements and automated action
* I could map the label matches, so I could use that to limit the search range of vis_e_lst
* I should wrap the automation as one class, perhaps?
* Basically I want to be able to change control flow depending on the type of page I am on
*
* Next Steps/features:
* [] Need to make run function more modular, have custom optional parameters to handle the shihtml that indeed is.
* [] Should add a default option for handling selectable inputs
* [] handle other types of fields (legends... how relevant? perhaps just handle checkboxes differently?)
* [NEXT] fuzzy string matching
* You should consider having 4 columns instead of 3 in excel: Question, Tag_Name, Type, Value... Not sure if this is a good idea...
* [] Have 2 concurrent code processes running, so that if url changes and it is a skippable page, I don't have to click "Go" to continue the application process 
'''

from automate import Automate
from gui import Window
import requests
import subprocess

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

autobot = Automate()
ctrl_win = Window(autobot)
ctrl_win.run()



ctrl_win.main.destroy()  # kill gui instead???
ctrl_win.main.mainloop() # keep gui open after script runs

