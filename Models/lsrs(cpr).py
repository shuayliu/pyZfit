"""
Model script for Ls + Rs + (Cp || Rp)
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
    ('Ls', (200e-9, (0, np.inf))),
    ('Rs', (500e-3, (0, np.inf))),
    ('Cp', (1e-9, (1e-12, np.inf))),
    ('Rp', (200, (0, np.inf))),
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
    Ls, Rs, Cp, Rp = params
    # This is the definition of the model impedance which we want to
    # fit to the data points.  Modify it to represent the circuit you
    # want to fit to the data.
    Ycp = (j * w * Cp) + 1/Rp
    Z = 1/Ycp + (j * w * Ls) + Rs
    return Z
