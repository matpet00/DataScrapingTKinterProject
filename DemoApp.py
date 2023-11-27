import tkinter

import pandas, heapq

from pathlib import Path
from tkinter import Tk, Canvas, Button, PhotoImage, Frame, ttk
from pandastable import Table, TableModel


from Scraping import Scraper
from DataHandler import DataHandler
from ExcelHandler import ExcelHandler
from Chart import Chart


import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)


class DemoApp:
    def __init__(self):

        self.OUTPUT_PATH = Path(__file__).parent
        self.ASSETS_PATH = self.OUTPUT_PATH / Path("assets/frame0")
        self.window = Tk()
        self.window.geometry("1440x1024")
        self.window.configure(bg="#FFFFFF")



        #create Canvas
        self.canvas = Canvas(
            self.window,
            bg="#FFFFFF",
            height=1024,
            width=1440,
            bd=0,
            highlightthickness=0,
            relief="ridge"
        )
        self.canvas.place(x=0, y=0)




        #highest_stocks_label
        self.highest_stocks_label = ttk.Label(master=self.canvas, text='Highest yield stocks', background='white')
        self.highest_stocks_label.place(x= 700, y = 330)
        self.highest_stocks_label.configure(font = ("Inter Medium", 24))


        #Figma rendered Fetch data button
        self.image_image_1 = PhotoImage(file=self.relative_to_assets("image_1.png"))
        self.image_1 = self.canvas.create_image(720.0, 99.0, image=self.image_image_1)

        self.button_image_1 = PhotoImage(file=self.relative_to_assets("button_1.png"))
        self.scrape_button = Button(
            image=self.button_image_1,
            borderwidth=0,
            highlightthickness=0,
            command= self.scrape_data,
            relief="flat"
        )

        #header background img
        self.scrape_button.place(x=36.0, y=891.0, width=313.0, height=75.0)
        self.image_image_2 = PhotoImage(file=self.relative_to_assets("image_2.png"))
        self.image_2 = self.canvas.create_image(144.0, 97.0, image=self.image_image_2)

        self.canvas.create_text(
            272.0,
            14.0,
            anchor="nw",
            text="This DEMO app is designed to scrap portion of data from targeted website that uses javascript to \n \
            fetch data into the front end. \nScrapped data are modified and casted to correct datatype by Scraper Class. Subsequently cleaned \n \
            data are provided to DataHandler class that takes of additional data flattening and conversion to \n \
            pandas Dataframe. Data are then fetched to the table where aditional filtering options are available.",
            fill="#FFFFFF",
            font=("Inter Medium", 24 * -1)
        )
        self.window.resizable(True, True)


        #Placing tables
        self.place_embedded_table(tablename='maintable', x = 40, y = 350)
        self.place_embedded_table(tablename='back', x = 700, y = 400, rows= 3, cols=3, showstatusbar=False, showtoolbar= False, width=300, height = 80)


        self.window.mainloop()




    def relative_to_assets(self, path: str) -> Path:
        return self.ASSETS_PATH / Path(path)


    def generate_download_button(self, excel_handler_instance):
        if not self.data_frame.empty:
            try:
                download_button = tkinter.Button(master = self.canvas, text='Download Table Data!')
                download_button.place(x=700, y = 900)
                download_button.configure(command=excel_handler_instance.to_excel)
            except ValueError:
                print('No Data in table!')


    def place_embedded_table(self,tablename, x,y, showtoolbar=True, showstatusbar=True, *args, **kwargs):

        self.frame = Frame(self.window)
        self.frame.place(x=x, y=y)
        setattr(self,tablename,Table(self.frame, showtoolbar=showtoolbar, showstatusbar=showstatusbar,*args, **kwargs))
        getattr(self, tablename).show()

    def scrape_data(self):
        scraper = Scraper('https://www.dividend.com/')
        scraper.get_headers()
        scraper.crawl_tables(num_pages=1)
        result = scraper.prepare_final_data()
        scraper.end_session()
        data_handler = DataHandler(result)
        pandas_df = data_handler.convert_to_pandas_df()
        self.data_frame = pandas_df
        self.populate_table(pandas_df=pandas_df, table=self.maintable)
        highest_stocks = self.get_highest_stocks(column='yield')
        self.populate_table(pandas_df = highest_stocks, table = self.back)

        excel_handler = ExcelHandler(self.data_frame)

        self.generate_download_button(excel_handler)
        chart = Chart(highest_stocks)
        chart.matplotcanvas(master = self.canvas)








    def populate_table(self,pandas_df, table):
        table_model = TableModel(dataframe=pandas_df)
        # Update the TableModel of the table and redraw
        table.updateModel(table_model)
        table.redraw()




    def get_highest_stocks(self,*,column, records=3):
        # Get the data from the table
        data = self.maintable.model.df  # Accessing table model dataframe
        data = data.drop_duplicates(subset=['NAME'])


        if data is not None  and column.upper() in data.columns:
            # Use heapq to get the top n rows with the highest yields
            result = heapq.nlargest(records, data.itertuples(), key=lambda row: getattr(row, str(column).upper()))
            # Display the highest yield stocks
            df = pandas.DataFrame(result)
            selected_columns = ['NAME','YIELD','AMOUNT','DECLARED_DATE', 'PAY_DATE']
            print(df[selected_columns])
            return df[selected_columns]





if __name__ == "__main__":
    app = DemoApp()




