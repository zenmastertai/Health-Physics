import tkinter as tk
import math

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
        self.attenuation_output_label = tk.Label(self.frame, text="u/p (cm^2/g):")
        self.shielding_mat_label = tk.Label(self.frame, text="Shielding Material:")
        
        self.outputv = tk.StringVar()
        self.outputv.set('0')
        self.attenuation_output = tk.Label(self.frame, text=self.outputv.get())

        #create button widgest
        calculate_button = tk.Button(self.frame, text="Calculate")
        calculate_button.bind("<Button-1>", self.calculate)

        #pack labels and widgets into input frame
        
        self.energy_input_label.grid(row=0,column=0, sticky='E')
        self.energy_input.grid(row=0,column=1)
        self.shielding_mat_label.grid(row=1,column=0,sticky='W')
        self.dropdown.grid(row=1,column=1,sticky='EW')
        self.dropdown.configure(width=8) #adjust width of the dropdown
        calculate_button.grid(row=2,column=0,sticky='W')
        
        self.attenuation_output_label.grid(row=0,column=2, sticky='E')
        self.attenuation_output.grid(row=0,column=3)

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

    def calculate(self,event=None):
        e_coef = round(self.interpolate(),4)
        HVL = math.log(1/2)/-(e_coef*self.density[self.v.get()])
        TVL = math.log(1/10)/-(e_coef*self.density[self.v.get()])
        print(HVL)
        self.attenuation_output['text']=str(e_coef)  
        
if __name__ == "__main__":
    window = Root()
    window.mainloop()
