import sympy
from sympy.utilities.lambdify import lambdify
from sympy.solvers import solve

from graphAnalysis_general import *
import ast, json, re

circuitPath = "Solved_Circuits\SMPS\DC_DC\CCM\Buck_Converter"
circuitNodesAnalyzed = "buck_nodes_gains_efficiency"
circuitObjectAnalyzed = "buck_object_efficiency"
EFFICIENCY_ANALAYSIS = True
input_output_transfer_current = "D"




if EFFICIENCY_ANALAYSIS:
    outputFile = "efficiency_analysis"
else:
    outputFile = "small_signal_analysis"

#outputFile = "small_signal_analysis"

outF = open(circuitPath+"\\"+outputFile+".txt", 'w')

r_load_equation = "(Vo/Io)"

def divStr(a, b):
    '''
    Returns a/b as string.
    '''
    return "(("+str(a)+")/("+str(b)+"))"

def minStr(a, b):
    '''
    Returns a-b as string.
    '''
    return "(("+str(a)+")-("+str(b)+"))"

def addStr(a, b):
    '''
    Returns a+b as string.
    '''
    return "(("+str(a)+")+("+str(b)+"))"

def multStr(a, b):
    '''
    Returns a*b as string.
    '''
    return "(("+str(a)+")*("+str(b)+"))"

def calcInputCurrent():
    #Calculate input current as a stand alone variable
    current = sympy.simplify(multStr("Io", input_output_transfer_current))
    #current = sympy.simplify(multStr("Io", "D"))
    #efficiency_equation = re.sub(r"\b"+"D"+r"\b", duty_cycle_equation, efficiency_equation)
    #print("current is "+ str(current))
    return str(current)

def calcDutyCycle():
    D = sympy.symbols("D")
    temp = solve(minStr(addStr(multStr("Vin", input_output_transfer), multStr("VD1", input_output_transfer_diode)), "Vo"), D)
    #print("temp is "+ str(temp))
    return str(temp[0])

def calcEfficiency():
    efficiency = divStr(multStr("Vo", "Io"), multStr("Vin", input_current))
    #print("Efficiency is "+ str(efficiency))
    return efficiency

#Gains must be on line 4, 1 based index, of the text file generated from mason_gain_js
#Next nodes must be on line 2, 1 based index
gainLine = 4
nodeLine = 2

file_nodes = open(circuitPath+"\\"+circuitNodesAnalyzed+".txt")

with open(circuitPath+"\\"+circuitObjectAnalyzed+".txt") as f:
    json_data = json.load(f)

lineNum = 0
nodes = []
gains = []
for line in file_nodes.readlines():
    if lineNum == nodeLine-1:
        nodes = ast.literal_eval(line)
    elif lineNum == gainLine-1:
        gains = ast.literal_eval(line)

    lineNum += 1

json_id_dict = {}

#Get id's and node numbers from JSON object, place in dictionary.
for obj in json_data:
    if obj["group"] == "nodes":
        json_id_dict[obj["data"]["id"]] = obj["data"]["nodeNumber"]

outStr = "ID Dictionary: "+ str(json_id_dict)+"\n"
outF.write(outStr+"\n")
print(outStr)

#Input impedance analysis
input_impedance = genGraphAnalysis(nodes, gains, json_id_dict["vin"], json_id_dict["iin"])
#Output impedance analysis
output_impedance = genGraphAnalysis(nodes, gains, json_id_dict["io"], json_id_dict["vo"])
#Input to output transfer function
input_output_transfer = genGraphAnalysis(nodes, gains, json_id_dict["vin"], json_id_dict["vo"])
#Input to output transfer function, diode contribution
input_output_transfer_diode = genGraphAnalysis(nodes, gains, json_id_dict["von"], json_id_dict["vo"])
#Input to output transfer function, current
#input_output_transfer_current = genGraphAnalysis(nodes, gains, json_id_dict["il"], json_id_dict["iin"])

transfers = [[input_impedance, "Input Impedance analysis:"], [output_impedance, "Output Impedance analysis:"], [input_output_transfer, "Input Voltage to Output Voltage analysis:"],
            [input_output_transfer_diode, "Input Voltage to Output Voltage Analysis, Diode contribution:"]]

s = sympy.symbols("s")
for tran in transfers:
    #Print the type of analysis.
    outStr = tran[1]+"\n"
    outF.write(outStr+"\n")
    print(outStr)

    if "Output Impedance" in tran[1] or "Current" in tran[1]:
        standardForm = sympy.simplify(divStr("1",tran[0]))
    else:
        standardForm = sympy.simplify(tran[0])

    #Create expression to evaluate standard form equation quickly.
    standardLambda = lambdify(s, standardForm)

    outStr = "Standard form of Equation: "+ str(standardForm)+"\n"
    outF.write(outStr+"\n")
    print(outStr)

    outStr = "DC Value of Standard Form Equation: " + str(standardLambda(0))+"\n"
    outF.write(outStr+"\n")
    print(outStr)

    tran[0] = standardLambda(0)

input_impedance = transfers[0][0]
output_impedance = transfers[1][0]
input_output_transfer = transfers[2][0]
input_output_transfer_diode = transfers[3][0]
#input_output_transfer_current = transfers[4][0]

#Calculate input current
input_current = calcInputCurrent()

#Calculate efficiency:
efficiency_equation = calcEfficiency()
#print(efficiency_equation)
duty_cycle_equation = calcDutyCycle()
efficiency_equation = re.sub(r"\b"+"D"+r"\b", duty_cycle_equation, efficiency_equation)
input_current = re.sub(r"\b"+"D"+r"\b", duty_cycle_equation, input_current)

efficiency_equation = re.sub(r"\b"+"Rload"+r"\b", r_load_equation, efficiency_equation)
input_current = re.sub(r"\b"+"Rload"+r"\b", r_load_equation, input_current)
duty_cycle_equation = re.sub(r"\b"+"Rload"+r"\b", r_load_equation, duty_cycle_equation)

duty_cycle_equation = sympy.simplify(duty_cycle_equation)

outStr = "Efficiency equation: "+ str(efficiency_equation)+"\n"
outF.write(outStr+"\n")
print(outStr)

outStr = "Efficiency equation simplified: "+ str(sympy.simplify(efficiency_equation))+"\n"
outF.write(outStr+"\n")
print(outStr)

outStr = "Duty Cycle: "+ str(duty_cycle_equation)+"\n"
outF.write(outStr+"\n")
print(outStr)

outStr = "Input Current: "+ str(sympy.simplify(input_current))+"\n"
outF.write(outStr+"\n")
print(outStr)

outF.close()