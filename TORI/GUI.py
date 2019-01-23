import pickle
import tkinter as tk
import tkinter.messagebox as msg
from tkinter.ttk import Notebook
from isoref import *
import datetime as dt
import math


class Root(tk.Tk):
    def __init__(self):
        super().__init__()

# ---------Initializing--------------------------------------

        # import data for gamma, beta, and alpha radiation
        with open('gamma.pickle', 'rb') as handle:
            self.gamma_db = pickle.load(handle)

        with open('beta.pickle', 'rb') as handle:
            self.beta_db = pickle.load(handle)

        with open('alpha.pickle', 'rb') as handle:
            self.alpha_db = pickle.load(handle)

        # this data includes A, Z, name, half-life, and abundance of each isotope attached to each reference
        with open('parents.pickle', 'rb') as handle:
            self.parents1 = pickle.load(handle)

        # this data includes the decay mode and branching ratio attached to each reference
        with open('parents2.pickle', 'rb') as handle:
            self.parents2 = pickle.load(handle)

        with open('xray.pickle', 'rb') as handle:
            self.xray_db = pickle.load(handle)
            
            
        self.y_rads = []  # gamma
        self.b_rads = []  # beta
        self.a_rads = []  # alpha
        self.x_rads = [] #x-ray

        self.y_I = []  # gamma intensity
        self.b_I = []  # beta intensity
        self.a_I = []  # alpha intensity
        self.x_level = [] #orbital shell

        self.iso = []
        self.hl = []
        self.act = []
            
        self.title("Table of Radioactive Isotopes Lookup")
        self.geometry("470x370")
        self.resizable(width=False, height=False)
        self.configure(background="Gray")
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

# ---------Tabs----------------------------------------------

        self.notebook = Notebook(self)
        
        self.tori_tab = tk.Frame(self.notebook)
        self.conversion_tab = tk.Frame(self.notebook)
        self.decay_tab = tk.Frame(self.notebook)
        self.xray_tab = tk.Frame(self.notebook)
        
        self.notebook.add(self.tori_tab, text='TORI')
        self.notebook.add(self.xray_tab, text='X-rays')
        self.notebook.add(self.decay_tab, text='Decay')
        self.notebook.add(self.conversion_tab, text='Conversion')



# -------TORI TAB--------------------------------------------

        # Row 0
        # Create Frame 0
        self.frame_zero = tk.Frame(self.tori_tab, bd=3, relief=tk.RIDGE)
        self.frame_zero.grid(row=0, column=0, sticky=tk.NSEW)
        
        self.isotope_input_label = tk.Label(self.frame_zero, text="Isotope:")
        self.isotope_input_label2 = tk.Label(self.frame_zero, text="(Ex: Cs-137, cs137,cesium-137, cesium137)")
        self.isotope_input = tk.Text(self.frame_zero, height=1, width=20)

        self.isotope_input_label.grid(row=0, column=0, sticky=tk.NSEW)
        self.isotope_input_label2.grid(row=0, column=2, rowspan=2, sticky=tk.NSEW)
        self.isotope_input.grid(row=0, column=1, sticky=tk.NSEW)

        # Row 1
        # Create Frame 1
        self.frame_one = tk.Frame(self.tori_tab)
        self.frame_one.grid(row=1, column=0, sticky=tk.NSEW)
        
        self.search_button = tk.Button(self.frame_one, text="Search")
        self.search_button.grid(row=0, column=0, sticky=tk.NSEW)
        self.print_button = tk.Button(self.frame_one, text="Print Data")
        self.print_button.grid(row=0, column=1, sticky=tk.NSEW)

        # Row 2
        # Create Frame 2
        self.frame_two = tk.Frame(self.tori_tab)
        self.frame_two.grid(row=2, column=0, sticky=tk.NSEW)
        
        self.gamma_label = tk.Label(self.frame_two, text="Gamma-Rays", width=20, relief=tk.RIDGE, padx=2)
        self.beta_label = tk.Label(self.frame_two, text="Beta Particles", width=20, relief=tk.RIDGE, padx=2)
        self.alpha_label = tk.Label(self.frame_two, text="Alpha Particles", width=20, relief=tk.RIDGE, padx=3)
        
        self.gamma_label.grid(row=0, column=0, columnspan=2, sticky=tk.NSEW)
        self.beta_label.grid(row=0, column=2, columnspan=2, sticky=tk.NSEW)
        self.alpha_label.grid(row=0, column=4, columnspan=2, sticky=tk.NSEW)

        # Row 3
        # Create Frame 3
        self.frame_three = tk.Frame(self.tori_tab)
        self.frame_three.grid(row=3, column=0, sticky=tk.NSEW)
        
        for i in range(6):
            energy_label = tk.Label(self.frame_three, text="Energy (keV)", width=10, bd=3, relief=tk.RIDGE)
            I_label = tk.Label(self.frame_three, text="Intensity %", width=9, bd=3, relief=tk.RIDGE)
            if i % 2 == 0:
                energy_label.grid(row=3,column=i, sticky="E")
                I_label.grid(row=3, column=i+1, sticky="E")
        
        # Row 4
        # Create Frame 4
        self.frame_four = tk.Frame(self.tori_tab)
        self.frame_four.grid(row=4, column=0, sticky=tk.NSEW)
        
        self.canvas = tk.Canvas(self.frame_four, width=439,height=200, bd=3, relief=tk.RIDGE)  # parent canvas to frame four
        self.canvas.grid(row=0, column=0,sticky=tk.NSEW)
        
        self.vsbar = tk.Scrollbar(self.frame_four, orient=tk.VERTICAL, command=self.canvas.yview)  # create scroll bar to frame four
        self.vsbar.grid(row=0, column=1, sticky=tk.NSEW)
        self.canvas.configure(yscrollcommand=self.vsbar.set)  # configure canvas to respond to scrollbar object

        self.radiations_frame = tk.Frame(self.canvas, bd=3, relief=tk.RIDGE)  # Create frame for radiations to be inserted onto
        
        self.canvas.create_window((0, 0), window=self.radiations_frame, anchor=tk.NW)  # create window with radiations frame
        self.radiations_frame.update_idletasks()  # acquire bbox
        self.canvas.configure(scrollregion=self.canvas.bbox(tk.ALL))  # configure the canvas to scroll

