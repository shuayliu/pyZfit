"""
Model script for L + Rdc plus skin effect
"""

import numpy as np
from collections import OrderedDict

j = 1j

# Ordered dictionary of parameter names, initial guess values, and
# min/max bounds. Use +/-np.inf for unbounded, set min = max to
# fix a value.
PINIT = 0       # index to init_val
PBOUNDS = 1     # index to boundaries
BOUNDWEIGHT = 1000
PARAMS = OrderedDict ([
    # name  init_val (min, max)
    ('L', (1e-6, (0, np.inf))),
    ('Rdc', (100e-3, (0, np.inf))),
    ('s', (1e-3, (0, np.inf))),
])

j = 1j

def model(w, params):
    """
    Calculate impedance using equations here for all frequencies w.
    :param w: radian frequency array
    :param params: list of component values to apply to the model equations
    :return: complex impedance array corresponding to freqs w
    """
    # Extract individual component values from params list, in the same
    # order as defined in PARAMS above
    L, Rdc, s = params
    # This is the definition of the model impedance which we want to
    # fit to the data points.  Modify it to represent the circuit you
    # want to fit to the data.
    Z = (j * w * L) + Rdc + (s * np.sqrt(w))
    return Z
