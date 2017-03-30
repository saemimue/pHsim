import numpy as np, pandas as pd, os
import bokeh.plotting as plt
from pH_sim import pH_calc as psi

def pH(c_Ac, c_B, pKs_Ac, pKs_B):
    values = (c_Ac, c_B, pKs_Ac, pKs_B)
    return psi.pH(values)

def balance(c_Ac, c_B, pKs_Ac, pKs_B):
    values = (c_Ac, c_B, pKs_Ac, pKs_B)
    return psi.balance(x, values)

def titrate(c_Ac, c_B, pKs_Ac, pKs_B, pKs_Tit):
    values = (c_Ac, c_B, pKs_Ac, pKs_B, pKs_Tit)
    return psi.titration(values)

if __name__=='__main__':
    print("Used parameters were: c(Ac) = {}, c(B)= {} ,pKs(Ac) = {} "\
            "\npKs(B) = {}, pKs(Tit) = {}".format(
                c_Ac,
                C_B,
                pKs_Ac,
                pKs_B,
                pKs_Tit))
