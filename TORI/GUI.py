import pickle
import tkinter as tk
import tkinter.messagebox as msg
from isoref import *

class Root(tk.Tk):
    def __init__(self,rads=None):
        super().__init__()

        #import data for gamma, beta, and alpha radiation
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
        self.isotope_input = tk.Text(self.frame,height=1,width=14)

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

    #function uses to acquire information from user input
    #passes input along to acquire radiation data from db
    def search(self,event=None):
        #pull data from user input
        isotope = self.isotope_input.get(1.0,tk.END).strip('\n')
        test = False
        #Logic to acquire formatting of isotope and separate name from A
        try:
            count = 0
            A = ""
            #check all characters in isotope variable
            for char in isotope:
                try:
                    value = int(char)
                    A += char
                except ValueError:
                    if char != "-":
                        count+=1
            #check if someone entered in a metastable state
            #includes error checking for miss-types
            try:
                if isotope[-1:].lower() == 'm':
                    count-=1
                    A += 'm'
                else:
                    value = int(isotope[-1:])
            except ValueError:
                    msg.askokcancel("Confirm", "Please enter a nuclide")
                    test = True
            #delete user input
            self.isotope_input.delete(1.0,tk.END)
            #if no errors with metastable entry, run
            if not test:
                isotope = isotope[:count]
                isotope = isotope[0].upper() + isotope[1:]
                self.translate_isotope(isotope,A)
        except IndexError:
            #if a blank is entered, show this error message
            msg.askokcancel("Confirm", "Please enter a nuclide")

    def translate_isotope(self,isotope=None,A=None):
        test = False
        try:
            Z = str(nuclides[isotope])
        except KeyError:
            try:
                Z = nuclides_long[isotope]
            except KeyError:
                msg.askokcancel("Error", "Valid Nuclide Not Entered")
                test = True
        if not test:
            if A[-1:] == 'm':
                A = str(int(A.replace('m',''))+300)
                ref = Z + "0" + A
            else:
                if int(A) < 10:
                    A = "00" + A
                elif int(A) >= 10 and int(A) <100:
                    A = "0" + A
                ref = Z + "0" + A
        self.add_radiation(ref,self.gamma_db)

    def add_radiation(self,ref=None,g_db=None):

        count = 1
        row = 3
        g_num = int(len(g_db[ref])/2)
        for i in range(g_num):
            new_rad = tk.Label(self.frame,text=g_db[ref]['gamma'+str(count)])
            new_rad_I = tk.Label(self.frame,text=g_db[ref]['I'+str(count)])
            new_rad.grid(row=row,column=0)
            new_rad_I.grid(row=row,column=1)
            row+=1
            count+=1

        #print(len(g_db[ref]))
                    


            
        #print(isotope,A)
        
        
        

        
        
    
        


if __name__ == "__main__":
    window = Root()
    window.mainloop()
