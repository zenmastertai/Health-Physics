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
        self.geometry("480x370")
        self.resizable(width=False,height=False)
        self.configure(background="Gray")
        self.columnconfigure(0,weight=1)
        self.rowconfigure(0,weight=1)

        #Master Frame
        self.master_frame = tk.Frame(self,bg='Light Blue',bd=3,relief=tk.RIDGE)
        self.master_frame.grid(sticky=tk.NSEW)
##        for i in range(6):
##            self.master_frame.columnconfigure(i,weight=1)

        #Row 0
        
        self.frame_zero = tk.Frame(self.master_frame)
        self.frame_zero.grid(row=0,column=0,sticky=tk.NSEW)
        self.isotope_input_label = tk.Label(self.frame_zero,text="Isotope:")
        self.isotope_input_label2 = tk.Label(self.frame_zero,text="(Ex: Cs-137, cs137,cesium-137, cesium137)")
        self.isotope_input = tk.Text(self.frame_zero,height=1,width=14)

        self.isotope_input_label.grid(row=0,column=0,sticky=tk.NSEW)
        self.isotope_input_label2.grid(row=0,column=2,rowspan=2,sticky=tk.NSEW)
        self.isotope_input.grid(row=0,column=1,sticky=tk.NSEW)

        #Row 1

        self.frame_one = tk.Frame(self.master_frame)
        self.frame_one.grid(row=1,column=0,sticky=tk.NSEW)
        self.search_button = tk.Button(self.frame_one, text="Search",relief=tk.RIDGE)
        self.search_button.grid(row=0,column=0,sticky=tk.NSEW)

        #Row 2

        self.frame_two = tk.Frame(self.master_frame)
        self.frame_two.grid(row=2,column=0,sticky=tk.NSEW)
        self.gamma_label = tk.Label(self.frame_two,text="Gamma-Rays",bg='red',width=20,relief=tk.RIDGE)
        self.beta_label = tk.Label(self.frame_two,text="Beta Particles",bg='lightgrey',width=20,relief=tk.RIDGE)
        self.alpha_label = tk.Label(self.frame_two,text="Alpha Particles",bg='red',width=20,relief=tk.RIDGE)        
        self.gamma_label.grid(row=0,column=0,columnspan=2,sticky=tk.NSEW)
        self.beta_label.grid(row=0,column=2,columnspan=2,sticky=tk.NSEW)
        self.alpha_label.grid(row=0,column=4,columnspan=2,sticky=tk.NSEW)

        #Row 3
        self.frame_three = tk.Frame(self.master_frame)
        self.frame_three.grid(row=3,column=0,sticky=tk.NSEW)
        for i in range (6):
            energy_label = tk.Label(self.frame_three,text="Energy (keV)",width = 10,bd=3,relief=tk.RIDGE)
            I_label = tk.Label(self.frame_three,text="Intensity %",width = 9,bd=3,relief=tk.RIDGE)
            if i%2==0:
                energy_label.grid(row=3,column=i,sticky="E")
                I_label.grid(row=3,column=i+1,sticky="E")
                
        
        #Row 4

        self.frame_four = tk.Frame(self.master_frame)
        self.frame_four.grid(row=4,column=0,sticky=tk.NW)
        
        self.canvas = tk.Canvas(self.frame_four,bg='Yellow',width=450)
        self.canvas.grid(row=0,column=0)
        self.vsbar = tk.Scrollbar(self.frame_four,orient=tk.VERTICAL, command=self.canvas.yview)
        self.vsbar.grid(row=0,column=1,sticky=tk.NS)
        self.canvas.configure(yscrollcommand=self.vsbar.set)

        self.radiations_frame = tk.Frame(self.canvas,bg='Blue',bd=2)

##        for i in range(1, 20):
##            for j in range(1, 20):
##                button = tk.Button(self.radiations_frame, padx=7, pady=7, relief=tk.RIDGE,
##                                   text="[%d, %d]" % (i, j))
##                button.grid(row=i, column=j, sticky='news')

        self.canvas.create_window((0,0), window=self.radiations_frame, anchor=tk.NW)
        self.radiations_frame.update_idletasks()
        self.canvas.configure(scrollregion=self.canvas.bbox(tk.ALL))

