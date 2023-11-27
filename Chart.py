from matplotlib.figure import  Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk



import matplotlib.pyplot as plt
import numpy as np

class Chart:
    def __init__(self, pandas_df):
        self.data = pandas_df


    def matplotcanvas(self, master):

        figure = Figure(figsize=(7,3), dpi=90)
        a = figure.add_subplot(111)
        bars = a.bar(self.data['NAME'], self.data['YIELD'])
        a.set_xlabel('Stocks')
        a.set_ylabel('Yield')
        a.set_title('Highest Yield Stocks')
        a.tick_params(axis='x', rotation=50)  # Rotate x-axis labels for better visibility if needed


        canvas = FigureCanvasTkAgg(figure, master=master)
        canvas.draw()
        canvas.get_tk_widget().place(x=700, y=550)


