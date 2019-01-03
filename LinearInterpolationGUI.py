import tkinter as tk
from tkinter import ttk

class Root(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Linear Interpolation GUI")
        self.geometry("300x400")

        options = {'Lead','Tungsten'}

        self.frame = tk.Frame(self)
        self.frame.grid()

        dropdown = tk.OptionMenu(self.frame,*options)
        dropdown.grid()



    def get_atten_data(self,event=None):
        # initialize lists
        data_array = []
        self.energy = []
        self.attenuation = []

        # open file and extract data
        fin = open('PbMassAttenData.txt')
        for line in fin:
            data_array.append(line)
        fin.close()

        # extract data to lists
        for i in range(len(data_array)):
            e, a = list(map(str, data_array[i].split(",")))
            energy.append(e)
            attenuation.append(a)

if __name__ == "__main__":
    window = Root()
    window.mainloop()