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

# Make automation class to customize automation depending on website
class Automate:
    def __init__(self):
        self.skip = False
        
        # chrome debug config for webdriver
        options = Options()
        options.add_experimental_option("debuggerAddress", "localhost:9222")  # align selenium to that chrome window
        self.driver = webdriver.Chrome(options=options)     # launch chrome with selenium attached to it

    
    
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

    # spagetti nonsense code that actually works
    def run(self, ctrl_win):
        while ctrl_win.keep_alive:
            if ctrl_win.keep_alive == False:
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
            
            ctrl_win.main.wait_variable(ctrl_win.go_signal)    # wait_variable checks variable modified not value
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
                a_match = ctrl_win.excel_QTV[ctrl_win.excel_QTV.iloc[:,0].apply(
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


    
