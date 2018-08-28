import sympy
from sympy.utilities.lambdify import lambdify
from sympy.solvers import solve

from graphAnalysis_general import *
import ast, json, re

circuitPath = "Solved_Circuits\SMPS\DC_DC\CCM\Buck_Converter"
EFFICIENCY_ANALYSIS = False
input_output_transfer_current = "D"

if EFFICIENCY_ANALYSIS:
    outputFile = "efficiency_analysis"

    circuitNodesAnalyzed = "buck_nodes_gains_efficiency"
    circuitObjectAnalyzed = "buck_object_efficiency"
else:
    outputFile = "small_signal_analysis"

    circuitNodesAnalyzed = "buck_nodes_gains_small_signal"
    circuitObjectAnalyzed = "buck_object_small_signal"



outF = open(circuitPath+"\\"+outputFile+".txt", 'w')

r_load_equation = "(Vo/Io)"

def logPrint(outStr):
    '''
    Logs and prints outStr to outF and cmd.
    '''
    outF.write(outStr+"\n")
    print(outStr)

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
logPrint(outStr)

'''
Query files and generate transfer functions using mason gain formula
for all transfer functions of interest.
'''
if not EFFICIENCY_ANALYSIS:
    #Input impedance analysis
    input_impedance = genGraphAnalysis(nodes, gains, json_id_dict["vin"], json_id_dict["iin"])
    #Output impedance analysis
    output_impedance = genGraphAnalysis(nodes, gains, json_id_dict["io"], json_id_dict["vo"])
    #Duty to Output Voltage analysis
    duty_to_output_transfer = genGraphAnalysis(nodes, gains, json_id_dict["d"], json_id_dict["vo"])

    transfers = [[input_impedance, "Input Impedance analysis:"], [output_impedance, "Output Impedance analysis:"], [duty_to_output_transfer, "Duty to Output Voltage Transfer analysis:"]]
else:
    #Input to output transfer function, diode contribution, only used in the efficiency analysis.
    input_output_transfer_diode = genGraphAnalysis(nodes, gains, json_id_dict["von"], json_id_dict["vo"])
    transfers = [[input_output_transfer_diode, "Input Voltage to Output Voltage Analysis, Diode contribution:"]]

#Input to output transfer function, used in both small signal and efficiency analyses
input_output_transfer = genGraphAnalysis(nodes, gains, json_id_dict["vin"], json_id_dict["vo"])
transfers.append([input_output_transfer, "Input Voltage to Output Voltage analysis:"])

'''
Create and symplify all transfer functions for specific type of
analysis.
'''
s = sympy.symbols("s")
for tran in transfers:
    #Print the type of analysis.
    outStr = tran[1]+"\n"
    logPrint(outStr)

    if "Input Impedance" in tran[1] or "Current" in tran[1]:
        standardForm = sympy.simplify(divStr("1",tran[0]))
    else:
        standardForm = sympy.simplify(tran[0])

    #Create expression to evaluate standard form equation quickly.
    standardLambda = lambdify(s, standardForm)

    outStr = "Standard form of Equation: "+ str(standardForm)+"\n"
    logPrint(outStr)

    outStr = "DC Value of Standard Form Equation: " + str(standardLambda(0))+"\n"
    logPrint(outStr)

    if EFFICIENCY_ANALYSIS:
        #If efficiency analylsis, DC value is the only value of interest.
        #Update transfer function with DC value of transfer function.
        tran[0] = str(standardLambda(0))
    else:
        #Update transfer function with simplified s-domain expression.
        tran[0] = str(standardForm)

'''
Create variables that are dependent upon the type of analysis
that are the simplified equations of the different transfer functions.
'''
if not EFFICIENCY_ANALYSIS:
    input_impedance = transfers[0][0]
    input_impedance = re.sub(r"\b"+"Rload"+r"\b", r_load_equation, input_impedance)
    outStr = "Input Impedance Equation Simplified: "+ str(sympy.simplify(input_impedance))+"\n"
    logPrint(outStr)

    output_impedance = transfers[1][0]
    output_impedance = re.sub(r"\b"+"Rload"+r"\b", r_load_equation, output_impedance)
    outStr = "Output Impedance Equation Simplified: "+ str(sympy.simplify(output_impedance))+"\n"
    logPrint(outStr)

    duty_output = transfers[2][0]
    duty_output = re.sub(r"\b"+"Rload"+r"\b", r_load_equation, duty_output)
    outStr = "Duty Cycle to Output Voltage Equation Simplified: "+ str(sympy.simplify(duty_output))+"\n"
    logPrint(outStr)

    input_output_transfer = transfers[3][0]
    input_output_transfer = re.sub(r"\b"+"Rload"+r"\b", r_load_equation, input_output_transfer)
    outStr = "Input Voltage to Output Voltage Equation Simplified: "+ str(sympy.simplify(input_output_transfer))+"\n"
    logPrint(outStr)
else:
    input_output_transfer_diode = transfers[0][0]
    input_output_transfer = transfers[1][0]

    #Calculate input current
    input_current = calcInputCurrent()

    #Calculate efficiency:
    efficiency_equation = calcEfficiency()
    duty_cycle_equation = calcDutyCycle()

    efficiency_equation = re.sub(r"\b"+"D"+r"\b", duty_cycle_equation, efficiency_equation)
    efficiency_equation = re.sub(r"\b"+"Rload"+r"\b", r_load_equation, efficiency_equation)

    input_current = re.sub(r"\b"+"D"+r"\b", duty_cycle_equation, input_current)

    input_current = re.sub(r"\b"+"Rload"+r"\b", r_load_equation, input_current)
    duty_cycle_equation = re.sub(r"\b"+"Rload"+r"\b", r_load_equation, duty_cycle_equation)

    duty_cycle_equation = sympy.simplify(duty_cycle_equation)

    outStr = "Efficiency equation: "+ str(efficiency_equation)+"\n"
    logPrint(outStr)

    outStr = "Efficiency equation simplified: "+ str(sympy.simplify(efficiency_equation))+"\n"
    logPrint(outStr)

    outStr = "Duty Cycle: "+ str(duty_cycle_equation)+"\n"
    logPrint(outStr)

    outStr = "Input Current: "+ str(sympy.simplify(input_current))+"\n"
    logPrint(outStr)

outF.close()