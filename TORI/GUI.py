import pickle
import tkinter as tk
import tkinter.messagebox as msg
from tkinter.ttk import Notebook
from isoref import *

class Root(tk.Tk):
    def __init__(self):
        super().__init__()

#---------Initializing--------------------------------------

        #import data for gamma, beta, and alpha radiation
        with open('gamma.pickle', 'rb') as handle:
            self.gamma_db = pickle.load(handle)

        with open('beta.pickle', 'rb') as handle:
            self.beta_db = pickle.load(handle)

        with open('alpha.pickle', 'rb') as handle:
            self.alpha_db = pickle.load(handle)

        #this data includes A, Z, name, half-life, and abundance of each isotope attached to each reference
        with open('parents.pickle', 'rb') as handle:
            self.parents1 = pickle.load(handle)

        #this data includes the decay mode and branching ratio attached to each reference
        with open('parents2.pickle', 'rb') as handle:
            self.parents2 = pickle.load(handle)
            
        self.y_rads = [] #gamma
        self.b_rads = [] #beta
        self.a_rads = [] #alpha

        self.y_I = [] #gamma intensity
        self.b_I = [] #beta intensity
        self.a_I = [] #alpha intensity
            
        self.title("Table of Radioactive Isotopes Lookup")
        self.geometry("470x370")
        self.resizable(width=False,height=False)
        self.configure(background="Gray")
        self.columnconfigure(0,weight=1)
        self.rowconfigure(0,weight=1)

#---------Tabs----------------------------------------------

        self.notebook = Notebook(self)
        
        self.tori_tab = tk.Frame(self.notebook)
        self.conversion_tab = tk.Frame(self.notebook)
        self.decay_tab = tk.Frame(self.notebook)
        self.xray_tab = tk.Frame(self.notebook)
        
        self.notebook.add(self.decay_tab,text='Decay')
        self.notebook.add(self.tori_tab,text='TORI')
        self.notebook.add(self.conversion_tab,text='Conversion')
        self.notebook.add(self.xray_tab,text='Xrays')


#-------TORI TAB--------------------------------------------

        #Row 0
        #Create Frame 0
        self.frame_zero = tk.Frame(self.tori_tab,bd=3,relief=tk.RIDGE)
        self.frame_zero.grid(row=0,column=0,sticky=tk.NSEW)
        
        self.isotope_input_label = tk.Label(self.frame_zero,text="Isotope:")
        self.isotope_input_label2 = tk.Label(self.frame_zero,text="(Ex: Cs-137, cs137,cesium-137, cesium137)")
        self.isotope_input = tk.Text(self.frame_zero,height=1,width=20)

        self.isotope_input_label.grid(row=0,column=0,sticky=tk.NSEW)
        self.isotope_input_label2.grid(row=0,column=2,rowspan=2,sticky=tk.NSEW)
        self.isotope_input.grid(row=0,column=1,sticky=tk.NSEW)

        #Row 1
        #Create Frame 1
        self.frame_one = tk.Frame(self.tori_tab)
        self.frame_one.grid(row=1,column=0,sticky=tk.NSEW)
        
        self.search_button = tk.Button(self.frame_one, text="Search")
        self.search_button.grid(row=0,column=0,sticky=tk.NSEW)
        self.print_button = tk.Button(self.frame_one, text="Print Data")
        self.print_button.grid(row=0,column=1,sticky=tk.NSEW)

        #Row 2
        #Create Frame 2
        self.frame_two = tk.Frame(self.tori_tab)
        self.frame_two.grid(row=2,column=0,sticky=tk.NSEW)
        
        self.gamma_label = tk.Label(self.frame_two,text="Gamma-Rays",width=20,relief=tk.RIDGE,padx=2)
        self.beta_label = tk.Label(self.frame_two,text="Beta Particles",width=20,relief=tk.RIDGE,padx=2)
        self.alpha_label = tk.Label(self.frame_two,text="Alpha Particles",width=20,relief=tk.RIDGE,padx=3)
        
        self.gamma_label.grid(row=0,column=0,columnspan=2,sticky=tk.NSEW)
        self.beta_label.grid(row=0,column=2,columnspan=2,sticky=tk.NSEW)
        self.alpha_label.grid(row=0,column=4,columnspan=2,sticky=tk.NSEW)

        #Row 3
        #Create Frame 3
        self.frame_three = tk.Frame(self.tori_tab)
        self.frame_three.grid(row=3,column=0,sticky=tk.NSEW)
        
        for i in range (6):
            energy_label = tk.Label(self.frame_three,text="Energy (keV)",width=10,bd=3,relief=tk.RIDGE)
            I_label = tk.Label(self.frame_three,text="Intensity %",width=9,bd=3,relief=tk.RIDGE)
            if i%2==0:
                energy_label.grid(row=3,column=i,sticky="E")
                I_label.grid(row=3,column=i+1,sticky="E")
        
        #Row 4
        #Create Frame 4
        self.frame_four = tk.Frame(self.tori_tab)
        self.frame_four.grid(row=4,column=0,sticky=tk.NW)
        
        self.canvas = tk.Canvas(self.frame_four,width=439,bd=3,relief=tk.RIDGE) #parent canvas to frame four
        self.canvas.grid(row=0,column=0)
        
        self.vsbar = tk.Scrollbar(self.frame_four,orient=tk.VERTICAL, command=self.canvas.yview) #create scroll bar to frame four
        self.vsbar.grid(row=0,column=1,sticky=tk.NS)
        self.canvas.configure(yscrollcommand=self.vsbar.set) #configure canvas to respond to scrollbar object

        self.radiations_frame = tk.Frame(self.canvas,bd=3,) #Create frame for radiations to be inserted onto
        
        self.canvas.create_window((0,0), window=self.radiations_frame, anchor=tk.NW) #create window with radiations frame
        self.radiations_frame.update_idletasks() #acquire bbox
        self.canvas.configure(scrollregion=self.canvas.bbox(tk.ALL)) #congiure the canvas to scroll