# -------CONVERSION TAB--------------------------------------------

        self.start_var = tk.StringVar()
        self.end_var = tk.StringVar()

        # Row 0
        self.frame_zero = tk.Frame(self.conversion_tab, bd=3, relief=tk.RIDGE)
        self.frame_zero.grid(row=0, column=0, sticky=tk.NSEW)

        self.curies_start = tk.Radiobutton(self.frame_zero, text='curies', variable=self.start_var, value='curies',tristatevalue=0)
        self.millicuries_start = tk.Radiobutton(self.frame_zero, text='millicuries', variable=self.start_var, value='millicuries',tristatevalue=0)
        self.microcuries_start = tk.Radiobutton(self.frame_zero, text='microcuries', variable=self.start_var, value='microcuries',tristatevalue=0)
        self.nanocuries_start = tk.Radiobutton(self.frame_zero, text='nanocuries', variable=self.start_var, value='nanocuries',tristatevalue=0)
        self.bq_start = tk.Radiobutton(self.frame_zero, text='Bq', variable=self.start_var, value='bq',tristatevalue=0)
        self.kbq_start = tk.Radiobutton(self.frame_zero, text='KBq', variable=self.start_var, value='kbq',tristatevalue=0)
        self.mbq_start = tk.Radiobutton(self.frame_zero, text='MBq', variable=self.start_var, value='mbq',tristatevalue=0)
        self.gbq_start = tk.Radiobutton(self.frame_zero, text='GBq', variable=self.start_var, value='gbq',tristatevalue=0)
        self.tbq_start = tk.Radiobutton(self.frame_zero, text='TBq', variable=self.start_var, value='tbq',tristatevalue=0)

        self.buffer = tk.Label(self.frame_zero, text="TO", padx=35)

        self.curies_end = tk.Radiobutton(self.frame_zero, text='curies', variable=self.end_var, value='curies',tristatevalue=0)
        self.millicuries_end = tk.Radiobutton(self.frame_zero, text='millicuries', variable=self.end_var, value='millicuries',tristatevalue=0)
        self.microcuries_end = tk.Radiobutton(self.frame_zero, text='microcuries', variable=self.end_var, value='microcuries',tristatevalue=0)
        self.nanocuries_end = tk.Radiobutton(self.frame_zero, text='nanocuries', variable=self.end_var, value='nanocuries',tristatevalue=0)
        self.bq_end = tk.Radiobutton(self.frame_zero, text='Bq', variable=self.end_var, value='bq',tristatevalue=0)
        self.kbq_end = tk.Radiobutton(self.frame_zero, text='KBq', variable=self.end_var, value='kbq',tristatevalue=0)
        self.mbq_end = tk.Radiobutton(self.frame_zero, text='MBq', variable=self.end_var, value='mbq',tristatevalue=0)
        self.gbq_end = tk.Radiobutton(self.frame_zero, text='GBq', variable=self.end_var, value='gbq',tristatevalue=0)
        self.tbq_end = tk.Radiobutton(self.frame_zero, text='TBq', variable=self.end_var, value='tbq',tristatevalue=0)

        self.curies_start.grid(row=0, column=0, sticky=tk.W)
        self.millicuries_start.grid(row=1, column=0, sticky=tk.W)
        self.microcuries_start.grid(row=2, column=0, sticky=tk.W)
        self.nanocuries_start.grid(row=3, column=0, sticky=tk.W)
        self.bq_start.grid(row=4, column=0, sticky=tk.W)
        self.kbq_start.grid(row=5, column=0, sticky=tk.W)
        self.mbq_start.grid(row=6, column=0, sticky=tk.W)
        self.gbq_start.grid(row=7, column=0, sticky=tk.W)
        self.tbq_start.grid(row=8, column=0, sticky=tk.W)

        self.buffer.grid(row=0, column=1, rowspan=9, sticky=tk.W)

        self.curies_end.grid(row=0, column=2, sticky=tk.W)
        self.millicuries_end.grid(row=1, column=2, sticky=tk.W)
        self.microcuries_end.grid(row=2, column=2, sticky=tk.W)
        self.nanocuries_end.grid(row=3, column=2, sticky=tk.W)
        self.bq_end.grid(row=4, column=2, sticky=tk.W)
        self.kbq_end.grid(row=5, column=2, sticky=tk.W)
        self.mbq_end.grid(row=6, column=2, sticky=tk.W)
        self.gbq_end.grid(row=7, column=2, sticky=tk.W)
        self.tbq_end.grid(row=8, column=2, sticky=tk.W)

        # Row 1
        self.frame_one = tk.Frame(self.conversion_tab, bd=3, relief=tk.RIDGE)
        self.frame_one.grid(row=1, column=0, sticky=tk.NSEW)

        self.calc_conv_button = tk.Button(self.frame_one, text="Calculate")

        self.calc_conv_button.grid(row=0, column=0, sticky=tk.NSEW)

        # Row 2
        self.frame_two = tk.Frame(self.conversion_tab, bd=3, relief=tk.RIDGE)
        self.frame_two.grid(row=2, column=0, sticky=tk.NSEW)

        self.start_entry = tk.Text(self.frame_two, height=1, width=20)
        self.start_entry_label = tk.Label(self.frame_two, text="Start Value:")

        self.start_entry_label.grid(row=0, column=0,sticky=tk.NSEW)
        self.start_entry.grid(row=0, column=1, sticky=tk.NSEW)

        # Row 3
        self.frame_three = tk.Frame(self.conversion_tab, bd=3, relief=tk.RIDGE)
        self.frame_three.grid(row=3, column=0, sticky=tk.NSEW)

        self.end_entry_label = tk.Label(self.frame_three, text="End Value:")
        self.end_entry_label.grid(row=0,column=0)

