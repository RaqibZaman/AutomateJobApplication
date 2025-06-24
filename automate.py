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


    