#-------DECAY TAB--------------------------------------------

        #Row 0
        #Create Frame 0
        self.frame_zero = tk.Frame(self.decay_tab,bd=3,relief=tk.RIDGE)
        self.frame_zero.grid(row=0,column=0,sticky=tk.NSEW)
        
        self.decay_isotope_input_label = tk.Label(self.frame_zero,text="Isotope:")
        self.decay_isotope_input_label2 = tk.Label(self.frame_zero,text="(Ex: Cs-137, cs137,cesium-137, cesium137)")
        self.decay_isotope_input = tk.Text(self.frame_zero,height=1,width=20)

        self.decay_isotope_input_label.grid(row=0,column=0,sticky=tk.NSEW)
        self.decay_isotope_input_label2.grid(row=0,column=2,rowspan=2,sticky=tk.NSEW)
        self.decay_isotope_input.grid(row=0,column=1,sticky=tk.NSEW)

        #Row 1
        #Create Frame 1
        self.frame_one = tk.Frame(self.decay_tab)
        self.frame_one.grid(row=1,column=0,sticky=tk.NSEW)
        
        self.decay_search_button = tk.Button(self.frame_one, text="Search")
        self.decay_search_button.grid(row=0,column=0,sticky=tk.NSEW)

#---------Binds---------------------------------------------

        self.bind_all("<MouseWheel>",self.mouse_scroll)

        #TORI TAB
        self.search_button.bind("<Button-1>",lambda foo: self.TORI_search(self,self.isotope_input))
        self.print_button.bind("<Button-1>",self.print_data)
        self.isotope_input.bind("<Return>",lambda foo: self.TORI_search(self,self.isotope_input))


        #Decay TAB
        self.decay_search_button.bind("<Button-1>",lambda foo: self.decay_search(self,self.decay_isotope_input))
        self.decay_isotope_input.bind("<Return>",lambda foo: self.decay_search(self,self.decay_isotope_input))

        self.decay_isotope_input.focus_set()


#---------Notebook------------------------------------------
        
        self.notebook.pack(fill=tk.BOTH,expand=1)
        
