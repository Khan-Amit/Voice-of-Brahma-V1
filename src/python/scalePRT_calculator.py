# scalePRT_calculator.py
# scalePRT (Room‑Temperature Planck Length Scale)
# Part of Voice-of-Brahma-V1
# Author: Seliim Ahmed
# All Rights Reserved ®

import math

# Physical constants
BOLTZMANN = 1.380649e-23  # J/K
PLANCK = 6.62607015e-34   # J·s
C = 299792458             # m/s
ELEMENTARY_CHARGE = 1.602176634e-19  # C

def calculate_scalePRT(resonance_width_Hz, temperature_K=300.0, laser_wavelength_m=780e-9):
    """
    Calculate scalePRT from measured resonance curve parameters.

    Parameters:
        resonance_width_Hz (float): Full width at half maximum (FWHM) in Hz.
        temperature_K (float): Temperature in Kelvin (default 300 K).
        laser_wavelength_m (float): Laser wavelength in meters (default 780 nm).

    Returns:
        dict: Contains scalePRT in meters, equivalent time, energy per bit.
    """
    # Energy dissipation per bit (Landauer limit)
    E_landauer = BOLTZMANN * temperature_K * math.log(2)  # J

    # Energy associated with resonance width (quantum)
    E_resonance = PLANCK * resonance_width_Hz  # J

    # Ratio: how close we are to the Landauer limit
    ratio = E_landauer / E_resonance if E_resonance > 0 else float('inf')

    # scalePRT: effective Planck length derived from resonance
    # Based on: scalePRT = (lambda / (2*pi)) * (E_landauer / E_resonance) / log2(3)
    # This is a definition consistent with the paper.
    if E_resonance > 0:
        scalePRT_m = (laser_wavelength_m / (2 * math.pi)) * (E_landauer / E_resonance) / math.log2(3)
    else:
        scalePRT_m = float('inf')

    # Equivalent time: time it takes light to travel scalePRT
    scalePRT_s = scalePRT_m / C if scalePRT_m != float('inf') else float('inf')

    return {
        'scalePRT_m': scalePRT_m,
        'scalePRT_s': scalePRT_s,
        'energy_per_bit_J': E_landauer,
        'energy_per_bit_eV': E_landauer / ELEMENTARY_CHARGE,
        'resonance_energy_J': E_resonance,
        'ratio_to_landauer': ratio,
        'temperature_K': temperature_K,
        'laser_wavelength_m': laser_wavelength_m
    }

def resonance_width_to_scalePRT(fwhm_Hz, temperature=300.0, wavelength=780e-9):
    """
    Simplified wrapper for calculate_scalePRT.
    Returns the scalePRT value in meters.
    """
    result = calculate_scalePRT(fwhm_Hz, temperature, wavelength)
    return result['scalePRT_m']

# Example usage
if __name__ == "__main__":
    # Typical resonance width from U‑bottom groove at room temperature
    fwhm = 41.7e3  # 41.7 kHz (from paper)
    result = calculate_scalePRT(fwhm, 300.0, 780e-9)
    print("scalePRT calculation:")
    for k, v in result.items():
        if isinstance(v, float):
            if v > 1e-10:
                print(f"  {k}: {v:.6e}")
            else:
                print(f"  {k}: {v:.6e} (scientific)")
        else:
            print(f"  {k}: {v}")
