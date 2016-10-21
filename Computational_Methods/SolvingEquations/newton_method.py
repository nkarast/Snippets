#
#   This script uses the newton method to find the root of an equation.
#
#   The newton method is:
#       Setup: Assume a function f, and its derivative f' = df/dx are known!
#       Step 1) Guess a point a and calculate f(a) and f'(a)
#       Step 2) Find the point b: Point b is the point when taking the slope (tangent) of the function f at
#               point a, the line crosses the x-axis (ie y(b)=0).
#                 f(a) = f'(a)(a-b) + 0  => b = a - f(a)/f'(a)
#
#       Step 3) Repeat with now starting point the point b until reach a tolerance
#
#
#
#      Newtwon's method is faster but it requires that you know the derivative.
#      Also it is affected by local minima and therefore it's not so robust

from math import *

# define my tolerance
tolerance = 1.e-6

# define my function:
def f(x):
    f = exp(x)*log(x)-x*x
    return f

# define its derivative
def df(x):
  df = -2*x + (exp(x)/x) + exp(x)*log(x)
  return df


# make a guess
guess = 4.


# define an initial distance (for iteration purposes)
dx = 2*tolerance

# loop trying to minimize the distance.
while dx > tolerance:
  new_guess = guess - f(guess)/df(guess)
  dx = abs(guess-new_guess)
  guess = new_guess

print "The solution is found at : x = %.8f +/- %0.8f " % (guess, tolerance)
