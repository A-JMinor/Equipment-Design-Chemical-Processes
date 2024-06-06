# -*- coding: utf-8 -*-
"""
Created on Thu Jun  6 23:39:49 2024

@author: Ann-Joelle
"""
import numpy as np

def vertical_vessels_weight(lowest_pressure, highest_temp, diameter, tangent_tangent_length, material_density):
    """
    Calculate the weight of a vertical chemical processing vessel based on provided parameters of pressure, temperature, dimensions, and material density.

    Parameters:
    - lowest_pressure (float): The minimum operating pressure of the tower in kilopascals (kPa).
    - highest_temp (float): The maximum operating temperature of the tower in Kelvin (K).
    - diameter (float): The diameter of the tower in meters (m).
    - tangent_tangent_length (float): The tangent-to-tangent length of the tower in meters (m).
    - material_density (float): The density of the material used to construct the tower in kilograms per cubic meter (kg/m3).

    Returns:
    - weight (float): The calculated weight of the tower in pounds (lbs), considering the thickness required for structural integrity under given operating conditions.

    Notes:
    - The function assumes that the calculations are based on the methodologies provided in "Seader et al.", a common reference for chemical process engineering.
    - The calculations involve converting SI units to Imperial units as required for specific engineering formulas.
    - The function checks for pressures and temperatures outside of acceptable ranges and adjusts calculations accordingly.

    Raises:
    - Warning messages are printed if the input parameters are out of the typical range for chemical processing equipment design.
    """
    
    # Constants for unit conversions
    kg_m3_to_lb_in3 = 0.000036127298147753
    m_to_inch = 39.3701
    kPa_to_psig = 0.145038
    kg_to_lb = 2.20462
    kPa_to_psig = 0.145038
    
    # Calculate design pressure based on lowest pressure
    if lowest_pressure <= 34.5: # in kPa
        design_pressure = 10.0 # in psig
    elif lowest_pressure <= 6895:
        design_pressure = np.exp(0.60608 + 0.91615 * np.log(lowest_pressure*kPa_to_psig) + 0.0015655*(np.log(lowest_pressure*kPa_to_psig))**2)
    elif lowest_pressure >= 6895:
        design_pressure = 1.1 * lowest_pressure*kPa_to_psig

    
    # Convert highest temperature from Kelvin to Fahrenheit and adjust
    design_temp = (highest_temp - 273.15) * 9/5 + 32.0 + 50.0 # in Fahrenheit
    
    # Determine modulus of elasticity based on design temperature
    if design_temp < 200.0:
        E_modulus = 30.2 * 10**6
    elif design_temp < 400.0:
        E_modulus = 29.5 * 10**6
    elif design_temp < 650.0:
        E_modulus = 28.3 * 10**6
    else:
        E_modulus = 26.0 * 10**6
    
    # Set allowable stress based on design temperature
    if design_temp <= 750:
        allowable_stress = 15000
    elif design_temp <= 800:
        allowable_stress = 14750
    elif design_temp <= 850:
        allowable_stress = 14200
    elif design_temp <= 900:
        allowable_stress = 13100
    else:
        print("Warning: Distillation design temperature is too high for wall thickness calculation")
    
    # Initial thickness guesses and error tolerance for iteration
    tE1 = 0.25
    error = 1
    
    # Wall thickness calculations
    if lowest_pressure >= 101:
        while abs(error) > 0.001:
            tE = 0.22 * (((diameter * m_to_inch) + tE1) + 18) * (tangent_tangent_length * m_to_inch)**2 / (allowable_stress * ((diameter * m_to_inch) + tE1)**2)
            error = (tE1 - tE) / tE1
            tE1 = tE
        tp = (design_pressure * (diameter * m_to_inch)) / (2 * allowable_stress - 1.2 * design_pressure)
        t_total = (tp + tE + tp) / 2
    elif lowest_pressure <= 101:
        while abs(error) > 0.001:
            tE = 1.3 * ((diameter * m_to_inch) + tE1) * ((design_pressure * (tangent_tangent_length * m_to_inch)) / (E_modulus * ((diameter * m_to_inch) + tE1)))**0.4
            error = (tE1 - tE) / tE1
            tE1 = tE
        check = tE / (diameter * m_to_inch)
        if check >= 0.05:
            print("Warning: The wall thickness does not pass the methods.")
        tEC = (tangent_tangent_length * m_to_inch) * (0.18 * (diameter * m_to_inch) - 2.2) * 10**(-5) - 0.19
        if tEC > 0:
            t_total = tEC + tE + 0.125  # Adding corrosive allowance
        else:
            t_total = tE + 0.125  # Adding corrosive allowance

    # Ensure minimum wall thickness
    if t_total < 0.25:
        t_total = 0.25
    
    # Calculate total weight
    weight = np.pi * t_total * (material_density * kg_m3_to_lb_in3) * ((diameter * m_to_inch) + t_total) * ((tangent_tangent_length * m_to_inch) + 0.8 * (diameter * m_to_inch))
    
    weight = weight / kg_to_lb
    
    return weight
