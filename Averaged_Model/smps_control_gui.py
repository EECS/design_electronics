import tkinter as tk
import re
import sympy

from utils_pkg import substitute_expression, graph_transfers, addStr, multStr, divStr, parallel, bracket

class GUI:

    def __init__(self, master):
        self.DEFAULT_WIDGET_HEIGHT = 0.05
        self.PARAMETERS = {}

        self.master = master
        self.master.title("Electrical Engineer Equation GUI")
        self.canvas = tk.Canvas(self.master, width=800, height=800)
        self.canvas.pack()
        self.frame = tk.Frame(self.master, bg="blue")
        self.frame.place(relwidth=0.8, relheight=1, relx=0.1, rely=0)
        

        self.create_equation_frame()
        self.create_ts_frame()
        self.create_closed_loop_frame()
    
    def create_equation_frame(self):
        self.CURRENT_EQUATION_HEIGHT = 1
        self.EQUATION_FRAME_HEIGHT = 0.3

        self.equation_frame = tk.Frame(self.frame)
        self.equation_frame.place(relx=0, rely=0, relwidth=1, relheight=self.EQUATION_FRAME_HEIGHT)

        self.gvd_label = tk.Label(self.equation_frame, text="GVD(s) Transfer Function:")
        self.gvd_label.place(relx=0, rely=0, relwidth=0.25, relheight=4*self.DEFAULT_WIDGET_HEIGHT)

        self.gvd_text = tk.Text(self.equation_frame)
        self.gvd_text.place(relx=0.25, rely=0, relwidth=0.75, relheight=4*self.DEFAULT_WIDGET_HEIGHT)

        self.CURRENT_EQUATION_HEIGHT += 3

        self.hs_label = tk.Label(self.equation_frame, text="H(s) Transfer Function:")
        self.hs_label.place(relx=0, rely=self.CURRENT_EQUATION_HEIGHT*self.DEFAULT_WIDGET_HEIGHT,
            relwidth=0.25, relheight=4*self.DEFAULT_WIDGET_HEIGHT)

        self.hs_text = tk.Text(self.equation_frame)
        self.hs_text.place(relx=0.25, rely=self.CURRENT_EQUATION_HEIGHT*self.DEFAULT_WIDGET_HEIGHT,
            relwidth=0.75, relheight=4*self.DEFAULT_WIDGET_HEIGHT)

        self.CURRENT_EQUATION_HEIGHT += 4

        self.gc_label = tk.Label(self.equation_frame, text="Gc(s) (Compensator) Transfer Function:")
        self.gc_label.place(relx=0, rely=self.CURRENT_EQUATION_HEIGHT*self.DEFAULT_WIDGET_HEIGHT,
            relwidth=0.25, relheight=4*self.DEFAULT_WIDGET_HEIGHT)

        self.gc_text = tk.Text(self.equation_frame)
        self.gc_text.place(relx=0.25, rely=self.CURRENT_EQUATION_HEIGHT*self.DEFAULT_WIDGET_HEIGHT,
            relwidth=0.75, relheight=4*self.DEFAULT_WIDGET_HEIGHT)

        self.CURRENT_EQUATION_HEIGHT += 4

        self.vm_label = tk.Label(self.equation_frame, text="VM: (Put in 1/Vm)")
        self.vm_label.place(relx=0, rely=self.CURRENT_EQUATION_HEIGHT*self.DEFAULT_WIDGET_HEIGHT,
            relwidth=0.25, relheight=4*self.DEFAULT_WIDGET_HEIGHT)

        self.vm_text = tk.Text(self.equation_frame)
        self.vm_text.place(relx=0.25, rely=self.CURRENT_EQUATION_HEIGHT*self.DEFAULT_WIDGET_HEIGHT,
            relwidth=0.75, relheight=4*self.DEFAULT_WIDGET_HEIGHT)
    
    def create_ts_frame(self):
        self.CURRENT_TS_HEIGHT = 1
        self.TS_FRAME_HEIGHT = 0.1

        self.ts_frame = tk.Frame(self.frame)
        self.ts_frame.place(relx=0, rely=self.EQUATION_FRAME_HEIGHT,
                            relwidth=1, relheight=self.TS_FRAME_HEIGHT)
        
        self.ts_button = tk.Button(self.ts_frame, text="Generate T(s) Transfer Function", command=lambda: self.create_ts_function())
        self.ts_button.place(relx=0.35, rely=0, relwidth=0.25, relheight=8*self.DEFAULT_WIDGET_HEIGHT)

        self.CURRENT_TS_HEIGHT += 7

        self.ts_label = tk.Label(self.ts_frame, text="T(s) Transfer Function:")
        self.ts_label.place(relx=0, rely=self.CURRENT_TS_HEIGHT*self.DEFAULT_WIDGET_HEIGHT,
                            relwidth=0.25, relheight=8*self.DEFAULT_WIDGET_HEIGHT)

        self.ts_text_var = tk.StringVar()
        self.ts_text = tk.Entry(self.ts_frame, textvariable=self.ts_text_var)
        self.ts_text.place(relx=0.25, rely=self.CURRENT_TS_HEIGHT*self.DEFAULT_WIDGET_HEIGHT,
                        relwidth=0.75, relheight=12*self.DEFAULT_WIDGET_HEIGHT)

        self.CURRENT_TS_HEIGHT += 12

    def create_ts_function(self):
        self.ts_hs_text = self.hs_text.get("1.0", "end-1c")
        self.ts_gvd_text = self.gvd_text.get("1.0", "end-1c")
        self.ts_gc_text = self.gc_text.get("1.0", "end-1c")
        self.ts_vm_text = self.vm_text.get("1.0", "end-1c")

        ts_text = sympy.simplify(multStr(self.ts_gc_text, self.ts_gvd_text, bracket(self.ts_vm_text), self.ts_hs_text))
        self.ts_text_var.set(ts_text)
        print("T(s) Transfer Function is: {}".format(self.ts_text_var.get()))
    
    def create_closed_loop_frame(self):
        self.CURRENT_CLOSED_HEIGHT = 0
        self.CLOSED_FRAME_HEIGHT = 0.2
        self.DEFAULT_LOOP_HEIGHT = 6

        self.closed_frame = tk.Frame(self.frame)
        self.closed_frame.place(relx=0, rely=(self.TS_FRAME_HEIGHT+self.EQUATION_FRAME_HEIGHT),
                            relwidth=1, relheight=self.CLOSED_FRAME_HEIGHT)

        self.vovin_label = tk.Label(self.closed_frame, text="Vo/Vin (s) Transfer Function:")
        self.vovin_label.place(relx=0, rely=0,
                            relwidth=0.25, relheight=self.DEFAULT_LOOP_HEIGHT*self.DEFAULT_WIDGET_HEIGHT)
        self.vovin_text = tk.Text(self.closed_frame)
        self.vovin_text.place(relx=0.25, rely=0,
                            relwidth=0.75, relheight=self.DEFAULT_LOOP_HEIGHT*self.DEFAULT_WIDGET_HEIGHT)

        self.CURRENT_CLOSED_HEIGHT += self.DEFAULT_LOOP_HEIGHT

        self.output_imped_label = tk.Label(self.closed_frame, text="Vo/Io (s) (Output Impedance) Transfer Function:")
        self.output_imped_label.place(relx=0, rely=self.CURRENT_CLOSED_HEIGHT*self.DEFAULT_WIDGET_HEIGHT,
                            relwidth=0.25, relheight=self.DEFAULT_LOOP_HEIGHT*self.DEFAULT_WIDGET_HEIGHT)
        self.output_imped_text = tk.Text(self.closed_frame)
        self.output_imped_text.place(relx=0.25, rely=self.CURRENT_CLOSED_HEIGHT*self.DEFAULT_WIDGET_HEIGHT,
                            relwidth=0.75, relheight=self.DEFAULT_LOOP_HEIGHT*self.DEFAULT_WIDGET_HEIGHT)

        self.CURRENT_CLOSED_HEIGHT += self.DEFAULT_LOOP_HEIGHT

        self.closed_params_button = tk.Button(self.closed_frame, text="Generate Parameters", command=lambda: self.create_parameters())
        self.closed_params_button.place(relx=0.35, rely=self.CURRENT_CLOSED_HEIGHT*self.DEFAULT_WIDGET_HEIGHT,
                                relwidth=0.25, relheight=self.DEFAULT_LOOP_HEIGHT*self.DEFAULT_WIDGET_HEIGHT)
    
    def create_parameters(self):
        ts_text = self.ts_text_var.get()
        output_imped_text = self.output_imped_text.get("1.0", "end-1c")
        input_output_text = self.vovin_text.get("1.0", "end-1c")

        #Equations to pull parameters from
        equations = [ts_text, output_imped_text, input_output_text]

        self.parameters = set()
        for equation in equations:
            #Finds all characters that are not single digits or an s parameter.
            #Would need to tweak for jw domain.
            self.parameters.update(re.findall(r'[A-Za-rt-z]+(?=\b)|[A-Za-rt-z]+\d+', equation))

        self.create_parameters_frame()
    
    def create_parameters_frame(self):
        if self.parameters:
            if "parameter_frame" in dir(self):
                self.parameter_frame.destroy()

            self.PARAMETERS_FRAME_HEIGHT = 0.5
            self.CURRENT_PARAMETER_HEIGHT = 0
            self.PARAMETER_IND_HEIGHT = 1

            self.parameter_frame = tk.Frame(self.frame)
            self.parameter_frame.place(relx=0, rely=(self.TS_FRAME_HEIGHT+self.EQUATION_FRAME_HEIGHT+ self.CLOSED_FRAME_HEIGHT),
                            relwidth=1, relheight=self.PARAMETERS_FRAME_HEIGHT)

            self.param_dict = {}
            for param in self.parameters:
                label = tk.Label(self.parameter_frame, text=param)
                label.place(relx=0, rely=self.CURRENT_PARAMETER_HEIGHT*self.DEFAULT_WIDGET_HEIGHT,
                            relwidth=0.25, relheight=self.PARAMETER_IND_HEIGHT*self.DEFAULT_WIDGET_HEIGHT)

                text = tk.Text(self.parameter_frame)
                text.place(relx=0.25, rely=self.CURRENT_PARAMETER_HEIGHT*self.DEFAULT_WIDGET_HEIGHT,
                            relwidth=0.25, relheight=self.PARAMETER_IND_HEIGHT*self.DEFAULT_WIDGET_HEIGHT)

                self.param_dict[label] = text
                self.CURRENT_PARAMETER_HEIGHT += self.PARAMETER_IND_HEIGHT
            
            self.evaluate_closed_button = tk.Button(self.parameter_frame, text="Evaluated Closed Loop Transfer Functions", command=lambda: self.graph_transfers())
            self.evaluate_closed_button.place(relx=0.25, rely=self.CURRENT_PARAMETER_HEIGHT*self.DEFAULT_WIDGET_HEIGHT,
                            relwidth=0.25, relheight=self.PARAMETER_IND_HEIGHT*self.DEFAULT_WIDGET_HEIGHT)
            
            self.CURRENT_PARAMETER_HEIGHT += self.PARAMETER_IND_HEIGHT

            self.generate_ts_button = tk.Button(self.parameter_frame, text="Generated Closed Loop Transfer Function w/ Subs", command=lambda: self.generate_ts())
            self.generate_ts_button.place(relx=0.25, rely=self.CURRENT_PARAMETER_HEIGHT*self.DEFAULT_WIDGET_HEIGHT,
                            relwidth=0.25, relheight=self.PARAMETER_IND_HEIGHT*self.DEFAULT_WIDGET_HEIGHT)

    def graph_transfers(self):
        components = {}

        for param_name, param_value in self.param_dict.items():
            components[param_name["text"]] = param_value.get("1.0", "end-1c")
        
        self.transfer_functions = {}

        Ts = self.ts_text_var.get()
        open_loop_output_impedance = self.output_imped_text.get("1.0", "end-1c")
        open_loop_vovin = self.vovin_text.get("1.0", "end-1c")

        #Closed Loop Output Impedance
        #Zout = -Zout(open loop)
        #        --------------
        #        1    +    T(s)
        #
        #Closed Loop Vo/Vin (s)
        #Vo/Vin = Vo/Vin(Open Loop)
        #         -----------------
        #         1    +    T(s)

        closed_output_impedance = sympy.simplify(divStr(multStr("-1", open_loop_output_impedance), addStr("1", Ts)))
        closed_vovin = sympy.simplify(divStr(open_loop_vovin, addStr("1", Ts)))

        self.transfer_functions["Output Impedance"] = closed_output_impedance
        self.transfer_functions["Input to Output"] = closed_vovin
        self.transfer_functions["T(s)"] = Ts

        self.transfer_functions["Gc(s)"] = sympy.simplify(self.gc_text.get("1.0", "end-1c"))

        graph_transfers(self.transfer_functions, components)

    def generate_ts(self):
        Ts = self.ts_text_var.get()
        components = {}

        for param_name, param_value in self.param_dict.items():
            components[param_name["text"]] = param_value.get("1.0", "end-1c")

        print("T(s) with substituted components: {}".format(substitute_expression(Ts, components)))

root = tk.Tk()
window = GUI(root)
root.mainloop()
