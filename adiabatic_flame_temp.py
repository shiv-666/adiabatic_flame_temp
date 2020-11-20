
# shivank joshi 11/17/20

from scipy.integrate import quad
from tkinter import *


welcome = """
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Iteratively finding flame temp given reaction info
Precision to within 1 Joule

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
"""




heat_capacities = '''
                
O2_low = (25.460, 1.519, -0.715, 1.311)
O2_high = (28.167, 0.630, -0.075)

H2O_low = (32.218, 0.192, 1.055, -3.593)
H2O_high = (29.163, 1.449, -0.202)

N2_high = (27.318, 0.623, -0.095)
'''


outs, goal = dict(), None

class chooseTings(object):

    def __init__(self, master):
        
        self.master = master
        master.title("Pick the things")

        self.title_txt = Label(master, text='enter all the mol of products and hit continue', font='16')
        self.title_txt.grid(row=0, columnspan=2, sticky='s')

        self.water_high = Entry(master, width=25, bg='#E8DFD8')
        self.water_high.grid(row=1, column=0)

        self.water_txt = Label(master, text='mol h2o high range', font='16')
        self.water_txt.grid(row=1, column=1, sticky='s')

        self.co2_high = Entry(master, width=25, bg='#E8DFD8')
        self.co2_high.grid(row=2, column=0)

        self.co2_txt = Label(master, text='mol co2 high range', font='16')
        self.co2_txt.grid(row=2, column=1, sticky='s')

        self.n2_high = Entry(master, width=25, bg='#E8DFD8')
        self.n2_high.grid(row=3, column=0)

        self.n2_txt = Label(master, text='mol n2 high range', font='16')
        self.n2_txt.grid(row=3, column=1, sticky='s')

        self.o2_high = Entry(master, width=25, bg='#E8DFD8')
        self.o2_high.grid(row=4, column=0)

        self.o2_txt = Label(master, text='mol o2 high range', font='16')
        self.o2_txt.grid(row=4, column=1, sticky='s')

        self.heat_combust = Entry(master, width=25, bg='#E8DFD8')
        self.heat_combust.grid(row=13, column=0)

        self.heat_combust_txt = Label(master, text='heat of products in kJ', font='16')
        self.heat_combust_txt.grid(row=13, column=1, sticky='s')

        self.continueButton = Button(master, text="Continue", font='8', command=self.save, width=15, height=1, background='#E8DFD8')
        self.continueButton.grid(row=14, column=1, sticky='w')

        self.closeButton = Button(master, text="Exit", font='8', command=self.quit, width=15, height=1, bg='#E8DFD8')
        self.closeButton.grid(row=14, column=0, sticky='s')
    
    def save(self):
        global outs, goal
        assert(outs == dict())
        try:  
            if self.water_high.get() != '':
                outs["H2O_high"] = float(self.water_high.get())
            if self.co2_high.get() != '':
                outs["CO2_high"] = float(self.co2_high.get())
            if self.n2_high.get() != '':
                outs["N2_high"] = float(self.n2_high.get())
            if self.o2_high.get() != '':
                outs["O2_high"] = float(self.o2_high.get())
        except:
            Exception("please only input number values")
        try:
            goal = float(self.heat_combust.get()) * 1000
        except:
            raise Exception("\nMust input a valid numerical heat of products")
        assert(outs != {} and isinstance(goal, float))
        self.master.destroy()

    def quit(self):
        self.master.destroy()


root = Tk()
chooseTings(root)
root.mainloop()

capacities = dict()
for line in heat_capacities.strip().splitlines():
    if line.isspace() or line == '': continue
    k = line.split(" ")[0]
    curr_string = line.split("=")[1].strip()
    curr = []
    for n in curr_string[1:-1].split(" "):
        if n[-1] == ',': n = n[:-1]
        try:
            curr.append(float(n))
        except:
            raise("data was not formatted correctly")
    capacities[k] = tuple(curr)

weighted_a, weighted_b, weighted_c, weighted_d, co2 = [0] * 5
for elem in outs:
    mols = outs[elem]
    if elem == "CO2_high":
        co2 = mols
        continue
    weighted_a += capacities[elem][0] * mols
    weighted_b += capacities[elem][1] * mols
    weighted_c += capacities[elem][2] * mols
    if len(capacities[elem]) > 3:
        weighted_d += capacities[elem][3] * mols
    
coeffs = (weighted_a, weighted_b * (10**-2), weighted_c * (10**-5), weighted_d * (10**-9), co2)

def cp(T, a, b, c, d, co2):
    fn = a + T*b + c*(T**2) + d*(T**3)
    fn += co2 * (-661.42/(T**0.5) + 75.464 - 1.872 * (10**-4) * T) 
    return fn

def iterate(guess, goal, coeffs):
    ans, inc = -1, 1
    while (abs(ans - goal) > 1):
        ans = quad(cp, 298, guess, args=(coeffs))[0]
        if (inc == 1 and abs(ans - goal) < 1000):
            inc = 0.0005
        elif (inc == .0005 and abs(ans - goal) < 1):
            inc = .0000005
        guess += inc
    return guess

def main():
    print(welcome)
    print("Calculating...\n")
    result = iterate(300, goal, coeffs)
    print("Adiabatic Flame Temp: %s" % result)

main()


