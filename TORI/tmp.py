import pickle
import tkinter as tk
from isoref import *

class Root(tk.Tk):
    def __init__(self,rads=None):
        super().__init__()

        with open('gamma.pickle', 'rb') as handle:
            self.gamma_db = pickle.load(handle)

        with open('beta.pickle', 'rb') as handle:
            self.beta_db = pickle.load(handle)

        with open('alpha.pickle', 'rb') as handle:
            self.alpha_db = pickle.load(handle)

        with open('alpha.pickle', 'rb') as handle:
            self.alpha_db = pickle.load(handle)

        if not rads:
            self.rads = []
        else:
            self.rads = rads
            
        self.title("Table of Radioactive Isotopes Lookup")
        self.geometry("800x600")

        #--Frames-------------------------------------------
        self.frame = tk.Frame(self)

        #--Text Box Widget----------------------------------
        self.isotope_input = tk.Text(self.frame,height=1,width=8)

        #--Button Widget------------------------------------
        self.search_button = tk.Button(self.frame, text="Search")

        #--Labels-------------------------------------------
        self.isotope_input_label = tk.Label(self.frame,text="Isotope:")
        self.isotope_input_label2 = tk.Label(self.frame,text="(Ex: Cs-137, cs137, cesium-137, cesium137)")
        self.radiation_label = tk.Label(self.frame,text="---Radiations go here---",bg="lightgrey",fg="black")

        #--Binds--------------------------------------------
        self.search_button.bind("<Button-1>",self.search)
        self.isotope_input.bind("<Return>",self.search)

        #--Grid---------------------------------------------
        self.isotope_input_label.grid(row=0,column=0)
        self.isotope_input_label2.grid(row=0,column=2)
        self.isotope_input.grid(row=0,column=1)
        self.radiation_label.grid(row=2,column=0,columnspan=4,sticky='WENS')

        self.search_button.grid(row=1,column=0)

        self.frame.grid()
        self.isotope_input.focus_set()

    def search(self,event=None):
        isotope = self.isotope_input.get(1.0,tk.END).strip('\n')
#THIS WONT WORK, NEED TO ACCOUNT FOR ALL POSSIBLE VARIATIONS
##        name=isotope[:2].lower()
##        tmp = name[0].upper()
##        name = tmp + name[1]
        
        
    
        


if __name__ == "__main__":
    window = Root()
    window.mainloop()