# -------DECAY TAB--------------------------------------------

        # Row 0
        self.frame_zero = tk.Frame(self.decay_tab, bd=3, relief=tk.RIDGE)
        self.frame_zero.grid(row=0, column=0, sticky=tk.NSEW)
        
        self.iso_input_label = tk.Label(self.frame_zero, text="Isotope:")
        self.iso_input_label2 = tk.Label(self.frame_zero, text="(Ex: Cs-137, cs137,cesium-137, cesium137)")
        self.iso_input = tk.Text(self.frame_zero, height=1, width=20)

        self.iso_input_label.grid(row=0, column=0, sticky=tk.NSEW)
        self.iso_input_label2.grid(row=0, column=2, rowspan=2, sticky=tk.NSEW)
        self.iso_input.grid(row=0, column=1, sticky=tk.NSEW)

        option_list = ('cpm','dpm','pCi','nCi','uCi','mCi','Ci',
                       'Bq','kBq','MBq','GBq','TBq')
        self.v = tk.StringVar()
        self.v.set(option_list[0])

        # Row 1
        self.frame_one = tk.Frame(self.decay_tab, bd=3, relief=tk.RIDGE)
        self.frame_one.grid(row=1, column=0, sticky=tk.NSEW)

        self.orig_act = tk.Label(self.frame_one, text="Enter Original Activity:")
        self.orig_act_input = tk.Text(self.frame_one, height=1, width=20)
        self.dropdown = tk.OptionMenu(self.frame_one, self.v, *option_list)
        self.decay_button = tk.Button(self.frame_one, text="Calculate")

        self.orig_act.grid(row=0, column=0)
        self.orig_act_input.grid(row=0, column=1)
        self.dropdown.grid(row=0, column=2)
        self.decay_button.grid(row=0, column=3, sticky=tk.NSEW)

        # Row 2
        self.frame_two = tk.Frame(self.decay_tab, bd=3, relief=tk.RIDGE)
        self.frame_two.grid(row=2, column=0, sticky=tk.NSEW)

        self.start_date_label = tk.Label(self.frame_two, text="Enter Original Date(MM/DD/YYYY):")
        self.start_date_input = tk.Text(self.frame_two, height=1, width=20)

        self.start_date_label.grid(row=0, column=0)
        self.start_date_input.grid(row=0, column=1)

        # Row 3
        self.frame_three = tk.Frame(self.decay_tab, bd=3, relief=tk.RIDGE)
        self.frame_three.grid(row=3, column=0, sticky=tk.NSEW)

        self.end_date_label = tk.Label(self.frame_three, text="Enter End Date (MM/DD/YYYY):")
        self.end_date_input = tk.Text(self.frame_three, height=1, width=20)
        
        self.end_date_label.grid(row=0, column=0)
        self.end_date_input.grid(row=0, column=1)

        # Row 4
        self.frame_four = tk.Frame(self.decay_tab, bd=3, relief=tk.RIDGE)
        self.frame_four.grid(row=4, column=0, sticky=tk.NSEW)

        self.iso_label = tk.Label(self.frame_four, text="Isotope:")
        
        self.iso_label.grid(row=0, column=0)

        # Row 5
        self.frame_five = tk.Frame(self.decay_tab, bd=3, relief=tk.RIDGE)
        self.frame_five.grid(row=5, column=0, sticky=tk.NSEW)

        self.half_life_label = tk.Label(self.frame_five, text="Half-life:")
        
        self.half_life_label.grid(row=0, column=0)

        # Row 6
        self.frame_six = tk.Frame(self.decay_tab, bd=3, relief=tk.RIDGE)
        self.frame_six.grid(row=6, column=0, sticky=tk.NSEW)

        self.end_act_label = tk.Label(self.frame_six, text="Decayed Activity:")
        
        self.end_act_label.grid(row=0, column=0)

