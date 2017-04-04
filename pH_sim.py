import numpy as np, sys, imp, ast
from scipy.optimize import newton as nt
from scipy.optimize import brentq as bq
import bokeh.plotting as plt

class pH_calc:
    '''
    Mit diesem Packet kann der pH Wert eines beliebigen 
    Säure Basen Gemisches berechnet werden aufgrund der 
    Protonenbilanz. Die Benutzung erlogt folgendermassen:

    import pH_sim

    pH_input = pH_sim.pH_calc(c_acids = [liste mit säure 
                                        konzentrationen]
                    pKs_acids = [[liste mit pKs listen der säuren]]
                    c_bases = [liste mit basen konzentrationen]
                    pKs_bases = [[liste mit pKs listen der basen]])

    Nun kann der pH-Wert durch Aufruf der Funktion pH() berechnet 
    werden:

    pH = pH_input.pH()
    Regenwasser example:
    acids = HNO3, H2SO4, HCl
    base = NH3
    resulting pH should be around 4,16
    c_xy = flaot [mol/l]
    pKs = float

    defaults:
    [2e-5, 3e-5, 1e-5]
    [[-1.32], [-3, 1.92], [-6]]
    [2e-5]
    [[9.25]]
    '''
    def pH(self,input_string, a, b):
        '''
        Berechnet aufgrund der Protonenbilanz die H+ Konzentration
        aus. Summe Basen - Summe Säuren muss 0 ergeben, daher wird
        mit dem "brentq" Algorithmus die Nullstelle iterativ gesucht.
        Dazu sind die Ober und Untergrenze anzugeben (a, b). Durch
        testen wurden untenstehende Parameter angegeben. Dies 
        scheint alle Fälle abzudecken. As input a tuple/list in the
        form ([],[[]],[],[[]]) is needed (c_acid, pKs_acid, c_base,
        pKs_base).
        '''
        # These parameters were used from the balance function below
        param = input_string[:]
        self.c_acids = param[0]
        self.c_bases = param[2]
        self.pKs_acids = param[1]
        self.pKs_bases = param[3]

        # this happens if a strong acid is titrated
        max_iter = 0
        while self.balance(a) < 0 and max_iter < 50 and self.balance(b) < 0:
            a = a/10
            print("blop a: ",a)
            max_iter += 1

        # This happens if a strong base is titrated
        max_iter = 0
        while self.balance(b) > 0 and max_iter < 50 and self.balance(a) > 0:
            b = b*10
            print("blop b: ",b)
            max_iter += 1

        # print(self.balance(a))
        # print(self.balance(b))

        pH_bq = -np.log10(bq(self.balance,
            a,
            b,
            xtol=10e-20,
            rtol=4.5e-16,
            maxiter=1500,
            ))

        return pH_bq


    def balance(self, x):
        '''
        Berechnet die Werte für die Protonenbilanz, d.h.
        Summe starker und schwacher Säuren, sowie die 
        Summe der starken und schwachen Basen eines
        beliebigen Säure/Basen gemisches. Definirt 
        werden die Parameter mit der pH-Funktion.
        '''
        # summe für säuren
        C_ac_s = 0
        C_ac = 0
        i = 0
        for i in range(len(self.pKs_acids)):
            for pKs in self.pKs_acids[i]:
                if pKs <= 0:        # für starke säuren
                    C_ac_s += self.c_acids[i]
                else:               # für schwache säuren
                    c = self.c_acids[i]
                    Ks = 10**(-1*pKs)
                    C_ac += (Ks*c)/(Ks+x)

        # summe für basen
        C_ba_s = 0
        C_ba = 0
        i = 0
        for i in range(len(self.pKs_bases)):
            for pKs in self.pKs_bases[i]:
                if pKs >= 14:       # für starke basen
                    C_ba_s += self.c_bases[i]
                else:               # für schwache basen
                    cb = self.c_bases[i]
                    Ks = 10**(-1*pKs)
                    C_ba += (cb*x)/(Ks+x)

        return C_ac_s + C_ac + ((10**(-1*14))/x) - C_ba_s - C_ba - x


    def titration(self,input_string):
        '''
        simulate a titration with calculated proton balance and
        the pH calculated with calculated proton balance. As in-
        put a tuple/list in the form ([],[[]],[],[[]],[[]]) is 
        needed (c_acid, pKs_acid, c_base, pKs_base, pKs_tit).
        '''
        param = input_string[:]

        c_Acids = param[0]
        c_Bases = param[2]
        pKs_acids = param[1]
        pKs_bases = param[3]
        pKs_tit = param[4]

        ac = []
        pK_ac = []
        ba = []
        pK_ba = []

        ac = c_Acids[:]
        pK_ac = pKs_acids[:]
        ba = c_Bases[:]
        pK_ba = pKs_bases[:]
        pH_start = self.pH(input_string,1e-15,1e1)
        pH = [pH_start]
        c_tit = 0
        x = []

        if pH_start < 7:
            pH_end = 14
            step = sum(ac)/500
            modus = 'acid'
            pK_ba.append(pKs_tit[0])
        else:
            pH_end = 0
            step = sum(ba)/500
            modus = 'base'
            pK_ac.append(pKs_tit[0])

        if modus == 'acid':
            loop = 0
            start = 1e-5
            end = 1e1
            while pH[loop] <= pH_end and loop <= 2000:
                b = [i for i in ba]
                b.append(c_tit)
                value = self.pH((ac, pK_ac, b, pK_ba), start, end)
                start = 10 ** (-1 * (value + 2))
                end = 10 ** (-1 * (value - 2))
                pH.append(value)
                x.append(loop)
                loop += 1
                c_tit += step

        if modus == 'base':
            loop = 0
            start = 1e-12
            end = 1
            while pH[loop] >= pH_end and loop <= 2000:
                a = [i for i in ac]
                a.append(c_tit)
                value = self.pH((a, pK_ac, ba, pK_ba), start, end)
                start = 10 ** (-1 * (value + 2))
                end = 10 ** (-1 * (value - 2))
                pH.append(value)
                x.append(loop)
                loop += 1
                c_tit += step

        return x, pH[:-1], start, end
