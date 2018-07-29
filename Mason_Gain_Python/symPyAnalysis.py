import sympy
from sympy.utilities.lambdify import lambdify

from graphAnalysis_general import *
import ast, json, re

circuitPath = "Solved_Circuits\SMPS\DC_DC\CCM\Buck_Converter"
circuitNodesAnalyzed = "buck_nodes_gains_efficiency"
circuitObjectAnalyzed = "buck_object_efficiency"
outputFile = "efficiency_analysis"
#outputFile = "small_signal_analysis"

duty_cycle_equation = "(Vo/Vin)"
r_load_equation = "(Vo/Io)"

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

print("ID Dictionary: "+ str(json_id_dict)+"\n")

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
    #tran = re.sub(r"\b"+"D"+r"\b", duty_cycle_equation, tran)
    #tran = re.sub(r"\b"+"Rload"+r"\b", r_load_equation, tran)
    #print(tran+"\n")
    print(tran[1]+"\n")
    if "Output Impedance" in tran[1] or "Current" in tran[1]:
        standardForm = sympy.simplify("1/("+tran[0]+")")
    else:
        standardForm = sympy.simplify(tran[0])

    #Create expression to evaluate standard form equation quickly.
    standardLambda = lambdify(s, standardForm)

    print("Standard form of Equation: "+ str(standardForm)+"\n")
    print("DC Value of Standard Form Equation: " + str(standardLambda(0))+"\n")

    tran[0] = standardLambda(0)

#Calculate efficiency:
efficiency_equation = "((("+str(transfers[2][0])+")*Vin" + "-("+str(transfers[3][0])+")*VD1)"+"*("+str(transfers[4][0])+"))"+"/(Vin)"
print(efficiency_equation)
efficiency_equation = re.sub(r"\b"+"D"+r"\b", duty_cycle_equation, efficiency_equation)
efficiency_equation = re.sub(r"\b"+"Rload"+r"\b", r_load_equation, efficiency_equation)
print(efficiency_equation)
print(sympy.simplify(efficiency_equation))