# -------X-RAY TAB--------------------------------------------

        # Row 0
        self.frame_zero = tk.Frame(self.xray_tab, bd=3, relief=tk.RIDGE)
        self.frame_zero.grid(row=0, column=0, sticky=tk.NSEW)
        
        self.ele_input_label = tk.Label(self.frame_zero, text="Element:")
        self.ele_input_label2 = tk.Label(self.frame_zero, text="(Ex: Cs, cs, cesium)")
        self.ele_input = tk.Text(self.frame_zero, height=1, width=20)
        self.xray_search_button = tk.Button(self.frame_zero, text='Search')

        self.ele_input_label.grid(row=0, column=0, sticky=tk.NSEW)
        self.ele_input_label2.grid(row=0, column=2, rowspan=2, sticky=tk.NSEW)
        self.ele_input.grid(row=0, column=1, sticky=tk.NSEW)
        self.xray_search_button.grid(row=0, column=3)

        # Row 1
        self.frame_one = tk.Frame(self.xray_tab, bd=3, relief=tk.RIDGE)
        self.frame_one.grid(row=1, column=0, sticky=tk.NSEW)

        self.x_label1 = tk.Label(self.frame_one, text="Energy (keV)", width=15, bd=3, relief=tk.RIDGE)
        self.x_label2 = tk.Label(self.frame_one, text="Orbital Shell", width=15, bd=3, relief=tk.RIDGE)

        self.x_label1.grid(row=0,column=0)
        self.x_label2.grid(row=0,column=1)

        # Row 2        
        self.frame_twox = tk.Frame(self.xray_tab)
        self.frame_twox.grid(row=2, column=0, sticky=tk.NSEW)
        
        self.x_canvas = tk.Canvas(self.frame_twox, width=439, height=200, bd=3, relief=tk.RIDGE)  # parent canvas to frame four
        self.x_canvas.grid(row=0, column=0)
        
        self.x_vsbar = tk.Scrollbar(self.frame_twox, orient=tk.VERTICAL, command=self.x_canvas.yview)  # create scroll bar to frame four
        self.x_vsbar.grid(row=0, column=1, sticky=tk.NS)
        self.x_canvas.configure(yscrollcommand=self.x_vsbar.set)  # configure canvas to respond to scrollbar object

        self.x_frame = tk.Frame(self.x_canvas, bd=3,relief=tk.RIDGE)  # Create frame for radiations to be inserted onto
        
        self.x_canvas.create_window((0, 0), window=self.x_frame, anchor=tk.NW)  # create window with radiations frame
        self.x_frame.update_idletasks()  # acquire bbox
        self.x_canvas.configure(scrollregion=self.x_canvas.bbox(tk.ALL))  # configure the canvas to scroll

        self.testlabel = tk.Label(self.x_frame,text='TEST')
        self.testlabel.grid(row=0,column=0)
