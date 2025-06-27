'''
# So either I switch to last window opened or focus on current window
# current window:: driver.switch_to.window(driver.current_window_handle)?
# Don't want to accidently switch to other chrome tabs ? 
'''
# module openpyxl (installed) is used by pandas but you don't need to import it
import pandas as pd
import tkinter as tk
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
        self.combo_QTV = pd.concat([self.excel_PI, self.excel_QTV], ignore_index=True)

        self.go_signal = tk.BooleanVar(value=False)
        self.keep_alive = True

        # put window in the center of the screen, QoL
        win_w = 350
        win_h = 500
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

        # row 4 label
        tk.Label(self.main, text="Add Excel Entry").pack()

        # row 4
        self.r4 = tk.Frame(self.main, bd=2, relief=tk.SOLID)
        self.r4.pack(fill=tk.BOTH, expand=True, padx="2", pady="2")

        tk.Label(self.r4, text="Enter Question Text").pack(anchor="w", padx="5", pady="5")
        self.entry_Q = tk.Entry(self.r4, width=30)
        self.entry_Q.pack(anchor="w", padx="5", pady="5")

        tk.Label(self.r4, text="Enter Type").pack(anchor="w", padx="5", pady="5")
        self.type_opt = ["radio", "text", "select-one", "button"]
        self.type_selected = tk.StringVar(value=self.type_opt[0])
        self.type_dropdown = tk.OptionMenu(self.r4, self.type_selected, *self.type_opt)
        self.type_dropdown.pack(anchor="w", padx="5", pady="5")

        tk.Label(self.r4, text="Enter Value").pack()
        self.val_txtbox = tk.Text(self.r4, height=10, width=40)
        self.val_txtbox.pack()

        tk.Button(self.r4, text="Add Excel Entry", bg="gold", fg="black", command=self.add_excel).pack(expand=True, fill=tk.BOTH,padx=5, pady=5)


        # need 3 field to enter information (Question, Type, Value)
        # And submit button.

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
        self.excel_PI = pd.read_excel("excel_files/PI_QTV.xlsx")
        self.combo_QTV = pd.concat([self.excel_PI, self.excel_QTV], ignore_index=True)
        # exceldf.to_excel("updated.xlsx", index=False)

    def add_excel(self):
        print("Add Excel Entry & update")
        question = self.entry_Q.get()
        type = self.type_selected.get()
        value = self.val_txtbox.get("1.0", tk.END).strip()
        new_row = {
            "Question": question,
            "Type": type,
            "Value": value
        }
        self.excel_QTV = pd.concat([self.excel_QTV, pd.DataFrame([new_row])], ignore_index=True)
        self.excel_QTV.to_excel("Q_T_V.xlsx", index=False)
        
        # exceldf.to_excel("updated.xlsx", index=False)

    def view_vis_ele(self):
        self.automate.page_visible_info()
    
    # spagetti nonsense code that actually works
    def run(self):
        while self.keep_alive:
            if self.automate.skip():
                continue
            
            self.main.wait_variable(self.go_signal)    # wait_variable checks variable modified not value
            if self.keep_alive == False:
                print("I'm dying!!! argh...")
                break
            print("continue auto filling forms")

            self.automate.focus_last_win()

            vis_e_lst = self.automate.page_visible_info()    # reads last window in focus, so must follow .switch_to
            vis_len = len(vis_e_lst)    
            for idx, e in enumerate(vis_e_lst):
                try:
                    # combine Personal Info with generic Ques.Ty.Val panda dataframes
                    #combo_QTV = pd.concat([self.excel_PI, self.excel_QTV], ignore_index=True)
                    e_txt = e.text.strip().lower()
                    a_match = self.combo_QTV[self.combo_QTV.iloc[:,0].apply(
                        lambda quest: str(quest).lower() in e_txt
                    )]

                    if not a_match.empty:
                        print("It's a match!")
                        type = str(a_match.iloc[0,1]).strip().lower()
                        value = str(a_match.iloc[0,2]).strip()  # Do not lower, want to preserve casing when inserting into textbox. Do lowering at value check in the handlers

                        for i in range(9):
                            if idx + i >= vis_len:
                                print("out of vis_len range")
                                break
                            
                            ee = vis_e_lst[idx + i] # I matched the label txt, now I am going to the next input element
                            match ee.tag_name:
                                case "input":
                                    if self.automate.input_handling(ee, type, value):
                                        break
                                case "select":
                                    if self.automate.select_handling(ee, type, value):
                                        break
                                case "textarea":
                                    if self.automate.textarea_handling(ee, type, value):
                                        break
                                case "button":
                                    if self.automate.button_handling(ee, type, value):
                                        break
                                case _:
                                    pass
                except Exception:
                    print("need to get a job...")




