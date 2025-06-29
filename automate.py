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
                time.sleep(2)   # chrome dev tools > network > ~ indeed page takes about 5-7 secs to load...
        
        just_clk_part = ["form/review", "form/resume", "form/commute-check", "form/post-apply", "questions-module/intervention", "questions-module/supporting-info"]
        if any(part in self.driver.current_url for part in just_clk_part):
            self.skip_clk()
            self.skip_v = True
            return True
        else:
            self.skip_v = False
            print("No URL match")
            return False
    
    def get_e_depth(self, e):
        depth = self.driver.execute_script("""
                let d=0, ee = arguments[0];
                while (ee.parentElement) {
                d++;
                ee = ee.parentElement;
                }
                return d;
            """, e)
        return depth
    
    # webdriver: Find the visible actionable UI elements of webpage
    def page_visible_info(self):
        gui_ele = self.driver.find_elements(
            By.XPATH,
            "//input | //button | //select | //label | //textarea | //legend"
        )
        visible = [e for e in gui_ele if e.is_displayed()]

        vis_ed = []     # ed sucks... very dysfunctional
        for e in visible:
            vis_ed.append((e, self.get_e_depth(e)))

        # debug info: honestly I need to know about what is on the page, in order to know what to do with it
        for index, ed in enumerate(vis_ed):
            tag = ed[0].tag_name
            type = ed[0].get_attribute("type")
            val = ed[0].get_attribute("value")
            match tag:
                case "input":
                    print(f"\nTag[{index}]: {tag}, Depth: {ed[1]}, Type: {type}, Value: {val}")

                case "textarea":
                    print(f"\nTag[{index}]: {tag}, Depth: {ed[1]}, Type: {type}, Value: {val}")

                case "button":
                    print(f"\nTag[{index}]: {tag}, Depth: {ed[1]}, Type: {type}, Value: {val}")
                    print(f"Text: {ed[0].text.strip()}")

                case "label":
                    print(f"\nTag[{index}]: {tag}, Depth: {ed[1]}, Type: {type}, Value: {val}")
                    print(f"Text: {ed[0].text.strip()}")

                case "select":
                    print(f"\nTag[{index}]: {tag}, Depth: {ed[1]}, Type: {type}, Value: {val}")

                case "legend":
                    print(f"\nTag[{index}]: {tag}, Depth: {ed[1]}, Type: {type}, Value: {val}")

        return visible
    
    class NodeArray:
        def __init__(self, e):
            self.siblings = []
            self.newNode 

        # need a function to decide whether the element is a child or sibling, and base case when siblings[] is empty
        def add_node(self, e):
            new_node = Automate.Node_e(e)
            # if there are no siblings
            if not self.siblings:
                self.siblings.append(new_node)
            # if there are siblings, check if node is child or sibling
            # cases:
            # depth is small number (higher in hierarchy)
            # depth is equal (sibling)
            # depth is larger

            # new_node has a bigger depth, so its a child
            elif self.siblings[-1].depth < new_node.depth:
                self.sibling[-1].add_child(new_node)
            # new_node has equal depth, so it is sibling
            elif self.siblings[-1].depth == new_node.depth:
                self.siblings.append(new_node)
            # new_node has smaller depth, so it is a parent, weird case, I'll just not add it for now?
            elif self.siblings[-1].depth > new_node.depth:
                #self.sibling.append(new_node)
                #print(f"")
                pass
            


        
    
    class Node_e:
        def __init__(self, e):
            self.e = e
            self.depth = self.get_depth(e)
            self.children = []

        def add_child(self, node):
            self.children.append(node)

        def get_depth(self, e):
            depth = self.driver.execute_script("""
                    let d=0, ee = arguments[0];
                    while (ee.parentElement) {
                    d++;
                    ee = ee.parentElement;
                    }
                    return d;
                """, e)
            return depth
        
        


        
    
    # element + depth = ed
    def page_visible_ed(self):
        gui_ele = self.driver.find_elements(
            By.XPATH,
            "//input | //button | //select | //label | //textarea | //legend"
        )
        visible = [e for e in gui_ele if e.is_displayed()]

        vis_ed = []     # ed sucks... very dysfunctional
        for e in visible:
            vis_ed.append((e, self.get_e_depth(e)))

        # I want to start with looking for a label
        # Once label is found, start making the array-tree
        # So essentially those elements before the label are truncated
        # the label with least depth goes into the array. This seems to be the first label found on DOM
        # That means the label element e needs to associate not only depth, but also its children
        labels = []
        for e in visible:
            if e.tag_name != "label" and labels:
                continue

        
        #for e in visible:

        # debug info: honestly I need to know about what is on the page, in order to know what to do with it
        for index, ed in enumerate(vis_ed):
            tag = ed[0].tag_name
            type = ed[0].get_attribute("type")
            val = ed[0].get_attribute("value")
            match tag:
                case "input":
                    print(f"\nTag[{index}]: {tag}, Depth: {ed[1]}, Type: {type}, Value: {val}")

                case "textarea":
                    print(f"\nTag[{index}]: {tag}, Depth: {ed[1]}, Type: {type}, Value: {val}")

                case "button":
                    print(f"\nTag[{index}]: {tag}, Depth: {ed[1]}, Type: {type}, Value: {val}")
                    print(f"Text: {ed[0].text.strip()}")

                case "label":
                    print(f"\nTag[{index}]: {tag}, Depth: {ed[1]}, Type: {type}, Value: {val}")
                    print(f"Text: {ed[0].text.strip()}")

                case "select":
                    print(f"\nTag[{index}]: {tag}, Depth: {ed[1]}, Type: {type}, Value: {val}")

                case "legend":
                    print(f"\nTag[{index}]: {tag}, Depth: {ed[1]}, Type: {type}, Value: {val}")

        return visible
    
    # webdriver: skip irrelevant pages
    def skip_clk(self):
        try:
            # webdriver stale head
            btns = self.driver.find_elements(By.XPATH, "//button")
            visible = [b for b in btns if b.is_displayed()]    # go through each item and apply a boolean-return function
            print(f"{len(visible)} buttons are visible")
            clk_keywords = ["continue", "submit", "return to job search", "apply anyway", "Continue applying"]
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
            if (ee.get_attribute("value") == y_n_map.get(value.lower(), "") 
                or ee.get_attribute("value").lower() == value.lower()
            ):
                ee.click()
                return True
            else:
                # incase radio value is nonsense, look at its label
                # check parent element, which should be label. Its text should indicate if input is valid
                parent_ee = ee.find_element(By.XPATH, "..") # .. means go up one level
                if parent_ee.text.strip().lower() == value.lower():
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
            print("excel type: is not select-one")
            return False
        
        select = Select(ee)
        for opt in select.options:
            if opt.text.strip().lower() == value.lower():
                select.select_by_visible_text(opt.text)
                return True

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
        if ee.text.strip().lower() == value.lower():
            ee.click()
            return True


    
