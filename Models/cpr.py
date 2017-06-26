"""
Model script for C || R
"""

import numpy as np
from collections import OrderedDict

# Ordered dictionary of parameter names, initial guess values, and
# min/max bounds. Use +/-np.inf for unbounded, set min = max to
# fix a value.
PINIT = 0       # index to init_val
PBOUNDS = 1     # index to boundaries
BOUNDWEIGHT = 1e10
PARAMS = OrderedDict ([
    # name  init_val (min, max)
    ('R', (1e3, (0, np.inf))),
    ('C', (10e-12, (1e-12, np.inf)))
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
    R, C = params
    # This is the definition of the model impedance which we want to
    # fit to the data points.  Modify it to represent the circuit you
    # want to fit to the data.
    Y = 1.0/R + (1j * w * C)
    return 1.0 / Y
