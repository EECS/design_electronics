from utils_pkg import *
import copy

if __name__=="__main__":

    parser = argparse.ArgumentParser(description="Playground Analysis")
    parser.add_argument("-graph", type=bool, help="Graph transfer or just analyze converter.")
    output_file = open_loop_output_file

    args = vars(parser.parse_args())

    print(args)

    C1="(1/(s*C1))"
    RC1="RC1"
    Rload="Rload"
    L1="(s*L1)"
    RL1="RL1"
    RQ1="D*RQ1"
    VD1="VD1*(1-D)"
    Vin="D*Vin"
    D="D"

    transfers = {}
    VinNum = 12
    Vo = 5
    Io= 3
    RloadNum=Vo/Io

    components = {
        "C1":100e-6,
        "L1":9.4e-6,
        "RL1":10e-3,
        "RQ1":100e-3,
        "RC1":100e-3,
        "Rload":RloadNum,
        "H": 10,
        "D": 0.461,
        "Vin": VinNum
    }

    #CCM buck converter analysis
    VoVinTransfer=multStr(divStr(parallel(addStr(RC1, C1), Rload), addStr(parallel(addStr(RC1, C1), Rload), L1, RL1, RQ1)), D)
    OutputImpedance = parallel(parallel(Rload, addStr(RC1, C1)), addStr(L1, RL1, RQ1))
    Efficiency = multStr(divStr(parallel(addStr(RC1, C1), Rload), addStr(parallel(addStr(RC1, C1), Rload), L1, RL1, RQ1)), minStr(Vin, VD1))
    ControlToOutput = multStr(divStr(parallel(addStr(RC1, C1), Rload), addStr(parallel(addStr(RC1, C1), Rload), L1, RL1, RQ1)), divStr(Vin, D))

    transfers.update({"Vin to Vo Transfer Function": sympy.simplify(VoVinTransfer)})
    transfers.update({"Output Impedance Transfer Function": sympy.simplify(OutputImpedance)})
    transfers.update({"Control to Output Transfer Function": sympy.simplify(ControlToOutput)})

    if args["graph"]:
        graph_transfers(copy.deepcopy(transfers), components, end_freq=10000)
    else:
        transfers.update({"Efficiency Transfer Function": sympy.simplify(Efficiency)})
        print_and_log_transfers(transfers, output_file)

