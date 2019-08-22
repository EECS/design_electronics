import tkinter as tk
import re
import sympy

from utils_pkg import substitute_expression, graph_transfers, addStr, multStr, divStr, parallel

class GUI:

    def __init__(self, master):
        self.DEFAULT_WIDGET_HEIGHT = 0.05
        self.PARAMETERS = {}

        self.master = master
        self.master.title("Electrical Engineer Equation GUI")
        self.canvas = tk.Canvas(self.master, width=800, height=800)
        self.canvas.pack()
        self.frame = tk.Frame(self.master, bg="blue")
        self.frame.place(relwidth=0.8, relheight=0.8, relx=0.1, rely=0.1)

        self.create_circuit_solver()
        self.create_equations()
    
    def create_circuit_solver(self):
        self.CURRENT_SOLVER_HEIGHT = 1

        self.solver_frame = tk.Frame(self.frame, bg="red")
        self.solver_frame.place(relx=0, rely=0, relwidth=1, relheight=0.5)

        self.solver_label = tk.Label(self.solver_frame, text="Equation to Simplify:")
        self.solver_label.place(relx=0, rely=0, relwidth=0.25, relheight=4*self.DEFAULT_WIDGET_HEIGHT)

        self.solver_text = tk.Text(self.solver_frame)
        self.solver_text.place(relx=0.25, rely=0, relwidth=0.75, relheight=4*self.DEFAULT_WIDGET_HEIGHT)
        self.CURRENT_SOLVER_HEIGHT += 4

        self.simplify_button = tk.Button(self.solver_frame, text="Simplify Equation", command=lambda: self.simplify_equation())
        self.simplify_button.place(relx=0.25, rely=self.CURRENT_SOLVER_HEIGHT*self.DEFAULT_WIDGET_HEIGHT, relwidth=0.25, relheight=2*self.DEFAULT_WIDGET_HEIGHT)
        self.CURRENT_SOLVER_HEIGHT += 2

        self.solved_eq_label = tk.Label(self.solver_frame, text="Simplified Equation:")
        self.solved_eq_label.place(relx=0, rely=self.CURRENT_SOLVER_HEIGHT*self.DEFAULT_WIDGET_HEIGHT, relwidth=0.25, relheight=4*self.DEFAULT_WIDGET_HEIGHT)

        self.solve_eq_text = tk.StringVar()

        self.solved_eq = tk.Entry(self.solver_frame, textvariable=self.solve_eq_text)
        self.solved_eq.place(relx=0.25, rely=self.CURRENT_SOLVER_HEIGHT*self.DEFAULT_WIDGET_HEIGHT, relwidth=0.75, relheight=4*self.DEFAULT_WIDGET_HEIGHT)

    def create_equations(self):
        self.CURRENT_EQUATION_HEIGHT = 1

        self.equation_frame = tk.Frame(self.frame, bg="gray")
        self.equation_frame.place(relwidth=1, relheight=1, relx=0, rely=self.DEFAULT_WIDGET_HEIGHT*self.CURRENT_SOLVER_HEIGHT)

        self.transfer_label = tk.Label(self.equation_frame, text="Transfer Equation:")
        self.transfer_label.place(relx=0, rely=0, relwidth=0.25, relheight=self.CURRENT_EQUATION_HEIGHT*2*self.DEFAULT_WIDGET_HEIGHT)

        self.transfer_equation = tk.Text(self.equation_frame)
        self.transfer_equation.place(relx=0.25, rely=0, relwidth=0.75, relheight=self.CURRENT_EQUATION_HEIGHT*2*self.DEFAULT_WIDGET_HEIGHT)

        self.detect_button = tk.Button(self.equation_frame, text="Detect Parameters", command=lambda: self.create_parameters())
        self.detect_button.place(relx=0.25, rely=self.CURRENT_EQUATION_HEIGHT*self.DEFAULT_WIDGET_HEIGHT, relwidth=0.25, relheight=self.DEFAULT_WIDGET_HEIGHT)
        self.update_button = tk.Button(self.equation_frame, text="Update Equation", command=lambda: self.update_equation())
        self.update_button.place(relx=0.5, rely=self.CURRENT_EQUATION_HEIGHT*self.DEFAULT_WIDGET_HEIGHT, relwidth=0.25, relheight=self.DEFAULT_WIDGET_HEIGHT)
        self.CURRENT_EQUATION_HEIGHT += 2
    
    def update_equation(self):
        self.eq_text = self.transfer_equation.get("1.0", "end-1c")
        print("Equation is now: {}".format(self.eq_text))
    
    def create_parameters(self):
        '''
        Given a text frame, returns the text in that frame.
        text_frame (tk.Text)
        '''
        self.eq_text = self.transfer_equation.get("1.0", "end-1c")
        #Finds all characters that are not single digits or an s parameter.
        #Would need to tweak for jw domain.
        result = re.findall(r'[A-Za-rt-z]+(?=\b)|[A-Za-rt-z]+\d+', self.eq_text)

        if result:
            if self.PARAMETERS:
                self.param_frame.destroy()
                self.CURRENT_PARAM_HEIGHT -= (2*len(self.PARAMETERS)+2)
                self.PARAMETERS ={}

            self.CURRENT_PARAM_HEIGHT = 1

            self.param_frame = tk.Frame(self.frame, bg="green")
            self.param_frame.place(relx=0, rely=(self.CURRENT_EQUATION_HEIGHT+self.CURRENT_SOLVER_HEIGHT)*self.DEFAULT_WIDGET_HEIGHT, 
                relwidth=1, relheight=0.5)

            self.parameter_label = tk.Label(self.param_frame, text="Parameters in equation:")
            self.parameter_label.place(relx=0, rely=0, relwidth=0.25, relheight=self.DEFAULT_WIDGET_HEIGHT)
        
            self.PARAMETERS = set(result)
            text = ""
            for param in self.PARAMETERS:
                text += param + " "

            self.param_text = tk.Label(self.param_frame, text=text)
            self.param_text.place(relx=0.25, rely=0, relwidth=0.75, relheight=self.DEFAULT_WIDGET_HEIGHT)

            self.param_vals ={}
            for param in self.PARAMETERS:
                tk.Label(self.param_frame, text=param).place(relx=0, rely=self.CURRENT_PARAM_HEIGHT*self.DEFAULT_WIDGET_HEIGHT, relwidth=0.25, relheight=2*self.DEFAULT_WIDGET_HEIGHT)
                self.param_vals[param] = tk.Text(self.param_frame)
                self.param_vals[param].place(relx=0.25, rely=self.CURRENT_PARAM_HEIGHT*self.DEFAULT_WIDGET_HEIGHT, relwidth=0.25, relheight=2*self.DEFAULT_WIDGET_HEIGHT)
                self.CURRENT_PARAM_HEIGHT += 2
            
            self.generate_analysis_button = tk.Button(self.param_frame, text="Generate analysis", command=lambda: self.conduct_analysis())
            self.generate_analysis_button.place(relx=0.25, rely=self.CURRENT_PARAM_HEIGHT*self.DEFAULT_WIDGET_HEIGHT, relwidth=0.25, relheight=2*self.DEFAULT_WIDGET_HEIGHT)


    def conduct_analysis(self):
        components = {}
        for name, tk_text in self.param_vals.items():
            components[name] = float(tk_text.get("1.0", "end-1c"))

        transfers = {}
        transfers["Test Transfer"] = self.eq_text
        print("Analysis being conducted on this equation: {}".format(self.eq_text))
        graph_transfers(transfers, components)
    
    def simplify_equation(self):
        self.circuit_equation = self.solver_text.get("1.0", "end-1c")
        simplification = sympy.simplify(eval(self.circuit_equation))
        print(simplification)
        self.solve_eq_text.set(simplification)

root = tk.Tk()
window = GUI(root)
root.mainloop()
