import numpy as np, pandas as pd, os
import pH_sim as p

psi = p.pH_calc()

def pH(c_Ac, c_B, pKs_Ac, pKs_B):
    values = (c_Ac, pKs_Ac, c_B, pKs_B)
    return psi.pH(values)

def balance(c_Ac, c_B, pKs_Ac, pKs_B):
    values = (c_Ac, c_B, pKs_Ac, pKs_B)
    return psi.balance(x, values)



def titrate(c_Ac, c_B, pKs_Ac, pKs_B, pKs_Tit):
    values = (c_Ac,  pKs_Ac, c_B, pKs_B, pKs_Tit)
    print("\n",values,"\n")
    head, script, div = psi.titration(values)
    return head, script, div

if __name__=='__main__':
    print("Used parameters were: c(Ac) = {}, c(B)= {} ,pKs(Ac) = {} "\
            "\npKs(B) = {}, pKs(Tit) = {}".format(
                c_Ac,
                C_B,
                pKs_Ac,
                pKs_B,
                pKs_Tit))
