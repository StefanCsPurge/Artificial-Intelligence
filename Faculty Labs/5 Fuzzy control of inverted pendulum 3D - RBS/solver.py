# -*- coding: utf-8 -*-
"""
In this file your task is to write the solver function!
"""


def solver(t,w):
    """
    Parameters
    ----------
    t : TYPE: float
        DESCRIPTION: the angle theta
    w : TYPE: float
        DESCRIPTION: the angular speed omega

    Returns
    -------
    F : TYPE: float
        DESCRIPTION: the force that must be applied to the cart
    or
        None :if we have a division by zero
    """
    theta = {"NVB": [-50, -25, -40],
             "NB": [-40, -10, -25],
             "N": [-20, 0, -10],
             "ZO": [-5, 5, 0],
             "P": [0, 20, 10],
             "PB": [10, 40, 25],
             "PVB": [25, 50, 40]}

    omega = {"NB": [-10, -3, -8], "N": [-6, 0, -3], "ZO": [-1, 1, 0], "P": [0, 6, 3], "PB": [3, 10, 8]}

    products = {'NVVB': -32, 'NVB': -24, 'NB': -16, 'N': -8, 'Z': 0, 'P': 8, 'PB': 16, 'PVB': 24, 'PVVB': 32}

    force = {'NVB+NB': 'NVVB',
             'NVB+N': 'NVVB',
             'NVB+ZO': 'NVB',
             'NVB+P': 'NB',
             'NVB+PB': 'N',
             'NB+NB': 'NVVB',
             'NB+N': 'NVB',
             'NB+ZO': 'NB',
             'NB+P': 'N',
             'NB+PB': 'Z',
             'N+NB': 'NVB',
             'N+N': 'NB',
             'N+ZO': 'N',
             'N+P': 'Z',
             'N+PB': 'P',
             'ZO+NB': 'NB',
             'ZO+N': 'N',
             'ZO+ZO': 'Z',
             'ZO+P': 'P',
             'ZO+PB': 'PB',
             'P+NB': 'N',
             'P+N': 'Z',
             'P+ZO': 'P',
             'P+P': 'PB',
             'P+PB': 'PVB',
             'PB+NB': 'Z',
             'PB+N': 'P',
             'PB+ZO': 'PB',
             'PB+P': 'PVB',
             'PB+PB': 'PVVB',
             'PVB+NB': 'P',
             'PVB+N': 'PB',
             'PVB+ZO': 'PVB',
             'PVB+P': 'PVVB',
             'PVB+PB': 'PVVB'}  # the rules for the fuzzy system

    miuTheta = {}  # membership degrees for theta (grade de apartenenta)

    for key in theta:
        miuTheta[key] = 0
        if theta[key][0] <= t <= theta[key][1]:
            try:  # formula
                miuTheta[key] = max(0, min((t - theta[key][0]) / (theta[key][2] - theta[key][0]), 1,
                                           (theta[key][1] - t) / (theta[key][1] - theta[key][2])))
            except ZeroDivisionError:
                pass

    miuOmega = {}  # membership degrees for omega
    for key in omega:
        miuOmega[key] = 0
        if omega[key][0] <= w <= omega[key][1]:
            try:
                miuOmega[key] = max(0, min((w - omega[key][0]) / (omega[key][2] - omega[key][0]), 1,
                                           (omega[key][1] - w) / (omega[key][1] - omega[key][2])))
            except ZeroDivisionError:
                pass

    # print(miuTheta)
    # print(miuOmega)

    forces = {}
    for key in theta:
        for key_2 in omega:
            # for each cell in the rule table we take the minimum of the membership values of the index set
            val = min(miuTheta[key], miuOmega[key_2])
            new_key = str(key) + '+' + str(key_2)
            # The membership degree of F to each class will be the maximum value for that class taken
            # from the rules’ table
            if force[new_key] not in forces:
                forces[force[new_key]] = val
            elif val > forces[force[new_key]]:
                forces[force[new_key]] = val

    # print(forces)
    # defuzzify the results for F using a weighted average of the membership degrees and the b values of the sets
    f_sum = 0
    products_sum = 0
    for key in forces:
        f_sum += forces[key]
        products_sum += forces[key] * products[key]

    try:
        force = products_sum / f_sum
    except ZeroDivisionError:
        force = None

    return force  # traction force