##        self.radiations_frame.update_idletasks()
##        bbox = self.canvas.bbox(tk.ALL)
##        w, h = bbox[2]-bbox[1], bbox[3]-bbox[1]
##        dw, dh = int((w/20) * 4), int((h/20) * 4)
##        self.canvas.configure(scrollregion=bbox, width=dw, height=dh)


        #--Binds--------------------------------------------
        self.search_button.bind("<Button-1>",self.search)
        self.isotope_input.bind("<Return>",self.search)
        self.bind_all("<MouseWheel>",self.mouse_scroll)
        

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
        row = 0
        r_num = int(len(self.gamma_db[ref])/2) #determine number of radiations of each type
        if r_num!=0:
            for i in range(r_num):
                new_rad = tk.Label(self.radiations_frame,text=self.gamma_db[ref]['gamma'+str(count)],width=10)
                new_rad_I = tk.Label(self.radiations_frame,text=self.gamma_db[ref]['I'+str(count)],width=9)
                new_rad.grid(row=row,column=0)
                new_rad_I.grid(row=row,column=1)
                self.y_rads.append(new_rad)
                self.y_I.append(new_rad_I)
                row+=1
                count+=1
        elif r_num ==0:
            new_rad = tk.Label(self.radiations_frame,text="",width=10)
            new_rad_I = tk.Label(self.radiations_frame,text="",width=9)
            new_rad.grid(row=0,column=0)
            new_rad_I.grid(row=0,column=1)
            self.y_rads.append(new_rad)
            self.y_I.append(new_rad_I)

        #add radiation energies of beta particles
        count = 1
        row = 0
        r_num = int(len(self.beta_db[ref])/2) #determine number of radiations of each type
        if r_num!=0:
            for i in range(r_num):
                new_rad = tk.Label(self.radiations_frame,text=self.beta_db[ref]['beta'+str(count)],width=10)
                new_rad_I = tk.Label(self.radiations_frame,text=self.beta_db[ref]['I'+str(count)],width=9)
                new_rad.grid(row=row,column=2)
                new_rad_I.grid(row=row,column=3)
                self.b_rads.append(new_rad)
                self.b_I.append(new_rad_I)
                row+=1
                count+=1
        elif r_num == 0:
            new_rad = tk.Label(self.radiations_frame,text="",width=10)
            new_rad_I = tk.Label(self.radiations_frame,text="",width=9)
            new_rad.grid(row=0,column=2)
            new_rad_I.grid(row=0,column=3)
            self.b_rads.append(new_rad)
            self.b_I.append(new_rad_I)            

        #add radiation energies of alpha particles
        count = 1
        row = 0
        r_num = int(len(self.alpha_db[ref])/2) #determine number of radiations of each type
        if r_num != 0:
            for i in range(r_num):
                new_rad = tk.Label(self.radiations_frame,text=self.alpha_db[ref]['alpha'+str(count)],width=10)
                new_rad_I = tk.Label(self.radiations_frame,text=self.alpha_db[ref]['I'+str(count)],width=9)
                new_rad.grid(row=row,column=4)
                new_rad_I.grid(row=row,column=5)
                self.a_rads.append(new_rad)
                self.a_I.append(new_rad_I)
                row+=1
                count+=1
        elif r_num == 0:
            new_rad = tk.Label(self.radiations_frame,text="",width=10)
            new_rad_I = tk.Label(self.radiations_frame,text="",width=9)
            new_rad.grid(row=0,column=4)
            new_rad_I.grid(row=0,column=5)
            self.a_rads.append(new_rad)
            self.a_I.append(new_rad_I)

        self.canvas.create_window((0,0), window=self.radiations_frame, anchor=tk.NW)
        self.radiations_frame.update_idletasks()
        self.canvas.configure(scrollregion=self.canvas.bbox(tk.ALL))

    def mouse_scroll(self, event):
        if event.delta:
            self.tasks_canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        else:
            if event.num == 5:
                move = 1
            else:
                move = -1

            self.tasks_canvas.yview_scroll(move, "units")

if __name__ == "__main__":
    window = Root()
    window.mainloop()