#---------Binds---------------------------------------------

        self.bind_all("<MouseWheel>", self.mouse_scroll)

        # TORI TAB
        self.search_button.bind("<Button-1>", lambda foo: self.TORI_search(self,self.isotope_input))
        self.print_button.bind("<Button-1>", self.print_data)
        self.isotope_input.bind("<Return>", lambda foo: self.TORI_search(self,self.isotope_input))

        # CONVERSION TAB
        self.calc_conv_button.bind("<Button-1>", self.calculate_conversion)
        self.start_entry.bind("<Return>", self.calculate_conversion)
        
        # DECAY TAB
        self.decay_button.bind("<Button-1>", self.calculate_decay)
        self.iso_input.bind("<Return>", self.calculate_decay)
        
        # XRAY TAB
        self.xray_search_button.bind("<Button-1>", self.search_xrays)
        self.ele_input.bind("<Return>", self.search_xrays)


# ---------Notebook------------------------------------------
        
        self.notebook.pack(fill=tk.BOTH,expand=1)
        
# ---------Functions-----------------------------------------

    def search_xrays(self, event=None):
        element = (self.ele_input.get(1.0, tk.END).strip('\n')).lower()
        self.ele_input.delete(1.0, tk.END)
        element = element[:1].upper() + element[1:]
        try:
            Z = nuclides[element]
        except KeyError:
            try:
                Z = nuclides_long[element]
            except KeyError:
                msg.askokcancel("Confirm", "Please enter a valid element")

        ref = str(Z) + '0000'

        # clear any existing radiation labels
        for xr in self.x_rads:
            xr.destroy()
        for lvl in self.x_level:
            lvl.destroy()
        self.x_rads = []
        self.x_level = []        

        row = 0
        for i in range(int(len(self.xray_db[ref])/2)):
            new_x = tk.Label(self.x_frame,text=self.xray_db[ref]['xray'+str(i+1)],width=15)
            new_level = tk.Label(self.x_frame,text=self.xray_db[ref]['level'+str(i+1)],width=15)

            new_x.grid(row=row, column=0)
            new_level.grid(row=row, column=1)

            self.x_rads.append(new_x)
            self.x_level.append(new_level)

            row+=1

        # reconfigure canvas with updated radiations_frame
        self.x_canvas.create_window((0, 0), window=self.x_frame, anchor=tk.NW)
        self.x_frame.update_idletasks()
        self.x_canvas.configure(scrollregion=self.x_canvas.bbox(tk.ALL))

    # Function used to calculate decay from start to end date with original activity
    # ----------------------------------------------------   
    def calculate_decay(self, event=None):
        unit_list = ['ns', 'us', 'ms', 's', 'm', 'd', 'y']
        unit_conv_list = [1.16e-14, 1.16e-11, 1.15e-8, 1.16e-5, 6.94e-4, 1, 365]

        # Get activity input
        try:
            act = float(self.orig_act_input.get(1.0, tk.END).strip('\n'))
            test = False
        except ValueError:
            msg.askokcancel("Confirm", "Please enter a valid activity")

        #return time in days
        t = self.get_time(self,self.start_date_input,self.end_date_input)

        #translate isotope input
        isotope,A = self.search(self, self.iso_input)
        ref = self.translate_isotope(isotope, A)


        #delete any isotope values on screen and put new value on screen
        for i in self.iso:
            i.destroy()
        self.iso = []
        iso = tk.Label(self.frame_four,text=isotope+"-"+A)
        iso.grid(row=0, column=1)
        self.iso.append(iso)

        #acquire half-life of isotope input
        halflife = self.parents1[ref]['halflife']

        #delete any halflife values on screen and put new value on screen
        for h in self.hl:
            h.destroy()
        self.hl = []
        half_life_label = tk.Label(self.frame_five,text=halflife)
        half_life_label.grid(row=0, column=1)
        self.hl.append(half_life_label)

        #split up num value and unit value of halflife
        for j in range(len(unit_list)):
            if unit_list[j] in halflife:
                halflife = halflife.replace(unit_list[j],"")
                hl_unit = unit_list[j]
                break

        #convert halflife unit to days and convert to decay constant
        halflife = float(halflife)*unit_conv_list[unit_list.index(hl_unit)]
        decay_constant = 0.693/halflife #d^-1

        #calculate decay factor and new activity after t passed

        try:
            decay_factor = math.exp(-decay_constant*t)
            new_act = decay_factor * act

            #delete any activity values ons creen and put new value on screen
            for a in self.act:
                a.destroy()
            self.act = []
            new_act_label = tk.Label(self.frame_six,text='{:.2e}'.format(new_act))
            new_act_label.grid(row=0, column=1)
            self.act.append(new_act_label)
        except (UnboundLocalError, TypeError):
            pass

    # Function used to calculate time difference between start and end date
    # ----------------------------------------------------    
    def get_time(self, event=None, start=None, end=None):
        #acquire start and end date, take the difference, return time passed
        try:
            start_date = start.get(1.0, tk.END).strip('\n')
            start_date = start_date.split('/')
            t1 = dt.datetime(int(start_date[2]),int(start_date[1]),int(start_date[0]))
        except IndexError:
            msg.askokcancel("Confirm", "Please enter a valid start date")

        try:
            end_date = end.get(1.0, tk.END).strip('\n')
            end_date = end_date.split('/')
            t2 = dt.datetime(int(end_date[2]),int(end_date[1]),int(end_date[0]))
        except IndexError:
            msg.askokcancel("Confirm", "Please enter a valid end date")
        try:
            t = t2-t1
            return t.days
        except UnboundLocalError:
            pass
        
    # Function used to calculate conversion from one unit to other
    # ----------------------------------------------------
    def calculate_conversion(self, event=None):
        units = ['curies', 'millicuries', 'microcuries', 'nanocuries',
                 'bq', 'kbq', 'mbq', 'gbq', 'tbq']
        conv_list = [[1E0, 1E3, 1E6, 1E9, 3.7E10, 3.7E7, 3.7E4, 3.7E1, 3.7E-2],
                     [1E-3, 1E0, 1E3, 1E6, 3.7E7, 3.7E4, 3.7E1, 3.7E-2, 3.7E-5],
                     [1E-6, 1e-3, 1e0, 1e3, 3.7e4, 3.7e1, 3.7e-2, 3.7e-5, 3.7e-8],
                     [1e-9, 1e-6, 1e-3, 1, 3.7e1, 3.7e-2, 3.7e-5, 3.7e-8, 3.7e-11],
                     [2.7e-11, 2.7e-8, 2.7e-5, 2.7e-2, 1, 1e-3, 1e-6, 1e-9, 1e-12],
                     [2.7e-8, 2.7e-5, 2.7e-2, 2.7e1, 1e3, 1, 1e-3, 1e-6, 1e-9],
                     [2.7e-5, 2.7e-2, 2.7e1, 2.7e4, 1e6, 1e3, 1, 1e-3, 1e-6],
                     [2.7e-2, 2.7e1, 2.7e4, 2.7e7, 1e9, 1e6, 1e3, 1, 1e-3],
                     [2.7e1, 2.7e4, 2.7e7, 2.7e10, 1e12, 1e9, 1e6, 1e3, 1],
                     ]

        start_unit = self.start_var.get()
        end_unit = self.end_var.get()

        val = int(self.start_entry.get(1.0, tk.END).strip('\n'))

        unit_num_start = units.index(start_unit)
        unit_num_end = units.index(end_unit)

        conversion = conv_list[unit_num_start][unit_num_end]
        val = val * conversion
        self.new_value = tk.Label(self.frame_three, text='{:.2e}'.format(val), width=10)
        self.new_value.grid(row=0, column=1)

    # Function used to translate user input and add radiations to GUI
    # ----------------------------------------------------
    def TORI_search(self, event=None, isotope_input=None):
        isotope, A = self.search(self, isotope_input)
        ref = self.translate_isotope(isotope, A)
        self.add_radiation(ref)


    # function used to acquire information from user input
    # passes input along to acquire radiation data from db
    # ----------------------------------------------------
    def search(self, event=None, isotope_input=None):
        # pull data from user input
        isotope = isotope_input.get(1.0, tk.END).strip('\n')
        test = False
        # Logic to acquire formatting of isotope and separate name from A
        try:
            count = 0
            A = ""
            # check all characters in isotope variable
            for char in isotope:
                try:
                    value = int(char)
                    A += char
                except ValueError:
                    if char != "-":
                        count+=1
            # check if someone entered in a metastable state
            # includes error checking for miss-types
            try:
                if isotope[-1:].lower() == 'm':
                    count -= 1
                    A += 'm'
                else:
                    value = int(isotope[-1:])
            except ValueError:
                    msg.askokcancel("Confirm", "Please enter a nuclide")
                    test = True
            # delete user input
            isotope_input.delete(1.0, tk.END)
            # if no errors with metastable entry, run
            if not test:
                isotope = isotope[:count]
                isotope = isotope[0].upper() + isotope[1:]
                return isotope, A
                self.isotope_print = isotope+A  # add to global variable so that print_data can access for file name
        except IndexError:
            # if a blank is entered, show this error message
            msg.askokcancel("Confirm", "Please enter a nuclide")

    # function used to translate user input to isotope reference number in database
    # passes reference number onto add_radiation() function
    # ----------------------------------------------------
    def translate_isotope(self, isotope=None, A=None):
        # test variable for error checking
        test = False
        try:
            # look up the Z from nuclides dictionary
            Z = str(nuclides[isotope])
        except KeyError:
            # if the isotope isnt in the first dictionary, try the second
            try:
                Z = nuclides_long[isotope]
            except KeyError:
                # if not in the second, user entered invalid isotope
                msg.askokcancel("Error", "Valid Nuclide Not Entered:" +isotope)
                test = True
        # test to see if a metastable isotope was entered
        if not test:
            # if yes, add 300 to A and format appropriately
            if A[-1:] == 'm':
                A = str(int(A.replace('m', ''))+300)
                ref = Z + "0" + A
            # if no, format appropriate according to # of decimal
            # places in A.
            else:
                if int(A) < 10:
                    A = "00" + A
                elif int(A) >= 10 and int(A) < 100:
                    A = "0" + A
                ref = Z + "0" + A
            try:
                return ref
            except UnboundLocalError:
                pass

    # Function used to translate a reference to isotope and atomic #
    # ----------------------------------------------------   
    def translate_reference(self, ref=None):
        isotope = ref.replace(ref[-4:], "")
        tmp = ref[-3:]

        if tmp[:2] == '00':
            A = ref[-1:]
        elif tmp[:1] == '0':
            A = ref[-2:]
        else:
            A = ref[-3:]
        
        return nuclides_rev[int(isotope)], A


    # add radiations to main screen of all 3 types from isotope
    # ----------------------------------------------------
    def add_radiation(self, ref=None):

        # clear any existing radiation labels
        for rad in self.y_rads:
            rad.destroy()
        for i in self.y_I:
            i.destroy()
        self.y_rads = []
        self.y_I = []

        # clear any existing radiation labels
        for rad in self.b_rads:
            rad.destroy()
        for i in self.b_I:
            i.destroy()
        self.b_rads = []
        self.b_I = []

        # clear any existing radiation labels
        for rad in self.a_rads:
            rad.destroy()
        for i in self.a_I:
            i.destroy()
        self.a_rads = []
        self.a_I = []
        
        # add radiation energies of gamma rays
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
        # if no radiations, add blank spaces to maintain width
        elif r_num ==0:
            new_rad = tk.Label(self.radiations_frame,text="",width=10)
            new_rad_I = tk.Label(self.radiations_frame,text="",width=9)
            new_rad.grid(row=0,column=0)
            new_rad_I.grid(row=0,column=1)
            self.y_rads.append(new_rad)
            self.y_I.append(new_rad_I)

        # add radiation energies of beta particles
        count = 1
        row = 0
        try:
            r_num = int(len(self.beta_db[ref])/2)  # determine number of radiations of each type
        except KeyError:
            pass
        if r_num != 0:
            for i in range(r_num):
                new_rad = tk.Label(self.radiations_frame, text=self.beta_db[ref]['beta'+str(count)], width=10)
                new_rad_I = tk.Label(self.radiations_frame, text=self.beta_db[ref]['I'+str(count)], width=9)
                
                new_rad.grid(row=row, column=2)
                new_rad_I.grid(row=row, column=3)
                
                self.b_rads.append(new_rad)
                self.b_I.append(new_rad_I)
                
                row += 1
                count += 1
        # if no radiations, add blank spaces to maintain width
        elif r_num == 0:
            new_rad = tk.Label(self.radiations_frame, text="", width=10)
            new_rad_I = tk.Label(self.radiations_frame, text="", width=9)
            new_rad.grid(row=0, column=2)
            new_rad_I.grid(row=0, column=3)
            self.b_rads.append(new_rad)
            self.b_I.append(new_rad_I)            

        # add radiation energies of alpha particles
        count = 1
        row = 0
        try:
            r_num = int(len(self.alpha_db[ref])/2)  # determine number of radiations of each type
        except KeyError:
            pass
        if r_num != 0:
            for i in range(r_num):
                new_rad = tk.Label(self.radiations_frame, text=self.alpha_db[ref]['alpha'+str(count)], width=10)
                new_rad_I = tk.Label(self.radiations_frame, text=self.alpha_db[ref]['I'+str(count)], width=9)
                
                new_rad.grid(row=row, column=4)
                new_rad_I.grid(row=row, column=5)
                
                self.a_rads.append(new_rad)
                self.a_I.append(new_rad_I)
                
                row += 1
                count += 1
        # if no radiations, add blank spaces to maintain width
        elif r_num == 0:
            new_rad = tk.Label(self.radiations_frame, text="", width=10)
            new_rad_I = tk.Label(self.radiations_frame, text="", width=9)
            new_rad.grid(row=0, column=4)
            new_rad_I.grid(row=0, column=5)
            self.a_rads.append(new_rad)
            self.a_I.append(new_rad_I)

        # reconfigure canvas with updated radiations_frame
        self.canvas.create_window((0, 0), window=self.radiations_frame, anchor=tk.NW)
        self.radiations_frame.update_idletasks()
        self.canvas.configure(scrollregion=self.canvas.bbox(tk.ALL))

    # Print all data
    # ----------------------------------------------------
    def print_data(self, event=None):
        
        # Get data from labels in GUI to temporary lists
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

        # compile all 3 lists into a single two dimensional list
        # 6 columns across, i rows down for largest # of radiations present
        outputlist = []
        for i in range(max(len(ytmp), len(btmp), len(atmp))):
            tmp = []
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

        # print data to a text file
        try:
            with open(self.isotope_print+'.txt', 'w') as f:
                f.write('Gamma-Rays'+','+''+','+'Beta-Particles'+','+''+','+'Alpha-Particles'+'\n')
                f.write('Energy(keV)'+','+'Intensity%'+','+'Energy(keV)'+','+'Intensity%'+','+'Energy(keV)'+','+'Intensity%'+'\n')
                for line in outputlist:
                    for i in range(len(line)):
                        if i != len(line)-1:
                            f.write(line[i]+",")
                        else:
                            f.write(line[i])
                    f.write('\n')
        except AttributeError:
            pass
                
    # allow the use of the mouse wheel to scroll
    # ----------------------------------------------------
    def mouse_scroll(self, event):
        self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")


 

if __name__ == "__main__":
    window = Root()
    window.mainloop()
