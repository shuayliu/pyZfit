import numpy as np
from scipy.optimize import leastsq

"""
Core modeling functions common to all modeling scripts

Two types of weighting are applied here:
1. Boundary weighting, applied when a param exceeds the (min, max) boundaries spec'd
   in the PARAMS dictionary.  The BOUNDWEIGHT constant defines the amount of penalty
   to be applied when a param goes outside its boundary.  This helps to constrain
   the optimizer to finding solutions with params within the spec'd boundaries.
2. Model weighting, which is used to obtain closer model fitting in specified
   frequency regions.  This weighting is applied graphically from the main GUI.

This module makes several references to objects in the model script, but to avoid
duplicating it in each model it is made into a separate module here.  The linkage is
as follows:
1. This module is imported in Zfit when it is first loaded
2. The module script is dynamically reloaded in Zfit every time Model is clicked
3. Zfit dynamically assigns the unresolved references from this module to the model.
   This allows this module to access the model as required.
"""

def _residuals(params, w, Z, m_weight):
    """
    This is the error function minimized by leastsq.  It should return the
    difference between the model and the data, not the square.
    :param params: tuple of variables to supply to model()
    :param w: radian frequency array
    :param Z: impedance data to match
    :return:
    """
    # Get difference between model and target, apply modeling weight
    diff = Z - model(w, params)
    diff *= m_weight
    diff.astype(np.complex128)
    # Split complex result into real & imag parts to minimize both
    zd = np.zeros(Z.size*2, dtype=np.float64)
    zd[0:zd.size:2] = diff.real.astype(np.float64)
    zd[1:zd.size:2] = diff.imag.astype(np.float64)
    return zd

def _penalties(params, bounds, b_weight):
    # Build an array with number of parameters elements, 0 if the
    # parameter is within bounds and how far out if not:
    penalties = [np.fmin(x-lo, 0) + np.fmax(0, x-hi) for x, (lo, hi) in zip(params, bounds)]
    # Scale for how much it should hurt if you're out of bounds
    return b_weight * np.array(penalties)


def _b_residuals(params, w, Z, m_weight, bounds, b_weight):
    """
    Create array of residuals including "penalty" elements when parameter
    min/max limits are exceeded.
    :param params: parameters adjusted to fit
    :param w: radian frequency array
    :param Z: target complex impedance array
    :return: array of residuals plus penalties
    """
    ba = np.hstack((_residuals(params, w, Z, m_weight), _penalties(params, bounds, b_weight)))
    return ba


def fit_model(Z, m_weight, f):
    """
    Entry point to fit model to impedance data Z over frequency range f
    :param Z: impedance array to fit
    :param m_weight: array of modeling weights to apply to residuals
    :param f: Hz frequency array
    :return: output from leastsq, see
    http://docs.scipy.org/doc/scipy-0.14.0/reference/generated/scipy.optimize.leastsq.html
    """
    # Convert f to angular freq
    w = 2 * np.pi * f
    # Extract the guess values out of the PARAMS values tuple
    init_val = [elem[PINIT] for elem in PARAMS.values()]
    # Extract bounds list of tuples from PARAMS values tuple
    bounds = [elem[PBOUNDS] for elem in PARAMS.values()]
    # Scale penalty weight by number of residual samples
    b_weight = len(w) * BOUNDWEIGHT
    return leastsq(_b_residuals, init_val, args=(w, Z, m_weight, bounds, b_weight),
                   full_output=True, maxfev=1000000,ftol=1e-12,factor=0.1)
