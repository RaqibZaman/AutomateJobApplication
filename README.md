# AutomateJobApplication
Automate the online job application process because I am tired of being the robot...
# Dev Notes for V0.1
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
# Dev Notes:
* If I use self., it refers to the current instance of a class. If I use window., it refers to a var called "window" that exists outside of class.
* I should not use window. because it breaks if I have multiple instances of "window", for example.
* .mainloop() starts tkinter event loop, and doesn't return until window is closed. That means I need to put this at the very end of my main script, I suppose...
* window is a class. so if I do window(), I am referring to the class. I actually want to refer to the isntance of the class so you call the class and assign it to a variable: ctrl_w = window()
* I'll change class window to Window for consistency...

* note that browser instance must be opened by Selenium for Selenium to work on it
* new problem: I am not logged in...
* Let's see if I can automate logging in?
* Looks like the simplest way is to open up chrome in debug mode and connect it with selenium

* r before a string means "raw string". So \ is not treated as an escape character
* f before a strng means "formatted string literal"
* You can test if newly opened browser is in debug mode with this url: http://localhost:9222/json
* the webdriver/selenium stuff can only run when chrome debugger window is open. Add check
* In selenium webdriver, use driver.find_elements vs .find_element. The one without the s will crash the runtime if element is not found
* use translate() to convert all upper case text to lower case test for case-insensitive text matching.
* XPath: // means look through all elements, for tag[] the [] is ___ 
* I can check what part of the application I am on by either Page title or URL. I'll go with URL
* check to find "Do you consent"
* I can pattern match the URL- it has a hierarchy where the end of the URL is more specific
* Find all buttons & inputs. Filter by visible. They should have an order of what comes first on the page.
* Before any automation occurs, there should be a debug/info output that tells me about the page I am on
* driver.switch_to.window(driver.window_handles[-1])
    * Force correct tab (for people like me who keeps chrome open while initiaing this script.)
    * -1 refers to the last tab opened i.e. newest tab in chrome
* look for visible element patterns, and use index to crawl back up and find associations between input and label 
* I could associate labels with inputs,
* Label is key... I don't want to throw away the label. Let's use tuples
* driver.implicitly_wait(10)      # apparently I just need to call this 1 time per session... ok, let's see. For when quickly going through webpages automatically
* Just want to wait the minimum time so time.sleep(10) isn't exactly the right solution

* How to detect when page is fully loaded? requests or websocket library? So if selenium library doesn't have exactly what I am looking for, I can look at a different library
* Also consider that when you select a radio button, the page dynamically loads in other radio button elements... are they just hidden i.e. not-visible
* put click continue btn by url match, for those pages put ontop of keep alive loop. Break it, reloop, use webdriver wait on finding the next button. Don't execute code for checking page for web elements, need to hange on wait_variable
* Should add error handing for selenium incase of staleness

* You should check the load order of the DOM in terms of first/last. And put the expected condition (EC) as what loads close to last, I suppose.
#wait = WebDriverWait(driver, 30)
#wait.until(EC.)
* map() func executes a function for each item in an iterable/list. so its map(func, iterable), takes 2 params. You don't need to add () to func in the map.
* rem, a =+ 5 is same as a= +5, so positive int. Not what I want.
* I tried WebDriverWait().until() for an expected condition, but it seems like I would have to individually find one for each page, otherwise I get a stale error or the like for webdriver. For the sake of simplicity, I'll use time.sleep() until I want to optimize the app later on.
* pd.read_excel outputs a DataFrame, which is like a 2D array. Think of a list of lists. The outer list is the rows by index, the inner list is the columns by index.
* 
* In case Selenium fails me, remember that it can use jQuery to find the right element e.g.
* driver.execute_script("$('#username').val('FirstNameTxt');")
* 
* I need to make sure that there is a 1 to 1 relationship to interactable web elements and automated action
* I could map the label matches, so I could use that to limit the search range of vis_e_lst
'''
