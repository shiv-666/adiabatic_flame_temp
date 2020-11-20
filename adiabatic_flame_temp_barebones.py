from scipy.integrate import quad

welcome = """
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Iteratively finding flame temp given reaction info
Precision to within 1 Joule
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
"""

a = 1
b = 1 * (10**-2)
c = 1 *(10**-5)
heat_products = 1322960 # in J
# don't include the 661/sqrt(T) term for co2
co2 = False # number of mol co2 coming out or false if no co2





def cp(T, a, b, c, d=0, co2=False):
    fn = a + T*b + c*(T**2) + d*(T**3)
    if co2:
        fn += co2 * -661.42/(T**0.5)
    return fn

def iterate(guess, goal, product_capacities):

    guess, ans, inc = 300, -1, 1
    while (abs(ans - goal) > 1):
        ans = quad(cp, 298, guess, args=(a, b, c, 0, 2))[0]
        if (inc == 1 and abs(ans - goal) < 1000):
            inc = 0.0005
        elif (inc == .0005 and abs(ans - goal) < 1):
            inc = .0000005
        guess += inc
    return guess

def main():
    print(welcome)
    print("Calculating...")
    result = iterate(300, heat_products, '')
    print("Adiabatic Flame Temp: %s" % result)

main()