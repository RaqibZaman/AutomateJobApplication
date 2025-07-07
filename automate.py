from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.remote.webelement import WebElement
import time
import pyperclip
from datetime import datetime

# Make automation class to customize automation depending on website
class Automate:
    def __init__(self):
        # chrome debug config for webdriver
        options = Options()
        options.add_experimental_option("debuggerAddress", "localhost:9222")  # align selenium to that chrome window
        self.driver = webdriver.Chrome(options=options)     # launch chrome with selenium attached to it
        
        self.focus_last_win = lambda: self.driver.switch_to.window(self.driver.window_handles[-1])  # Focus on lasted tab (debugged)
        self.skip_v = False

        # form fill action flags
        self.flag_cv = False


    def skip(self):
        if self.skip_v:
                # Let webdriver catch up, otherwise driver.current_url uses previous url
                # also if you go to fast it might trigger anti-bot nonsense...
                time.sleep(1)   # chrome dev tools > network > ~ indeed page takes about 5-7 secs to load...
        
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

        vis_ed = []
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
    
    def relevant_visible_elements(self):
        gui_ele = self.driver.find_elements(
            By.XPATH,
            "//input | //button | //select | //label | //textarea | //legend"
        )
        visible = [e for e in gui_ele if e.is_displayed()]

        # split off the preliminary non-label elements, not relevant
        trunc_vis = []
        for idx, e in enumerate(visible):
            # need to also include the first legend or label that appears
            if e.tag_name in ["label", "legend", "fieldset"]:
                trunc_vis = visible[idx:]
                break
            else:
                continue
        return trunc_vis
    
    def page_vis_node_arr(self):
        gui_ele = self.driver.find_elements(
            By.XPATH,
            #"//input | //button | //select | //label | //textarea | //legend"
            #"//input | //button | //select | //label | //textarea | //fieldset"
            "//input | //button | //select | //label | //textarea | //fieldset | //legend"
        )
        visible = [e for e in gui_ele if e.is_displayed()]

        # split off the preliminary non-label elements, not relevant
        trunc_vis = []
        for idx, e in enumerate(visible):
            # need to also include the first legend or label that appears
            if e.tag_name in ["label", "legend", "fieldset"]:
                trunc_vis = visible[idx:]
                break
            else:
                continue
        
        if not trunc_vis:
            trunc_vis = visible
        # Starting with a label element, make a list of elements of small depth, these are higher in the hierarchy.
        # Their children are the elements inside, thus having a lower hierarchy in the DOM
        
        node_array: list[Node_e] = []
        for e in trunc_vis:
            new_node = Node_e(e, self.get_e_depth(e))
            # if there are no siblings
            if not node_array:
                node_array.append(new_node)
            # new_node has a bigger depth, so its a child
            elif node_array[-1].DOM_depth < new_node.DOM_depth:
                # an exception is if it is a fieldset
                #if new_node.tag == "fieldset" or new_node.tag == "legend":
                if new_node.tag == "fieldset":
                    node_array.append(new_node)
                else:
                    node_array[-1].add_child(new_node)
            # new_node has equal depth, so it is sibling
            elif node_array[-1].DOM_depth == new_node.DOM_depth:
                node_array.append(new_node)
            # new_node has smaller depth, so it is a parent, weird case, I'll just add it for now?
            elif node_array[-1].DOM_depth > new_node.DOM_depth:
                node_array.append(new_node)

        # debug info: honestly I need to know about what is on the page, in order to know what to do with it
        for index, t in enumerate(node_array):
            
            if t.e.tag_name in ["label", "legend", "fieldset"]:
                text = t.e.text.replace("\n", "").strip()
                if len(text) > 70:
                    text = text[:70] + "..."
                print(f"{index} [{t.e.tag_name}] D: {t.DOM_depth}, txt: {text}")
            else:
                print(index, end=" ")
                t.to_str()
            # go through children of tree
            for c in t.children:
                if index < 10:
                    print(end="  ")
                else:
                    print(end="   ")
                c.to_str()
            print()

        return node_array
    
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
                    #time.sleep(1)       # Try to avoid bot detection!
                    v.click()
                    break
        except Exception as ex:
            # let program keep running
            print("too fast:", ex) 

    def input_handling(self, ee: WebElement, type, value):
        # Note that radio input values, a lot of the time, are not revelant
        ee_type = ee.get_attribute("type")
        if(ee_type == "radio" == type):
            value = value.lower()
            parent_ee = ee.find_element(By.XPATH, "..") # .. means find the parent element in DOM, which should be label
            parent_txt = parent_ee.text.strip().lower()
            
            if value in parent_ee.text.strip().lower():
                ee.click()
                return True
            elif value[0] == "[" and value[-1] == "]":
                value = value.strip("[]")
                if value == parent_txt:
                    ee.click()
                    return True
                else:
                    return False
        # text input
        elif(ee_type == "text" == type):
            if value == "[current date]":
                value = datetime.today().strftime("%m/%d/%Y")
            # clear content before adding value
            ee.click()
            ee.send_keys(Keys.CONTROL + "a")
            ee.send_keys(Keys.DELETE)
            ee.send_keys(value)
            return True
        elif(ee_type == "checkbox" == type):
            parent_ee = ee.find_element(By.XPATH, "..") # .. means go up one level
            if value.lower() in parent_ee.text.strip().lower():
                if not ee.is_selected():
                    ee.click()
                return True
        else:
            return False

    # currently only for handling select-one type
    def select_handling(self, ee, type, value, df_matches):
        if ee.get_attribute("type") != "select-one":
            print("only handling select-one type")
            return False
        if type != "select-one":
            return False
        select = Select(ee)
        for opt in select.options:
            opt_txt = opt.text.strip().lower()
            if value.lower() in opt_txt:
                select.select_by_visible_text(opt.text)
                return True
        return False


    def textarea_handling(self, ee, type, value):
        if type != "text" and type != "textarea":
            if type != "[cover letter]":      # you can also add the cover letter flag check if you need.
                return False
        if value == "[current date]":
                value = datetime.today().strftime("%m/%d/%Y")
        ee.click()  # focus?
        ee.send_keys(Keys.CONTROL + "a")
        ee.send_keys(Keys.DELETE)   # clear content before adding value
        
        pyperclip.copy(value)
        ee.click()
        ee.send_keys(Keys.CONTROL, 'v')
        
        # not working for long strings????
        #ee.send_keys(value)
        # Opt 2 incase
        # for line in value.split('\n'):
        #     ee.send_keys(line)
        #     ee.send_keys(Keys.SHIFT, Keys.ENTER)

        return True
    
    def button_handling(self, ee, type, value):
        if type != ee.get_attribute("type"):
            return False
        if ee.text.strip().lower() == value.lower():
            ee.click()
            return True
        else:
            return False

    def page_visible_tree(self):
        visible_elements = self.relevant_visible_elements()
        root_node = self.e_tree_builder(visible_elements)
        return root_node

    
    # I was wondering if I wanted to build a tree class, and I remind myself: you build a class when you want to maintain a state tied to an object. I just want to build a tree for now, so perhaps its not needed atm.
    def e_tree_builder(self, e_list: list):
        # first element is parent, return this at the end
        # pointer to current node
        parent_node: Node_e = None
        pointer: Node_e = None
        
        for e in e_list:
            new_node = Node_e(e, self.get_e_depth(e))
            
            # if first node
            if not parent_node:
                parent_node = new_node
                pointer = parent_node
                pointer.update("T", 0, 0)
                pointer.to_str()
            else:
                pointer = compare_nodes(pointer, new_node)
        
        print()
        return parent_node

