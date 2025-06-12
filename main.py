'''
Objective: Automate the online job application process
Requirements:
    * store data in excel files. Maybe multiple excel files depending on the type of data-relation:
        label to input
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
# pip install pandas openpyxl
# module openpyxl is used by pandas but you don't need to import it
import pandas as pd

excel_data = pd.read_excel("excel_files/FormLabels&Inputs.xlsx")    #format req: .xlsx

# show some first rows
print(excel_data.head())