#---------Functions-----------------------------------------

    #Function used to translate user input and add radiations to GUI
    #----------------------------------------------------      
    def TORI_search(self,event=None,isotope_input=None):
        isotope,A = self.search(self,isotope_input)
        ref = self.translate_isotope(isotope,A)
        self.add_radiation(ref)

    #Function used to translate user input and search decay chain
    #----------------------------------------------------      
    def decay_search(self,event=None,isotope_input=None):
        
        isotope,parent_A = self.search(self,isotope_input)
        parent_isotope = isotope+'-'+parent_A
        self.dc = {}
        self.dc[parent_isotope]={}

        self.gen_list = [[parent_isotope]]
        self.decay_chain_get(1)
        for line in self.gen_list:
            print(line)

    def decay_chain_get(self,gen_num):
        x = 1
        #cycle through each generation to determine which generation is the current one
        for g in self.gen_list:
            if x == gen_num:
                generation = g
            else:
                x+=1
            
        tmp = []

        #for every isotope in the current generation,
        #calculate each daughter product
        for iso in generation:
            #break down isotope into isotope and A components
            for i in range(len(iso)):
                if iso[i] == '-':
                    isotope = iso[0:i]
                    A = iso.replace(isotope+'-',"")
                    break
            
            ref = self.translate_isotope(isotope,A) #get referenc id for isotope
            
            branch_list = self.decay_mode_get(ref) #get all branching ratios in a list for that isotope

            #if the isotope isn't stable, caclulate daughter
            if len(branch_list)>0:
                for branch in branch_list: #loop through all branching ratios
                    decay_modes = self.decay_mode_split(branch) #split all decay modes up into a list in order for single branch
                    new_i,new_A = self.decay_mode_translate(decay_modes,ref,A) #calculate daughter from parent for each branch
                    new_isotope = new_i+'-'+new_A



                    tmp.append(new_isotope)
        #if the branch ends, stop recursion
        #if the branch keeps going, go deeper
        if len(tmp)>0:
            self.gen_list.append(tmp)
            self.decay_chain_get(x+1)

    def set(key, value):
        keys = key.split('.')
        latest = keys.pop()
        for k in keys:
            self.dc = self.dc.setdefault(k, {})
        self.dc.setdefault(latest, value)
            
            


    
    def decay_mode_get(self,ref=None):
        decay_mode_list=[]
        try:
            for i in range(int(len(self.parents2[ref])/2)):
                decay_mode_list.append(self.parents2[ref]['mode'+str(i+1)])
        except KeyError:
            pass
        return decay_mode_list

    def decay_mode_split(self,branch=None):
        tmp_list = []
        count = 1
        while len(branch) > 0:
            x = branch[:count]
            try:
                if branch[:count+1] == 'EC+':
                    x = branch[:count+3]
                    tmp_list.append(x)
                    branch = branch.replace(x,"")
                    count = 1
                elif x in decay_types:
                    tmp_list.append(x)
                    branch = branch.replace(x,"")
                    count = 1
                else:
                    count+=1
            except IndexError:
                pass
        return tmp_list

    def decay_mode_translate(self,modes=None,ref=None,A=None):

        Z = int(ref.replace(ref[-4:],""))
        A = int(A)

        for mode in modes:
            if mode == 'B-':
                Z = Z + 1
            elif mode == 'B+':
                Z = Z - 1
            elif mode == 'EC':
                Z = Z - 1
            elif mode == 'EC+':
                Z = Z - 1
            elif mode == 'EC+B+':
                Z = Z - 1
            elif mode == 'A' or mode == '2A':
                Z = Z - 2
                A = A - 4
            elif mode == '3A':
                Z = Z - 4
                Z = Z - 8
            elif mode == 'N':
                A = A - 1
            elif mode == '2N':
                A = A - 2
            elif mode == '3N':
                A = A - 3
            elif mode == 'P':
                Z = Z - 1
                A = A - 1
            elif mode == '2P':
                Z = Z - 2
                A = A - 2
            elif mode == 'IT':
                A = A - 300
            elif mode == 'D':
                Z = Z - 1
                A = A - 1
            elif mode == 'T':
                Z = Z - 1
                A = A - 3

        isotope = nuclides_rev[Z]
        return isotope,str(A)
            
    #function used to acquire information from user input
    #passes input along to acquire radiation data from db
    #----------------------------------------------------
    def search(self,event=None,isotope_input=None):
        #pull data from user input
        isotope = isotope_input.get(1.0,tk.END).strip('\n')
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
            isotope_input.delete(1.0,tk.END)
            #if no errors with metastable entry, run
            if not test:
                isotope = isotope[:count]
                isotope = isotope[0].upper() + isotope[1:]
                return isotope, A
                self.isotope_print = isotope+A #add to global variable so that print_data can access for file name
        except IndexError:
            #if a blank is entered, show this error message
            msg.askokcancel("Confirm", "Please enter a nuclide")

    #function used to translate user input to isotope reference number in database
    #passes reference number onto add_radiation() function
    #----------------------------------------------------
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
                msg.askokcancel("Error", "Valid Nuclide Not Entered:" +isotope)
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
            try:
                return ref
            except UnboundLocalError:
                pass

    def translate_reference(self,ref=None):
        isotope = ref.replace(ref[-4:],"")
        tmp = ref[-3:]

        if tmp[:2] == '00':
            A = ref[-1:]
        elif tmp[:1] == '0':
            A = ref[-2:]
        else:
            A = ref[-3:]
        
        return nuclides_rev[int(isotope)],A


    #add radiations to main screen of all 3 types from isotope
    #----------------------------------------------------
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
        try:
            r_num = int(len(self.gamma_db[ref])/2) #determine number of radiations of each type
        except KeyError:
            pass
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
        #if no radiations, add blank spaces to maintain width
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
        try:
            r_num = int(len(self.beta_db[ref])/2) #determine number of radiations of each type
        except KeyError:
            pass
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
        #if no radiations, add blank spaces to maintain width
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
        try:
            r_num = int(len(self.alpha_db[ref])/2) #determine number of radiations of each type
        except KeyError:
            pass
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
        #if no radiations, add blank spaces to maintain width
        elif r_num == 0:
            new_rad = tk.Label(self.radiations_frame,text="",width=10)
            new_rad_I = tk.Label(self.radiations_frame,text="",width=9)
            new_rad.grid(row=0,column=4)
            new_rad_I.grid(row=0,column=5)
            self.a_rads.append(new_rad)
            self.a_I.append(new_rad_I)

        #reconfigure canvas with updated radiations_frame
        self.canvas.create_window((0,0), window=self.radiations_frame, anchor=tk.NW)
        self.radiations_frame.update_idletasks()
        self.canvas.configure(scrollregion=self.canvas.bbox(tk.ALL))

    #Print all data
    #----------------------------------------------------
    def print_data(self,event=None):
        
        #Get data from labels in GUI to temporary lists
        ytmp = []
        btmp = []
        atmp = []
        for i in range(len(self.y_rads)):
            new = []
            new.append(self.y_rads[i].cget("text"))
            new.append(self.y_I[i].cget("text"))
            ytmp.append(new)
        for i in range(len(self.b_rads)):
            new = []
            new.append(self.b_rads[i].cget("text"))
            new.append(self.b_I[i].cget("text"))
            btmp.append(new)
        for i in range(len(self.a_rads)):
            new = []
            new.append(self.a_rads[i].cget("text"))
            new.append(self.a_I[i].cget("text"))
            atmp.append(new)

        #compile all 3 lists into a single two dimensional list
        #6 columns across, i rows down for largest # of radiations present
        outputlist = []
        for i in range(max(len(ytmp),len(btmp),len(atmp))):
            tmp=[]
            try:
                if str(ytmp[i][0]) != "":
                    tmp.append(str(ytmp[i][0]))
                    tmp.append(str(ytmp[i][1]))
            except IndexError:
                pass
            try:
                if str(btmp[i][0]) != "":
                    tmp.append(str(btmp[i][0]))
                    tmp.append(str(btmp[i][1]))
            except IndexError:
                pass
            try:
                if str(atmp[i][0]) != "":
                    tmp.append(str(atmp[i][0]))
                    tmp.append(str(atmp[i][1]))
            except IndexError:
                pass
            outputlist.append(tmp)

        #print data to a text file
        with open(self.isotope_print+'.txt','w') as f:
            f.write('Gamma-Rays'+','+''+','+'Beta-Particles'+','+''+','+'Alpha-Particles'+'\n')
            f.write('Energy(keV)'+','+'Intensity%'+','+'Energy(keV)'+','+'Intensity%'+','+'Energy(keV)'+','+'Intensity%'+'\n')
            for line in outputlist:
                for i in range(len(line)):
                    if i != len(line)-1:
                        f.write(line[i]+",")
                    else:
                        f.write(line[i])
                f.write('\n')
                
    #allow the use of the mouse wheel to scroll
    #----------------------------------------------------
    def mouse_scroll(self, event):
        self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")


 

if __name__ == "__main__":
    window = Root()
    window.mainloop()
