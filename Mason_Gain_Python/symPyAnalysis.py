import sympy
from sympy.utilities.lambdify import lambdify
from sympy.solvers import solve

from graphAnalysis_general import *
import ast, json, re

circuitPath = "Solved_Circuits\SMPS\DC_DC\CCM\Buck_Converter"
circuitNodesAnalyzed = "buck_nodes_gains_efficiency"
circuitObjectAnalyzed = "buck_object_efficiency"


outputFile = "efficiency_analysis"
#outputFile = "small_signal_analysis"

outF = open(circuitPath+"\\"+outputFile+".txt", 'w')

#r_load_equation = "(Vo/Io)"

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

def calcDutyCycle():
    D = sympy.symbols("D")
    temp = solve(minStr(addStr(multStr("Vin", input_output_transfer), multStr("VD1", input_output_transfer_diode)), "Vo"), D)
    print("DUTY CYCLE SOLVE:"+ str(temp))
    return str(temp[0])

def calcEfficiency():
    return multStr(addStr(multStr(input_output_transfer, "Vin"), multStr(input_output_transfer_diode, "-VD1")), divStr(input_output_transfer_current, "Vin"))

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
input_output_transfer_diode = genGraphAnalysis(nodes, gains, json_id_dict["-von"], json_id_dict["vo"])
#Input to output transfer function, current
input_output_transfer_current = genGraphAnalysis(nodes, gains, json_id_dict["io"], json_id_dict["iin"])

transfers = [[input_impedance, "Input Impedance analysis:"], [output_impedance, "Output Impedance analysis:"], [input_output_transfer, "Input to Output analysis:"],
            [input_output_transfer_diode, "Input to Output Analysis, Diode contribution:"], [input_output_transfer_current, "Input to Output Current Analysis:"]]

s = sympy.symbols("s")
for tran in transfers:
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
input_output_transfer_current = transfers[4][0]

#Calculate efficiency:
efficiency_equation = calcEfficiency()
#print(efficiency_equation)
duty_cycle_equation = calcDutyCycle()
efficiency_equation = re.sub(r"\b"+"D"+r"\b", duty_cycle_equation, efficiency_equation)
#efficiency_equation = re.sub(r"\b"+"Rload"+r"\b", r_load_equation, efficiency_equation)
#duty_cycle_equation = re.sub(r"\b"+"Rload"+r"\b", r_load_equation, duty_cycle_equation)

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

outF.close()