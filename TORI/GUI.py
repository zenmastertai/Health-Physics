import pickle
import tkinter as tk
import tkinter.messagebox as msg
from isoref import *

class Root(tk.Tk):
    def __init__(self):
        super().__init__()

        #import data for gamma, beta, and alpha radiation
        with open('gamma.pickle', 'rb') as handle:
            self.gamma_db = pickle.load(handle)

        with open('beta.pickle', 'rb') as handle:
            self.beta_db = pickle.load(handle)

        with open('alpha.pickle', 'rb') as handle:
            self.alpha_db = pickle.load(handle)

        self.y_rads = [] #gamma
        self.b_rads = [] #beta
        self.a_rads = [] #alpha

        self.y_I = [] #gamma
        self.b_I = [] #beta
        self.a_I = [] #alpha
            
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
        self.isotope_input_label2 = tk.Label(self.frame,text="(Ex: Cs-137, cs137,cesium-137, cesium137)")
        self.gamma_label = tk.Label(self.frame,text="Gamma-Rays",bg='red')
        self.beta_label = tk.Label(self.frame,text="Beta Particles",bg='lightgrey')
        self.alpha_label = tk.Label(self.frame,text="Alpha Particles",bg='red')
        self.radiation_label = tk.Label(self.frame,text="---Radiations go here---",bg="lightgrey",fg="black")
        self.test1 = tk.Label(self.frame,text='4',bg='blue',width = 15)
        self.test2 = tk.Label(self.frame,text='5',bg='red',width=15)

        #--Binds--------------------------------------------
        self.search_button.bind("<Button-1>",self.search)
        self.isotope_input.bind("<Return>",self.search)

        #--Grid---------------------------------------------
        self.isotope_input_label.grid(row=0,column=0)
        self.isotope_input_label2.grid(row=0,column=2,rowspan=2)
        self.isotope_input.grid(row=0,column=1)
        #self.radiation_label.grid(row=1,column=0,columnspan=4,sticky='WENS')
        self.gamma_label.grid(row=3,column=0,columnspan=2,sticky='EWNS')
        self.beta_label.grid(row=3,column=2,columnspan=2,sticky='WENS')
        self.alpha_label.grid(row=3,column=4,columnspan=2,sticky='WENS')
        self.test1.grid(row=0,column=3)
        self.test2.grid(row=0,column=4)

        self.search_button.grid(row=2,column=0)

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
        #test variable for error checking
        test = False
        try:
            #look up the Z from nuclides dictionary
            Z = str(nuclides[isotope])
        except KeyError:
            #if the isotope isnt in the first dictionary, try the second
            try:
                Z = nuclides_long[isotope]
            except KeyError:
                #if not in the second, user entered invalid isotope
                msg.askokcancel("Error", "Valid Nuclide Not Entered")
                test = True
        #test to see if a metastable isotope was entered
        if not test:
            #if yes, add 300 to A and format appropriately
            if A[-1:] == 'm':
                A = str(int(A.replace('m',''))+300)
                ref = Z + "0" + A
            #if no, format appropriate according to # of decimal
            #places in A.
            else:
                if int(A) < 10:
                    A = "00" + A
                elif int(A) >= 10 and int(A) <100:
                    A = "0" + A
                ref = Z + "0" + A
        self.add_radiation(ref)

    def add_radiation(self,ref=None):

        #clear any existing radiation labels
        for rad in self.y_rads:
            rad.destroy()
        for i in self.y_I:
            i.destroy()
        self.y_rads = []
        self.y_I = []

        #clear any existing radiation labels
        for rad in self.b_rads:
            rad.destroy()
        for i in self.b_I:
            i.destroy()
        self.b_rads = []
        self.b_I = []

        #clear any existing radiation labels
        for rad in self.a_rads:
            rad.destroy()
        for i in self.a_I:
            i.destroy()
        self.a_rads = []
        self.a_I = []
        
        #add radiation energies of gamma rays
        count = 1
        row = 4
        r_num = int(len(self.gamma_db[ref])/2) #determine number of radiations of each type
        for i in range(r_num):
            new_rad = tk.Label(self.frame,text=self.gamma_db[ref]['gamma'+str(count)])
            new_rad_I = tk.Label(self.frame,text=self.gamma_db[ref]['I'+str(count)])
            new_rad.grid(row=row,column=0)
            new_rad_I.grid(row=row,column=1)
            self.y_rads.append(new_rad)
            self.y_I.append(new_rad_I)
            row+=1
            count+=1

        #add radiation energies of beta particles
        count = 1
        row = 4
        r_num = int(len(self.beta_db[ref])/2) #determine number of radiations of each type
        for i in range(r_num):
            new_rad = tk.Label(self.frame,text=self.beta_db[ref]['beta'+str(count)])
            new_rad_I = tk.Label(self.frame,text=self.beta_db[ref]['I'+str(count)])
            new_rad.grid(row=row,column=2)
            new_rad_I.grid(row=row,column=3)
            self.b_rads.append(new_rad)
            self.b_I.append(new_rad_I)
            row+=1
            count+=1

        #add radiation energies of alpha particles
        count = 1
        row = 4
        r_num = int(len(self.alpha_db[ref])/2) #determine number of radiations of each type
        for i in range(r_num):
            new_rad = tk.Label(self.frame,text=self.alpha_db[ref]['alpha'+str(count)])
            new_rad_I = tk.Label(self.frame,text=self.alpha_db[ref]['I'+str(count)])
            new_rad.grid(row=row,column=4)
            new_rad_I.grid(row=row,column=5)
            self.a_rads.append(new_rad)
            self.a_I.append(new_rad_I)
            row+=1
            count+=1 


if __name__ == "__main__":
    window = Root()
    window.mainloop()