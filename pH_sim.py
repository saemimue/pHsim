import numpy as np, sys, imp, ast
from scipy.optimize import fsolve as fs
from scipy.optimize import brentq as bq

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
    def pH(self,input_string):
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
        param = input_string[:]
        self.c_acids = param[0]
        self.c_bases = param[2]
        self.pKs_acids = param[1]
        self.pKs_bases = param[3]

        #print('-----------------------------')
        #print('pH Function Input from GUI')
        #print(self.c_acids, self.pKs_acids, self.c_bases, self.pKs_bases)
        #print(type(self.c_acids),type(self.pKs_acids),type(self.c_bases),type(self.pKs_bases))
        #print('-----------------------------\n')
         
        ac = sum(self.c_acids)
        ba = sum(self.c_bases)
        if ac > ba:
            a = 1e-15
            b = 1e1
        else:
            a = 1e-15
            b = 1e1
        #pH_fs = -np.log10(fs(self.balance, 1e-7))
        pH_bq = -np.log10(bq(self.balance, a, b, maxiter=10000))

        #print('\n-----------------------------')
        #print("Der pH-Wert beträgt: {:.2f}".format(pH_bq))
        #print('-----------------------------')
        #print('-----------------------------')
        
        return pH_bq


    def balance(self, x):
        '''
        Berechnet die Werte für die Protonenbilanz, d.h.
        Summe starker und schwacher Säuren, sowie die 
        Summe der starken und schwachen Basen eines
        beliebigen Säure/Basen gemisches. Definirt 
        werden die Parameter mit der pH-Funktion.
        '''
        #print("pH-calls me")
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

        A = C_ac_s + C_ac + ((10**(-1*14))/x) - C_ba_s - C_ba - x
        #print("C_ac_s = {:.5f}".format(A))

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

        #print('-----------------------------')
        #print('Titration Function Input from GUI')
        #print('pH :',c_Acids, pKs_acids, c_Bases, pKs_bases, pKs_tit)
        #print('-----------------------------\n')
        
        ac = []
        pK_ac = []
        ba = []
        pK_ba = []
        
        ac = c_Acids[:]
        pK_ac = pKs_acids[:]
        ba = c_Bases[:]
        pK_ba = pKs_bases[:]
        pH_start = self.pH(input_string)
        pH = [pH_start]
        c_tit = 0

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
            while pH[loop] <= pH_end and loop <= 2000:
                b = [i for i in ba]
                b.append(c_tit)
                value = self.pH((ac, pK_ac, b, pK_ba))
                pH.append(value)

                loop += 1
                c_tit += step

        if modus == 'base':
            loop = 0
            while pH[loop] >= pH_end and loop <= 2000:
                a = [i for i in ac]
                a.append(c_tit)
                value = self.pH((a, pK_ac, ba, pK_ba))
                pH.append(value)

                loop += 1
                c_tit += step

        plt.plot(pH, alpha=0.5, linewidth=3)
        plt.grid(1)
        plt.ylabel('pH')
        plt.xlabel('index')
        plt.xlim(0, 2000)
        

        return  

                    
class solutions():
    '''
    Class contains a few tool to calculate some stuff
    like the mass which is needed to create a whished 
    solution.
    '''
    def __init__(self):
        pass

    def calc_mass(inputs):
        '''
        This function calculates the mass for a 
        desired solution
        '''
        Molmass = inputs[0]  # Molecular mass [g/mol]
        conc = inputs[1]     # Molar concentration [mol/L]
        Volume = inputs[2]   # Volume [L]

        # n = m/M
        # c = n/V
        # -> m = c*V*M
        mass = float(conc) * float(Volume) * float(Molmass)

        return '{:.4f}'.format(mass)

def test(A):
    '''
    Function to test connection to gui
    '''
    #print('parameters\n')
    
    a = A[0]
    if len(ast.literal_eval(A[1])) == 1:
        b = [[i] for i in ast.literal_eval(A[1])]
    else:
        b = [i for i in ast.literal_eval(A[1])]
    c = A[2]
    if len(ast.literal_eval(A[3])) == 1:
        d = [[i] for i in ast.literal_eval(A[3])]
    else:
        d = [i for i in ast.literal_eval(A[3])]
           
    print(a)
    print(b)
    print(c)
    print(d)

    return
