from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Make automation class to customize automation depending on website
class Automate:
    def __init__(self):
        # chrome debug config for webdriver
        options = Options()
        options.add_experimental_option("debuggerAddress", "localhost:9222")  # align selenium to that chrome window
        self.driver = webdriver.Chrome(options=options)     # launch chrome with selenium attached to it
        
        self.focus_last_win = lambda: self.driver.switch_to.window(self.driver.window_handles[-1])  # Focus on lasted tab (debugged)
        self.skip_v = False



    def skip(self):
        if self.skip_v:
                # Let webdriver catch up, otherwise driver.current_url uses previous url
                time.sleep(3)   # chrome dev tools > network > ~ indeed page takes about 5-7 secs to load...
        
        just_clk_part = ["form/review", "form/resume", "form/commute-check", "form/post-apply", "questions-module/intervention"]
        if any(part in self.driver.current_url for part in just_clk_part):
            self.skip_clk()
            self.skip_v = True
            return True
        else:
            self.skip_v = False
            print("No URL match")
            return False
    
    # webdriver: Find the visible actionable UI elements of webpage
    def page_visible_info(self):
        print("Tab webdriver is on:", self.driver.title)
        print("Page URL:", self.driver.current_url)
        gui_ele = self.driver.find_elements(
            By.XPATH,
            "//input | //button | //select | //label | //textarea"
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
            
            if tag == "textarea":
                type = e.get_attribute("type")
                val = e.get_attribute("value")
                name = e.get_attribute("name")
                print(f"Type: {type}, Value: {val}, \nName: {name}")

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

    # webdriver: skip irrelevant pages
    def skip_clk(self):
        try:
            # webdriver stale head
            btns = self.driver.find_elements(By.XPATH, "//button")
            visible = [b for b in btns if b.is_displayed()]    # go through each item and apply a boolean-return function
            print(f"{len(visible)} buttons are visible")
            clk_keywords = ["continue", "submit", "return to job search", "apply anyway"]
            for v in visible:
                txt = v.text.strip().lower()
                print(f"button text: {txt}")
                if any(keyword in txt for keyword in clk_keywords):
                    print("clicked", v.text)
                    v.click()
                    break
        except Exception as ex:
            # let program keep running
            print("too fast:", ex) 

    def input_handling(self, ee, type, value):
        if(ee.get_attribute("type") == "radio" == type):
            # indeed has val 1:yes, 0:no
            y_n_map = {"yes": "1", "no": "0", "Doesn't apply":"DOESN_T_APPLY"}  # radio value can be 1, 0, or some other nonsense value
            if (ee.get_attribute("value") == y_n_map.get(value, "") 
                or ee.get_attribute("value").lower() == value.lower()
            ):
                ee.click()
                return True
            else:
                # incase radio value is nonsense, look at its label
                # check parent element, which should be label. Its text should indicate if input is valid
                parent_ee = ee.find_element(By.XPATH, "..") # .. means go up one level
                if parent_ee.text.strip().lower() == value:
                    ee.click()
                    return True
        # text input
        if(ee.get_attribute("type") == "text" == type):
            # clear content before adding value
            ee.click()
            ee.send_keys(Keys.CONTROL + "a")
            ee.send_keys(Keys.DELETE)
            ee.send_keys(value)
            return True
        else:
            return False

    # currently only for handling select-one type
    def select_handling(self, ee, type, value):
        if ee.get_attribute("type") != "select-one":
            print("only handling select-one type")
            return False
        if type != "select-one":
            return False
        
        # Please write a better implementation that looks through the <options> to directly select the right one
        
        try:
            v1 = value.lower()
            Select(ee).select_by_value(value)
            return True
        except Exception:
            try:
                v2 = v1[0].upper() + v1[1:]
                Select(ee).select_by_value(v2)
                return True
            except Exception as ex:
                print("Error in select-one", ex)
                return False

    def textarea_handling(self, ee, type, value):
        if type != "text":
            return False
        ee.click()  # focus?
        ee.send_keys(Keys.CONTROL + "a")
        ee.send_keys(Keys.DELETE)   # clear content before adding value
        ee.send_keys(value)
        return True
    
    def button_handling(self, ee, type, value):
        if type != "button":
            return False
        if ee.text.strip().lower() == value:
            ee.click()
            return True


    
