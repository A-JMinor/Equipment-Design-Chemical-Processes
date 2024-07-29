# -*- coding: utf-8 -*-
"""
Created on Mon Jul 29 2024

@author: Ann-Joelle
"""

import math


def gas_liquid_separator_sizing(rho_vapor, rho_liquid, gas_flowrate, liquid_flowrate, viscosity_gas, h_d_ratio=3, D_sphere=0.0001):
    """
    Calculate the key properties of a gas-liquid separator, including the diameter and volume of the vessel,
    the hold-up time of the liquid within the vessel, and the gas velocity through the vessel. The calculations
    are based on ensuring effective phase separation under given flow conditions and physical properties of the
    involved fluids.

    Parameters:
    - rho_vapor (float): Density of the vapor phase (kg/m^3).
    - rho_liquid (float): Density of the liquid phase (kg/m^3).
    - gas_flowrate (float): Volumetric flow rate of the gas (m^3/s).
    - liquid_flowrate (float): Volumetric flow rate of the liquid (m^3/s).
    - viscosity_gas (float): Dynamic viscosity of the gas (Pa.s).
    - h_d_ratio (float, optional): Height-to-diameter ratio of the vessel. Defaults to 3.
    - D_sphere (float, optional): Critical diameter of the liquid droplets, doplets with smaller diameter than that 
        might not be separated but come with the gas (m). Defaults to 0.0001 m.

    Returns:
    - D_vessel: Diameter of the vessel (m)
    - D_volume: Volume of the vessel (m^3)
    - hold_up_time: Hold-up time (hours)
    - gas_velocity: Gas velocity in the vessel (m/s)

    Theory and Calculations:
    1. Terminal Velocity: The terminal velocity of droplets is crucial to ensure that the droplet can settle
       and be separated from the gas phase. It is calculated based on the modified Stokes' law which considers
       the effect of droplet diameter, and density differences between phases, under the influence of gravity.

    2. Separator Sizing: The diameter of the separator is sized to ensure that the gas velocity is less than
       the terminal velocity of the droplets. This is to prevent entrainment of the liquid droplets with the
       exiting gas and is based on the premise that lower gas velocities promote better phase separation.

    3. Hold-up Time: The hold-up time reflects the residence time of the liquid within the separator and is
       based on an assumed 60% of the total volume being occupied by the liquid. This metric is useful for
       assessing the efficiency of the separation process.
       
    4. D_sphere: The choice of D_sphere is instrumental in defining the smallest size of liquid droplets
      targeted for separation. A smaller D_sphere value increases the separation's effectiveness but also demands
      more precise and potentially costly equipment because of increasing equipment diameter and volume. Smaller values indicate
      that smaller droplets are targeted for removal, implying more stringent separation requirements. Typically,
      for water-like liquids, a droplet diameter of 0.0001m is used. For more viscous liquids, a larger diameter may
      still ensure efficient and effective separation.

    """
    
    g = 9.81  # gravitational acceleration in m/s^2

    # Calculate the terminal velocity 
    D_stern = D_sphere * (rho_vapor * (rho_liquid - rho_vapor) * g / viscosity_gas**2)**(1/3)
    u_t_stern = (18 / D_stern**2 + 0.591 / D_stern**0.5)**-1
    u_t = u_t_stern * (rho_vapor**2 / (viscosity_gas * (rho_liquid - rho_vapor) * g))**(-1/3)

    # Calculate the vessel diameter by setting gas velocity equal to terminal velocity
    D_vessel = (4 * gas_flowrate / (math.pi * u_t))**(1/2)

    # Calculate the actual gas velocity
    gas_velocity = 4 * gas_flowrate / (math.pi * D_vessel**2)

    # Calculate the length of the vessel based on the height-to-diameter ratio
    D_length = h_d_ratio * D_vessel

    # Calculate the volume of the vessel
    D_volume = math.pi / 4 * D_vessel**2 * D_length

    # Calculate the hold-up time based on the volume of the reactor occupied by liquid (assuming 10% liquid volume)
    hold_up_time = (math.pi * (0.1 * D_length) * D_vessel**2 ) / (4 * liquid_flowrate) / 3600  # converted to hours

    return D_vessel, D_volume, hold_up_time, gas_velocity


