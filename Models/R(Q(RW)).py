"""
Model script for R + (Q || (R + W))
"""
import numpy as np
from collections import OrderedDict

j = 1j
# Ordered dictionary of parameter names, initial guess values, and
# min/max bounds. Use +/-np.inf for unbounded, set min = max to
# fix a value
PINIT = 0       # index to init_val
PBOUNDS = 1     # index to boundaries
BOUNDWEIGHT = 10
PARAMS = OrderedDict([
    # name init_val (min,max)
    ('Rs',(490,(1,1e3))),
    ('Yq',(3.6e-6,(1e-7,1e-5))),
    ('n',(0.8,(0.5,1))),
    ('Rf',(1e5,(1e4,1e6))),
    ('W',(5e3,(1,1e6))),
])


def model(w,params):
     """
    Calculate impedance using equations here for all frequencies w.
    :param w: radian frequency array
    :param params: list of component values to apply to the model equations
    :return: complex impedance array corresponding to freqs w
    """
     # Extract individual component values from params list
     Rs,Yq,n,Rf,W = params
     # This is the definition of the model impedance which we want to
     #  fit to the data points.  Modify it to represent the circuit you
     #  want to fit to the data.
     # Zq = 1 / ( Yq * np.float_power((1j * w),n) )
     Zq = np.divide(1,( Yq * np.float_power((1j * w),n) ))
     Zw = W * w**(-0.5) * (1-j)
     Zrw = Rf + Zw
     Yp = 1/Zq + 1/Zrw
     Z = Rs + 1/Yp
     # Z = Rs + ( Yq * np.float_power((1j * w),n) ) + 1/Zrw
     # print(Z)

     return Z
