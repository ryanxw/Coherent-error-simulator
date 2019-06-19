from numpy import pi, sin, random
from scipy.optimize import fsolve

# -- Define error distribution --
# Gate error: 1 - cos(x) probability distribution
def func_gen(r):
    func = lambda x : x - sin(x) - 2 * pi * r
    return func

# -- Totally random distribution --
# err = max. single-qubit error rate
# Has to be called every time to randomize
def r(err):
    r = random.rand()
    func = func_gen(r)
    return 1 + err * (fsolve(func, pi)[0]/pi - 1)