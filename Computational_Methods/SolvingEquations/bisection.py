#
#   This script uses the bisection method to find the root of an equation.
#
#   The bisection method is:
#       Setup: Assume a function f, with one root.
#       Step 1) Guess two points a,b that are on either side of the root (That's important! They must be on
#               on the two sides of the root.
#       Step 2) Take the half point, x, between a and b.
#       Step 3) Calculate f(a), f(b), f(x)
#       Step 4) if f(a)*f(x) > 0:  # ie they have the same sight
#                     the root must be to the right of x
#                      set x = a
#               if f(a)*f(x)<0: #they have opposite signs
#                       the root must be between left of x
#                       set x=b
#       Step 5) Take the mid-point, x between the "new" a,b
#       Step 6) Repeat until a tolerence is achieved


from math import *
import matplotlib.pyplot as plt
import sympy as sp
#
#   Assume the function is f(x) = exp(x)*ln(x)-x*x = 0
#

# let's plot it to check the solution...
#x = sp.Symbol('x', real=True)
#pl = sp.plot(sp.exp(x)*sp.ln(x)-x*x,(x,1,2))


# define my tolerance
tolerance = 1.e-6

# define my function:
def f(x):
    f = exp(x)*log(x)-x*x
    return f

# Initial guesses:
#a,b = input("Enter two guesses separated by comma ',' : ")
a, b = 1,100


# Get my length
dx = abs(b-a)

# Go into a loop where the difference between the two guesses is less than my tolerance
while dx>tolerance:
    x = (a+b)/2.  # calculate mid point

    if (f(a)*f(x))<0.:
        b=x
    else:
        a = x

    dx = abs(b-a)

print "The solution is found at : x = %.8f +/- %0.8f " % (x, tolerance)