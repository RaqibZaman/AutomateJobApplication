'''
# So either I switch to last window opened or focus on current window
# current window:: driver.switch_to.window(driver.current_window_handle)?
# Don't want to accidently switch to other chrome tabs ?

* Note that tkinter Text objects can pass through newline characters. I'll stick with Entry when possible.
'''
# module openpyxl (installed) is used by pandas but you don't need to import it
import pandas as pd
import tkinter as tk
import traceback
# My files
from automate import Automate

class Window:
    def __init__(self, automate: Automate):
        self.automate = automate    # instantiating a class in another class is called composition. "a Window has an Automate"
        
        self.main = tk.Tk()
        self.main.title("Auto Job Applier")
        self.main.attributes("-topmost", True)
        
        self.excel_QTV = pd.read_excel("Q_T_V.xlsx")    # Col: Question, Type, Value
        self.excel_PI = pd.read_excel("excel_files/PI_QTV.xlsx") # Personal Information: same format as QTV
        combo_QTV = pd.concat([self.excel_PI, self.excel_QTV], ignore_index=True)
        self.sorted_QTV = combo_QTV.sort_values(by="Question", key=lambda q: q.str.len(), ascending=False)    # Sorting improves efficiency and minimizes mis-matches. longer strings are more accurate to match vs. shorter strings



        self.go_signal = tk.BooleanVar(value=False)
        self.keep_alive = True

        # put window in the center of the screen, QoL
        win_w = 350
        win_h = 650
        screen_w = self.main.winfo_screenwidth()
        screen_h = self.main.winfo_screenheight()
        x = (screen_w // 2) - (win_w // 2)
        y = (screen_h // 2) - (win_h // 2)
        self.main.geometry(f"{win_w}x{win_h}+{x}+{y}")

        # row 0
        r0 = tk.Frame(self.main)
        r0.pack(fill=tk.BOTH, expand=True)

        tk.Label(r0, text="Current Tab").pack(anchor="w", padx="5", pady="5")
        self.tab_text = tk.StringVar()
        tk.Entry(r0, width=80, textvariable=self.tab_text, state="readonly").pack(anchor="w", padx="5")
        
        tk.Label(r0, text="Current URL").pack(anchor="w", padx="5", pady="5")
        self.URL_text = tk.StringVar()
        tk.Entry(r0, width=80, textvariable=self.URL_text, state="readonly").pack(anchor="w", padx="5")
        
        # row 1
        self.r1 = tk.Frame(self.main)
        self.r1.pack(fill=tk.BOTH, expand=True)

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

        view_vis_ele_btn = tk.Button(self.r3, text="View Visible Elements", bg="blue", fg="white", command=self.view_vis_tree)
        view_vis_ele_btn.pack(expand=True, fill=tk.BOTH, padx=5, pady=(5,10))

        # row 4 label
        tk.Label(self.main, text="Add Excel Entry").pack()

        # row 4
        self.r4 = tk.Frame(self.main, bd=2, relief=tk.SOLID)
        self.r4.pack(fill=tk.BOTH, expand=True, padx="2", pady="2")

            # e.text
        tk.Label(self.r4, text="Question Text").pack(anchor="w", padx="5", pady="5")
        self.question_txt = ""
        self.Q_txtbox = tk.Text(self.r4, height=2, width=40)
        self.Q_txtbox.pack(anchor="w", padx="5", pady="5")

            # e.tag_name
        tk.Label(self.r4, text="tag_name").pack(anchor="w", padx="5", pady="5")
        self.tagname_txt = tk.StringVar()
        tk.Entry(self.r4, width=40, textvariable=self.tagname_txt, state="readonly").pack(anchor="w", padx="5")

            # e.getattribute("type")
        tk.Label(self.r4, text="type").pack(anchor="w", padx="5", pady="5")
        self.type_txt = tk.StringVar()
        tk.Entry(self.r4, width=40, textvariable=self.type_txt).pack(anchor="w", padx="5")

        tk.Label(self.r4, text="Enter Value").pack()
        self.val_txtbox = tk.Text(self.r4, height=6, width=40)
        self.val_txtbox.pack()

        tk.Button(self.r4, text="Add Excel Entry", bg="gold", fg="black", command=self.add_excel).pack(expand=True, fill=tk.BOTH,padx=5, pady=5)


        # need 3 field to enter information (Question, Type, Value)
        # And submit button.

        # test excel files
        print(self.excel_QTV.head())
        print(self.excel_PI.head())

    def update_tab_url(self):
        self.tab_text.set(self.automate.driver.title)
        self.URL_text.set(self.automate.driver.current_url)

    def set_new_match(self, question, tagname, type):
        # I need Question text, type, maybe tag_name?, and value to enter
        self.Q_txtbox.insert("1.0", question)
        self.question_txt = question
        self.type_txt.set(type)
        self.tagname_txt.set(tagname)
    
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
        self.excel_PI = pd.read_excel("excel_files/PI_QTV.xlsx")
        combo_QTV = pd.concat([self.excel_PI, self.excel_QTV], ignore_index=True)
        self.sorted_QTV = combo_QTV.sort_values(by="Question", key=lambda q: q.str.len(), ascending=False)

    def add_excel(self):
        print("Add Excel Entry & update")
        question = self.Q_txtbox.get("1.0", tk.END).strip()
        #type = self.type_selected.get()
        type = self.type_txt.get().strip()
        value = self.val_txtbox.get("1.0", tk.END).strip()
        new_row = {
            "Question": question,
            "Type": type,
            "Value": value
        }
        # add new entry to df
        self.excel_QTV = pd.concat([self.excel_QTV, pd.DataFrame([new_row])], ignore_index=True)
        # sort like an idiot
        self.excel_QTV = self.excel_QTV.sort_values(by="Question", key=lambda q: q.str.len(), ascending=False)
        # write to specific excel file
        self.excel_QTV.to_excel("Q_T_V.xlsx", index=False)
        # combine QTV and PI
        combo_QTV = pd.concat([self.excel_PI, self.excel_QTV], ignore_index=True)
        # sort again like a double idiot
        self.sorted_QTV = combo_QTV.sort_values(by="Question", key=lambda q: q.str.len(), ascending=False)
        
        # clean up fields
        self.Q_txtbox.delete("1.0", tk.END)
        self.val_txtbox.delete("1.0", tk.END)


    def view_vis_ele(self):
        self.automate.page_visible_info()

    def view_vis_tree(self):
        self.automate.page_visible_tree()

    def e_match(self, e, type, value):
        if value.lower() == "nan":  # handling panda empty cell
            return True
        match e.tag_name:
            case "input":
                if self.automate.input_handling(e, type, value):
                    return True
            case "select":
                if self.automate.select_handling(e, type, value):
                    return True
            case "textarea":
                if self.automate.textarea_handling(e, type, value):
                    return True
            case "button":
                if self.automate.button_handling(e, type, value):
                    return True
            case _:
                return False
    
    # spagetti nonsense code that actually works
    def run(self):
        while self.keep_alive:
            self.update_tab_url()

            if self.automate.skip():
                continue
            
            self.main.wait_variable(self.go_signal)    # wait_variable checks variable modified not value
            if self.keep_alive == False:
                print("I'm dying!!! argh...")
                break
            print("continue auto filling forms")

            self.automate.focus_last_win()

            vis_t_lst = self.automate.page_visible_tree()    # reads last window in focus, so must follow .switch_to
            #vis_len = len(vis_e_lst)    
            # Why don't I take note of the index  for each label element, and do the search from there?
            try:
                for t in vis_t_lst:
                    # The element e has to be a label for the question check- I only put label text in that part of the column
                    e_txt = t.e.text.strip().lower()
                    a_match = self.sorted_QTV[self.sorted_QTV.iloc[:,0].apply(
                        lambda quest: str(quest).lower() in e_txt
                    )]

                    ### PROBLEM HERE ### a_match can be a set of data, right now only checking the first entry
                    if not a_match.empty:    
                        print("It's a match!")
                        type = str(a_match.iloc[0,1]).strip().lower()
                        value = str(a_match.iloc[0,2]).strip()  # Do not lower, want to preserve casing when inserting into textbox. Do lowering at value check in the handlers

                        if t.children:
                            for c in t.children:
                                # I matched the label txt, now I am going to the next input element
                                if self.e_match(c.e, type, value):
                                    break
                        else:
                            self.e_match(t.e, type, value)
                    elif t.children:
                        # if there is no match, it should prompt the user to enter in the missing data
                        # Should automatically pull the Question text, the tag_name, and type
                        c = t.find_IUI_child()
                        self.set_new_match(e_txt, c.tag, c.type)
                        # yay, new problems. Now I need to find the tag_name of the next interactable UI element i.e. not the label
                        break   # maybe retry this part of the loop? or put a pause, add info, send info, and then continue looping?
            except Exception:
                traceback.print_exc()




