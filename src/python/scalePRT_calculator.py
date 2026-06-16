# scalePRT_calculator.py
# All Rights Reserved ® Seliim Ahmed

import math

BOLTZMANN = 1.380649e-23
PLANCK = 6.62607015e-34
C = 299792458
ELEMENTARY_CHARGE = 1.602176634e-19

def compute_scalePRT(fwhm_hz: float, temp_k: float = 300.0, wavelength_m: float = 780e-9) -> dict:
    """
    Compute scalePRT (groove coupling length) from resonance curve.
    """
    if fwhm_hz <= 0:
        return {'error': 'FWHM must be positive'}

    E_land = BOLTZMANN * temp_k * math.log(2)
    E_res = PLANCK * fwhm_hz
    ratio = E_land / E_res
    log2_3 = math.log2(3)
    scale = (wavelength_m / (2 * math.pi)) * ratio / log2_3

    return {
        'scalePRT_m': scale,
        'scalePRT_nm': scale * 1e9,
        'ratio_to_landauer': ratio,
        'resonance_energy_j': E_res,
        'resonance_energy_ev': E_res / ELEMENTARY_CHARGE,
        'landauer_energy_j': E_land,
        'fwhm_hz': fwhm_hz,
        'temperature_k': temp_k
    }

def build_energy_matrix(fwhm_list=None, temp_k=300):
    if fwhm_list is None:
        fwhm_list = [1000, 5000, 10000, 20000, 41700, 50000, 100000]
    return {f: compute_scalePRT(f, temp_k) for f in fwhm_list}

def build_scale_matrix(fwhm_list=None, temp_k=300, wavelength_m=780e-9):
    if fwhm_list is None:
        fwhm_list = [1000, 5000, 10000, 20000, 41700, 50000, 100000]
    return {f: compute_scalePRT(f, temp_k, wavelength_m) for f in fwhm_list}
