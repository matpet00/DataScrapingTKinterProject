import datetime
import pandas as pd
from tkinter import filedialog, messagebox
import openpyxl



class ExcelHandler:
    def __init__(self, pandas_data_frame):
        self.data = pandas_data_frame


    def to_excel(self):

        file_path = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Excel files", "*.xlsx")])
        if file_path:
            try:
                self.data.to_excel(file_path, index=False, header=True)
            except Exception as Ex:
                print(f'Something went wrong! {Ex}')

            else:
                messagebox.showinfo(title="Save file info", message="File saved!")
        else:
            print('Not saved!')


