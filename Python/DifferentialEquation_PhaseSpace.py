#
#	Python function to solve and plot the phase space of
#	a simple oscillator
#

import sympy as sym
from sympy import pprint

# Def
t = sym.Symbol('t')
k = sym.Symbol('k', real=True, positive=True)

x = sym.Function('x')

de = sym.diff(x(t), t, t) +k*x(t)
de = sym.Eq(de)
sym.pprint(de)

solut = sym.dsolve(de, x(t))


sym.pprint(solut)





#
#	WORKAROUND TO GET INITIAL CONDITIONS
#
#solut_variables = solut.atoms(sym.Symbol) # this holds the set of symbols
										  # in the solut (solution of ODE)

#C1C2_consts = solut.atoms(sym.Symbol).difference(de.atoms(sym.Symbol))
#c1 = C1C2_consts.pop(0)
#print c1






# import numpy as np
# import sympy as sp
# from sympy.physics import units as u
# from sympy import *
# from IPython.display import *
# init_printing(use_latex=True)

# g = sp.Symbol('g', real=True)
# L = sp.Symbol('L', real=True)
# A = sp.Symbol('A', real=True)
# w = sp.Symbol('w', real=True)
# t = sp.Symbol('t', real=True)
# x = sp.Symbol('x', cls=Function)

# g = 10.0 * u.meters/u.seconds**2
# L = 5 * u.meters
# #A = 15 * u.meters
# w.is_real


# ## Define the differential equation of the problem:

# myeq = Eq(x(t).diff(t,t) + w*x(t))
# display(myeq)

# des = dsolve(myeq, x, ics={x(0):5.})
# display(des)