"""
Model script for a segmented transmission line with skin effect
and arbitrary complex load termination.
See LTspice schematic for one segment in ./Data/LineSegment.asc
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
    ('Lpm',  (700e-9, (10e-9, 1e-6))),
    ('Lspm', (200e-9, (10e-9, 1e-6))),
    ('Rpm',  (400e-3, (100e-3, 800e-3))),
    ('Cpm',  (40e-12, (20e-12, 100e-12))),
    ('Gpm',  (1e-6, (10e-9, 10e-6)))
])


def model(w, params):
    """
    Model an arbitrary load impedance at the end of a cable.
    :param w: radian frequency array
    :param params: list of per-meter component values to apply to the 
                    model equations
    :return: complex impedance array corresponding to freqs w
    """
    # Length of cable in meters
    LENGTH = 3.0
    # Integer number of segments to split cable into
    SEGMENTS = 6
    # Skin effect parallel L/R branches
    BRANCHES = 5
    def load_z(w):
        """
        Define the load impedance at the cable end.
        :param w: radian frequency array
        :return: complex impedance array corresponding to w.
        """
        # For load of (92.2 ohms||820.9pF) + 69.16nH
        # Yl = 1.0/92.2 + 1j*w*820.9e-12   # Bc is positive
        # Zl = 1.0/Yl + 1j*w*69.16e-9      # Xl is positive
        # For fixed load
        Zl = np.full(len(w), 49.9 + 1j*0.0, dtype='complex')
        return Zl

    def segment_z(Zl, w, Lps, Lsps, Rps, Cps, Gps):
        """
        Return impedance array of a cable segment
        See LTspice schem ".\Data\LineSegment.asc"
        :param Zl: load impedance to this segment
        :param w: radian frequency array
        :param Lps: series inductance per segment
        :param Lsps: skin inductance per segment
        :param Rps: series resistance per segment
        :param Cps: shunt capacitance per segment
        :param Gps: shunt conductance per segment
        """
        dL = Lps / 2.0
        dLs = Lsps / 2.0
        dR = Rps / 2.0
        dC = Cps
        dG = Gps
        # Branch factors
        bf = [10**(x/2.0) for x in range(BRANCHES)]
        Ys = np.zeros(len(w), dtype='complex')
        # For each skin effect branch:
        for factor in bf:
            Lb = dLs / factor
            Xb = np.array(1j * w * Lb)
            Rb = dR * factor
            Zb = Rb + Xb
            Ys += 1.0 / Zb
        # Total skin effect impedance
        Zskin = 1.0 / Ys
        # "Termination Z" is load in series with skin effect and incremental L
        Zt = Zl + Zskin + 1j*w*dL
        # "Shunt Z" is parallel combination of Zt and incremental C and G
        Zs = 1.0/(1.0/Zt + 1j*w*dC + dG)
        # Total segment Z is Zs in series with skin effect and incremental L
        return Zs + Zskin + 1j*w*dL

    # Get per-segment values from parameter list
    Lps, Lsps, Rps, Cps, Gps = [x * LENGTH / SEGMENTS for x in params]
    # Initialize Z array (don't just refer to it)
    Zmod = load_z(w) + 0.0
    # Iterate cable segments, supplying previous Zmod as load to each iteration
    for s in range(SEGMENTS):
        Zmod = segment_z(Zmod, w, Lps, Lsps, Rps, Cps, Gps)
    # Return impedance
    return Zmod
