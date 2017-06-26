"""
Model script for a segmented transmission line with 
arbitrary complex load termination.  Each segment 
is a T with 1/2 LR in series in the top branches and 
CG in shunt between them.
"""

import numpy as np
from collections import OrderedDict

j = 1j

# Ordered dictionary of parameter names, initial guess values, and
# min/max bounds. Use +/-np.inf for unbounded, set min = max to
# fix a value.
PINIT = 0
PBOUNDS = 1
BOUNDWEIGHT = 1e5
PARAMS = OrderedDict([
    # name   init_val (min, max)
    ('Lpm',  (700e-9, (600e-9, 1e-6))),
    ('Rpm',  (1, (700e-3, 1.5))),
    ('Cpm',  (40e-12, (40e-12, 70e-12))),
    ('Gpm',  (40e-12, (40e-12, 70e-12))),
])


def model(w, params):
    """
    Model an arbitrary load impedance at the end of a cable.
    :param w: radian frequency array
    :param params: list of per-meter component values to apply to the 
                    model equations
    :return: complex impedance array corresponding to w
    """
    # Length of cable in meters
    LENGTH = 3.0
    # Integer number of segments to split cable into
    SEGMENTS = 3
    def load_z(w):
        """
        Define the load impedance at the cable end.
        :param w: radian frequency array
        :return: complex impedance array corresponding to w.
        """
        # For load of (92.2 ohms||820.9pF) + 69.16nH
        # Yl = 1.0/92.2 + 1j*w*820.9e-12   # Bc is positive
        # Zl = 1.0/Yl + 1j*w*69.16e-9      # Xl is positive
        # For fixed 49.9 ohm load
        Zl = np.full(len(w), 49.9 + 1j*0.0, dtype='complex')
        return Zl

    def segment_z(Zl, w, Lps, Rps, Cps, Gps):
        """
        Return impedance array of a cable segment
        :param Zl: load impedance to this segment
        :param w: radian frequency array
        :param Lps: series inductance per segment
        :param Rps: series resistance per segment
        :param Cps: shunt capacitance per segment
        """
        # Half of series leg
        Zleg = 1j*0.5*w*Lps + 0.5*Rps
        # Termination Z in series with half of series elements
        Zt = Zl + Zleg
        # Now in parallel with segment C and G
        Yt = 1.0/Zt + 1j*w*Cps + Gps     # Bc is positive
        # In series with remainder of series elements
        Zt = 1.0/Yt + Zleg
        return Zt

    # Get per-segment values from parameter list
    Lps, Rps, Cps, Gps = [x * LENGTH / SEGMENTS for x in params]
    # Initialize Z array (don't just refer to it)
    Zmod = load_z(w) + 0.0
    # Iterate cable segments, supplying previous Zmod as load to each iteration
    for s in range(SEGMENTS):
        Zmod = segment_z(Zmod, w, Lps, Rps, Cps, Gps)
    # Return impedance
    return Zmod
