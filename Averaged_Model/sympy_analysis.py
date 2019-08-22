from utils_pkg import addStr, multStr, divStr, minStr, bracket
import sympy


#DCM Buck Converter D2 analysis.
Vin = "Vin"
Vo = "Vo"
D1 = "D1"
D2 = "D2"
R = "Rload"
Ts = "Ts"
L = "L"

eq1 = minStr(Vo, multStr(Vin, divStr(D1, addStr(D1, D2))))

D_needed = sympy.symbols(D2)

D2_solved = sympy.solve(eq1, D_needed)

print("List of D2 solutions: {}".format(D2_solved))
print("Solved D2 as string: {}".format(D2_solved[0]))

#Update this variable as needed
D2_solved = D2_solved[0]

eq2 = minStr(Vo, 
            multStr(
                divStr(R, "2"), 
                multStr(D1, Ts), 
                divStr(minStr(Vin, Vo), L), 
                addStr(D1, bracket(D2_solved))
            )
        )

Vo_solve = sympy.symbols(Vo)
D1_needed = sympy.symbols(D1)

solved_vo_equation = sympy.solve(eq2, Vo_solve)
solved_d1_equation = sympy.solve(eq2, D1_needed)

print("Solve equation for Vo: {}".format(solved_vo_equation))
print("Solve equation for D1: {}".format(solved_d1_equation))
