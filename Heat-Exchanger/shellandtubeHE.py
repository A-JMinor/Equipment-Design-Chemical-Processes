# -*- coding: utf-8 -*-
"""
Created on Thu Jun  6 23:55:27 2024

@author: Ann-Joelle
"""



import numpy as np
import math



def estimate_tube_number(heat_transfer_area, tube_outer_diameter, length, n, min_tubes=20):
    """
    Estimate the number of tubes required to achieve a specified heat transfer area with a given tube diameter and a fixed length.

    Parameters:
    - heat_transfer_area (float): The total required heat transfer area (m^2).
    - tube_outer_diameter (float): The outer diameter of the tubes (m).
    - length (float): The fixed length of the tubes (m).
    - n (int): Maximum allowable number of tubes.
    - min_tubes (int): Minimum number of tubes typically needed for shell and tube heat exchangers, default is 20.

    Returns:
    - int: The estimated total number of tubes, adjusted for minimum practical limits unless only one tube is required.
    """
    # Calculate the surface area of one tube
    tube_surface_area_per_meter = math.pi * tube_outer_diameter
    tube_surface_area = tube_surface_area_per_meter * length  # Total surface area for the given length

    # Calculate the number of tubes needed to achieve the desired total heat transfer area
    total = math.ceil(heat_transfer_area / tube_surface_area)

    # Adjust the tube count based on specific requirements
    if total > 1 and total < min_tubes:
        total = min_tubes  # Set to minimum tubes if below threshold but more than one
    if total > n:
        return 0  # Return 0 if the total exceeds the maximum allowable number of tubes

    return total


def calculate_baffle_spacing(shell_diameter, baffle_cut_percentage):
    """
    Estimate the number of baffles and their spacing according to Kern's method.

    Parameters:
    - shell_diameter (float): Internal diameter of the shell (m).
    - baffle_cut_percentage (int): Percentage of baffle cut (%).

    Returns:
    tuple: Number of baffles and recommended baffle spacing (m).
    """
    # Calculate number of baffles
    num_baffles = max(0, round(shell_diameter / 0.9))  # Example correlation, adjust as needed

    # Calculate baffle spacing based on cut percentage and number of baffles
    if num_baffles > 0:
        baffle_spacing = shell_diameter / (num_baffles + (baffle_cut_percentage / 100))
    else:
        baffle_spacing = 0  # Set baffle spacing to 0 if there are no baffles

    return num_baffles, baffle_spacing




def calculate_shell_diameter(num_tubes, tube_outer_diameter, pitch_type='t', min_shell_diameter=0.15):
    """
    Calculates the shell diameter for a shell and tube heat exchanger, enforcing a minimum shell diameter.

    Parameters:
    num_tubes (int): Number of tubes in the heat exchanger.
    tube_outer_diameter (float): Outer diameter of each tube (in meters).
    pitch_type (str): Type of pitch ('t' for triangular, 's' for square).
    min_shell_diameter (float): Minimum shell diameter (in meters), default is 0.15 meters.

    Returns:
    float: Shell diameter (in meters), adjusted for minimum size.
    """
    # Set the pitch factor based on the pitch type
    if pitch_type == 't':
        pitch_factor = 1.1  # Typical for triangular pitch
    elif pitch_type == 's':
        pitch_factor = 1.25  # Typical for square pitch
    else:
        raise ValueError("Invalid pitch type. Use 't' for triangular or 's' for square.")

    # Calculate the pitch (center-to-center distance between tubes)
    pitch = tube_outer_diameter * pitch_factor

    # Calculate the approximate diameter of the tube bundle
    tube_bundle_diameter = math.sqrt((num_tubes * pitch**2) / math.pi)

    # Estimate the shell diameter (usually 30% larger than the tube bundle diameter)
    shell_diameter = tube_bundle_diameter * 1.3

    # Apply the minimum shell diameter rule
    shell_diameter = max(shell_diameter, min_shell_diameter)

    return shell_diameter


def calculate_shelltubeexchanger_weight(shell_diameter, tube_length, tube_outer_diameter, num_tubes, baffle_spacing, shell_thickness=0.0127, tube_thickness=0.00211, baffle_thickness=0.00635, shell_steel_density=7850, tube_steel_density=7850):
    """
    Calculates the approximate weight of a shell and tube heat exchanger, including consideration for the presence of baffles based on the provided baffle spacing.

    Parameters:
    shell_diameter (float): Diameter of the shell in meters.
    tube_length (float): Length of the tubes in meters.
    tube_outer_diameter (float): Outer diameter of the tubes in meters.
    num_tubes (int): Number of tubes.
    baffle_spacing (float): Spacing between baffles in meters.
    shell_thickness (float): Thickness of the shell in meters (default is typical for carbon steel).
    tube_thickness (float): Thickness of the tubes in meters (default is typical for standard carbon steel tubes).
    baffle_thickness (float): Thickness of the baffles in meters (default is typical thickness).
    shell_steel_density (float): Density of the shell side steel in kg/m^3 (default is 7850 for carbon steel).
    tube_steel_density (float): Density of the shell side steel in kg/m^3 (default is 7850 for carbon steel).

    Returns:
    float: Total weight of the heat exchanger in kilograms.
    """
    # Calculate shell volume
    shell_inner_diameter = shell_diameter - 2 * shell_thickness
    shell_volume = math.pi * (shell_diameter**2 - shell_inner_diameter**2) / 4 * tube_length

    # Calculate tube volume
    tube_inner_diameter = tube_outer_diameter - 2 * tube_thickness
    tube_volume = num_tubes * math.pi * (tube_outer_diameter**2 - tube_inner_diameter**2) / 4 * tube_length

    # Initialize baffle weight
    baffle_weight = 0

    # Determine if baffles are needed
    if baffle_spacing > 0 and baffle_spacing < tube_length:
        # Calculate baffle volume
        baffle_count = math.floor(tube_length / baffle_spacing)
        baffle_area = shell_inner_diameter * shell_inner_diameter * math.pi / 4
        baffle_volume = baffle_area * baffle_thickness * baffle_count

        # Calculate baffle weight
        baffle_weight = baffle_volume * shell_steel_density

    # Calculate weights
    shell_weight = shell_volume * shell_steel_density  + baffle_weight
    tube_weight = tube_volume * tube_steel_density

    # Total weight
    total_weight = shell_weight + tube_weight + baffle_weight

    return total_weight, shell_weight, tube_weight
