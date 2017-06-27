"""
Model script for R + (C|| (R))
"""
import numpy as np
from collections import OrderedDict

j = 1j
# Ordered dictionary of parameter names, initial guess values, and
# min/max bounds. Use +/-np.inf for unbounded, set min = max to
# fix a value
PINIT = 0       # index to init_val
PBOUNDS = 1     # index to boundaries
BOUNDWEIGHT = 6
PARAMS = OrderedDict([
    # name init_val (min,max)
    ('Rs',(1243,(1e-3,1e5))),
    ('C',(8e-7,(1e-7,1e-4))),
    ('Rf',(1e5,(1e4,1e6))),
])


def model(w,params):
     """
    Calculate impedance using equations here for all frequencies w.
    :param w: radian frequency array
    :param params: list of component values to apply to the model equations
    :return: complex impedance array corresponding to freqs w
    """
     # Extract individual component values from params list
     Rs,C,Rf = params
     # This is the definition of the model impedance which we want to
     #  fit to the data points.  Modify it to represent the circuit you
     #  want to fit to the data.
     # Zq = 1 / ( Yq * (1j * w)**n )
     Zc = 1 / (1j*w*C)
     # Zrw = Rf + Zw
     Yp = 1/Zc + 1/Rf
     Z = Rs + 1/Yp

     # print(Z)

     return Z
