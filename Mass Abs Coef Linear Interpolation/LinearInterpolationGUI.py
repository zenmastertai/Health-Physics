import tkinter as tk
import math
import tkinter.messagebox as msg

class Root(tk.Tk):
    def __init__(self):
        super().__init__()

        #set the title and default geometry of the window
        self.title("Linear Interpolation GUI")

        #create the frame for the widgets
        self.frame = tk.Frame(self)

        #shielding material drop down options/variables
        option_list = ('Lead','Tungsten')
        self.density = {'Lead':11.34,'Tungsten':19.4}
        self.v = tk.StringVar()
        self.v.set(option_list[0])

        #create text box widget
        self.energy_input = tk.Text(self.frame, height=1, width=8)

        #create drop down widget
        self.dropdown = tk.OptionMenu(self.frame,self.v,*option_list)

        #create label
        self.energy_input_label = tk.Label(self.frame, text="Energy (keV):")
        self.attenuation_output_label = tk.Label(self.frame, text="u (cm^-1):")
        self.shielding_mat_label = tk.Label(self.frame, text="Shielding Material:")
        self.HVL_output_label = tk.Label(self.frame, text="HVL (cm):")
        self.TVL_output_label = tk.Label(self.frame, text="TVL (cm):")


        self.outputv = tk.StringVar()
        self.outputv.set('0')
        self.attenuation_output = tk.Label(self.frame, text=self.outputv.get())

        self.outputhvl = tk.StringVar()
        self.outputhvl.set('0')
        self.HVL_output = tk.Label(self.frame, text=self.outputhvl.get())

        self.outputtvl = tk.StringVar()
        self.outputtvl.set('0')
        self.TVL_output = tk.Label(self.frame, text=self.outputtvl.get())

        #create button widgest
        calculate_button = tk.Button(self.frame, text="Calculate")
        calculate_button.bind("<Button-1>", self.calculate)

        #pack labels and widgets into input frame
        
        self.energy_input_label.grid(row=0,column=0, sticky='E')
        self.energy_input.grid(row=0,column=1)
        self.shielding_mat_label.grid(row=1,column=0,sticky='W')
        self.dropdown.grid(row=1,column=1,sticky='EW')
        self.dropdown.configure(width=8) #adjust width of the dropdown
        calculate_button.grid(row=0,column=2,sticky='W')

        
        self.attenuation_output_label.grid(row=2,column=0, sticky='E')
        self.attenuation_output.grid(row=2,column=1)
        self.HVL_output_label.grid(row=3,column=0,sticky='E')
        self.HVL_output.grid(row=3,column=1)
        self.TVL_output_label.grid(row=4,column=0,sticky='E')
        self.TVL_output.grid(row=4,column=1)

        #pack input frame
        self.frame.grid()

        #set focus to text widget
        self.energy_input.focus_set()

    def interpolate(self,event=None):
        #initialize lists
        data_array = []
        energy = []
        attenuation = []

        #open file and extract data
        filename = ""
        if self.v.get() == "Lead":
            filename = "PbMassAttenData.txt"
        elif self.v.get() == "Tungsten":
            filename = "WMassAttenData.txt"
        fin = open(filename)

        for line in fin:
            data_array.append(line)
        fin.close()

        #extract data to lists
        for i in range(len(data_array)):
            e, a = list(map(str, data_array[i].split(",")))
            energy.append(float(e))
            attenuation.append(float(a))

        #interpolate data to acquire attenuation coefficeint for energy input

        
        if self.energy_input.get(1.0,tk.END)=="\n":
            msg.askokcancel("Confirm", "Please enter a number")
        else:
            try:
                energy_input = int(self.energy_input.get(1.0,tk.END))
                for j in range(len(energy)):
                    if energy[j] == energy_input:
                        y3 = attenuation[j]
                    elif energy[j] > energy_input:
                        x3 = energy[j]
                        x2 = energy_input
                        x1 = energy[j-1]
                        y3 = attenuation[j]
                        y1 = attenuation[j-1]
                        e_coef =(((x2-x1)*(y3-y1))/(x3-x1))+y1 #Linear Interpolation
                        break

                return e_coef
            except ValueError:
                msg.askokcancel("Confirm", "Please enter a number")

    def calculate(self,event=None):
        try:
            e_coef = round(self.interpolate()*self.density[self.v.get()],2)
            HVL = round(math.log(1/2)/-e_coef,4)
            TVL = round(math.log(1/10)/-e_coef,4)
            self.attenuation_output['text']=str(e_coef)
            self.HVL_output['text']=str(HVL)
            self.TVL_output['text']=str(TVL)
        except TypeError:
            pass
        
if __name__ == "__main__":
    window = Root()
    window.mainloop()