class Node_e:
    def __init__(self, e: WebElement, d: int):
        self.e = e
        self.tag = e.tag_name
        self.type = e.get_attribute("type")
        self.value = e.get_attribute("value")
        self.text = e.text.strip()
        self.DOM_depth = d

        self.parent: Node_e = None
        self.left_master: Node_e = None
        self.right_slave: Node_e = None
        self.id = ""
        self.tree_depth = 0
        self.right_depth = 0
        self.children = []

    def add_child(self, node):
        self.children.append(node)

    def update(self, id: str, tree_depth: int, right_depth: int):
        self.id = id
        self.tree_depth = tree_depth
        self.right_depth = right_depth
    
    def to_str(self):
        text = self.text.replace("\n", "").strip()
        if len(text) > 60:
            text = text[:60] + "..."
        for i in range(self.right_depth):
            print(end="  ")
        if (self.id == ""):     # print depending on which function used.
            print(f"[{self.tag}] D:{self.DOM_depth}, Ty:{self.type}, Tx: {text}")
        else:
            print(f"[{self.id}:{self.tag}] D:{self.DOM_depth}, Ty:{self.type}, Tx: {text}")

    # Find an Interactive User Interface element
    def find_IUI_child(self):
        for c in self.children:
            if c.tag != "label":
                return c

# limit = 0
def compare_nodes(parent: Node_e, child: Node_e):
    # global limit
    # if limit == 50:
    #     return
    # else:
    #     limit += 1
    # right child is filled with higher depth
    # if another subsequent node is given with higher depth, move pointer to right child and fill
    if (parent.DOM_depth < child.DOM_depth):
        if (parent.right_slave == None):
            # new_node has +1 deeper level, and id=R
            child.update("R", parent.tree_depth+1, parent.right_depth+1)
            parent.right_slave = child
            child.to_str()
            return parent
        else:
            parent = parent.right_slave
            child.update("R", parent.tree_depth+1, parent.right_depth+1)
            return compare_nodes(parent, child)

    # left child is filled with lower or equal depth
    # if another subsequent node is given with lower or equal depth, move pointer to left child and fill
    elif(parent.DOM_depth >= child.DOM_depth):
        if (parent.left_master == None):
            child.update("L", parent.tree_depth+1, parent.right_depth)
            parent.left_master = child
            child.to_str()
            return parent
        else:
            parent = parent.left_master
            child.update("L", parent.tree_depth+1, parent.right_depth)
            return compare_nodes(parent, child)