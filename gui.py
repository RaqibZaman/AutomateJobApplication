# module openpyxl (installed) is used by pandas but you don't need to import it
import pandas as pd
import tkinter as tk
import time

# My files
from automate import Automate

class Window:
    def __init__(self, automate: Automate):
        self.automate = automate    # instantiating a class in another class is called composition. "a Window has an Automate"
        
        self.main = tk.Tk()
        self.main.title("Auto Job Applier")
        self.main.attributes("-topmost", True)
        
        self.excel_QTV = pd.read_excel("Q_T_V.xlsx")    # Col: Question, Type, Value
        self.excel_PI = pd.read_excel("excel_files/FormLabels&Inputs.xlsx") # Personal Information: Col:: label, input_value
        
        self.go_signal = tk.BooleanVar(value=False)
        self.keep_alive = True

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
        update_excel_btn.pack(expand=True, fill=tk.BOTH, padx=5, pady=(5,5))

        # row 3
        self.r3 = tk.Frame(self.main)
        self.r3.pack(fill=tk.BOTH, expand=True)

        view_vis_ele_btn = tk.Button(self.r3, text="View Visible Elements", bg="blue", fg="white", command=self.view_vis_ele)
        view_vis_ele_btn.pack(expand=True, fill=tk.BOTH, padx=5, pady=(5,10))

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

    def view_vis_ele(self):
        self.automate.page_visible_info()
    
    # spagetti nonsense code that actually works
    def run(self):
        while self.keep_alive:
            if self.keep_alive == False:
                print("I'm dying!!! argh...")
                break

            if self.skip:
                    # Let webdriver catch up, otherwise driver.current_url uses previous url
                    time.sleep(3)   # chrome dev tools > network > ~ indeed page takes about 5-7 secs to load...
            
            just_clk_part = ["form/review", "form/resume", "form/commute-check", "form/post-apply", "questions-module/intervention"]
            if any(part in self.driver.current_url for part in just_clk_part):
                self.skip_clk()
                self.skip = True
                continue
            else:
                self.skip = False
                print("No URL match")
            
            self.main.wait_variable(self.go_signal)    # wait_variable checks variable modified not value
            print("continue auto filling forms")

            self.driver.switch_to.window(self.driver.window_handles[-1])  # Focus on lasted tab (debugged)
            #print(driver.window_handles)

            # A label may follow a label, and then the relevant input. So filtering by label doesn't always work
            vis_e_lst = self.page_visible_info()    # reads last window in focus, so must follow .switch_to
            vis_len = len(vis_e_lst)    
            for idx, e in enumerate(vis_e_lst):
                # 1. load information into excel_QTV: Question/prompt, type, value
                # 2. check if Questions column of dataframe matches WebElement label text

                e_txt = e.text.strip().lower()
                # element tag_names in page_visible_info(): input, button, label, select
                    # I have a current index of vis_e_lst, check if its an input.
                    # If not, check next element in vis_e_lst. Up to 2
                    # don't go outside of list, range starts at 0. range(2) = 0, 1
                a_match = self.excel_QTV[self.excel_QTV.iloc[:,0].apply(
                    lambda quest: str(quest).lower() in e_txt
                )]

                if not a_match.empty:
                    print("It's a match!")
                    type = str(a_match.iloc[0,1]).strip().lower()
                    value = str(a_match.iloc[0,2]).strip().lower()

                    for i in range(9):
                        if idx + i >= vis_len:
                            print("out of vis_len range")
                            break
                        
                        ee = vis_e_lst[idx + i] # I matched the label txt, now I am going to the next input element
                        # input
                        if (ee.tag_name == "input"):
                            # radio input
                            if(ee.get_attribute("type") == "radio" == type):
                                # indeed has val 1:yes, 0:no
                                y_n_map = {"yes": "1", "no": "0", "Doesn't apply":"DOESN_T_APPLY"}  # radio value can be 1, 0, or some other nonsense value
                                if (ee.get_attribute("value") == y_n_map.get(value, "") 
                                    or ee.get_attribute("value").lower() == value.lower()
                                ):
                                    ee.click()
                                    break
                                else:
                                    # incase radio value is nonsense, look at its label
                                    # check parent element, which should be label. Its text should indicate if input is valid
                                    parent_ee = ee.find_element(By.XPATH, "..") # .. means go up one level
                                    if parent_ee.text.strip().lower() == value:
                                        ee.click()
                                        break
                            # text input
                            if(ee.get_attribute("type") == "text" == type):
                                # clear content before adding value
                                ee.click()
                                ee.send_keys(Keys.CONTROL + "a")
                                ee.send_keys(Keys.DELETE)
                                ee.send_keys(value)
                                break
                        # select: select-one
                        if (
                            ee.tag_name == "select" and
                            ee.get_attribute("type") == "select-one" == type
                        ):
                            try:
                                v1 = value.lower()
                                Select(ee).select_by_value(value)
                                break
                            except Exception:
                                try:
                                    v2 = v1[0].upper() + v1[1:]
                                    Select(ee).select_by_value(v2)
                                    break
                                except Exception as ex:
                                    print("Error in select-one", ex)
                        # textarea
                        if (ee.tag_name == "textarea"):
                            # clear content before adding value
                            ee.click()
                            ee.send_keys(Keys.CONTROL + "a")
                            ee.send_keys(Keys.DELETE)
                            ee.send_keys(value)
                            print("this is a textarea")
                            break
                        # button: 
                        if (
                            ee.tag_name == "button" == type and
                            ee.text.strip().lower() == value
                        ):
                            ee.click()
                            self.skip = True     # delay automation to let the page load for skip_clk()
                            break
                        #print("checked for entering input")
                else:
                    pass
                    #print("no label match")    
