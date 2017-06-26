"""
Model script for 2-resonance transducer model: 
(C1 + R1) || (C2 + R2 + L2) || (C3 + R3 + L3)
"""

import numpy as np
from collections import OrderedDict

j = 1j

# Ordered dictionary of parameter names, initial guess values, and
# min/max bounds. Use +/-np.inf for unbounded, set min = max to
# fix a value.
PINIT = 0       # index to init_val
PBOUNDS = 1     # index to boundaries
BOUNDWEIGHT = 1
PARAMS = OrderedDict ([
    # name  init_val (min, max)
    ('R1', (100,     (10, 1e3))),
    ('C1', (200e-12, (10e-12, 1e-9))),
    ('R2', (100,     (10, 1e3))),
    ('C2', (200e-12, (10e-12, 1e-9))),
    ('L2', (36e-6,   (1e-6, 100e-6))),
    ('R3', (20,      (1, 1e3))),
    ('C3', (300e-12, (10e-12, 1e-9))),
    ('L3', (20e-6,   (1e-6, 100e-6)))
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
    R1, C1, R2, C2, L2, R3, C3, L3 = params
    # This is the definition of the model impedance which we want to
    # fit to the data points.  Modify it to represent the circuit you
    # want to fit to the data.
    # (series R1, C1) || (series R2, C2, L2) || (series R3, C3, L3)
    Z1 = R1 + 1 / (j * w * C1)
    Z2 = R2 + 1 / (j * w * C2) + j * w * L2
    Z3 = R3 + 1 / (j * w * C3) + j * w * L3
    Z = 1 / (1 / Z1 + 1 / Z2 + 1 / Z3)
    return Z
