"""
Model script for R || C || (L + Rl)
"""

import numpy as np
from collections import OrderedDict

j = 1j

# Ordered dictionary of parameter names, initial guess values, and
# min/max bounds. Use +/-np.inf for unbounded, set min = max to
# fix a value.
PINIT = 0       # index to init_val
PBOUNDS = 1     # index to boundaries
BOUNDWEIGHT = 100
PARAMS = OrderedDict ([
    # name  init_val (min, max)
    ('R', (1e3, (0, np.inf))),
    ('C', (10e-12, (0, np.inf))),
    ('L', (1e-6, (0, np.inf))),
    ('Rl', (50e-3, (1e-3, np.inf))),
])

j = 1j

def model(w, params):
    """
    Calculate impedance using equations here for all frequencies w.
    :param w: radian frequency array
    :param params: list of component values to apply to the model equations
    :return: complex impedance array corresponding to freqs w
    """
    # Extract individual component values from params list
    R, C, L, Rl = params
    # This is the definition of the model impedance which we want to
    # fit to the data points.  Modify it to represent the circuit you
    # want to fit to the data.
    Zl = (j * w * L) + Rl
    Zc = 1/(j * w * C)
    Y = 1/R + 1/Zc + 1/Zl
    Z = 1 / Y
    return Z
