import numpy as np

def square(point, side, alpha = 0):
    sq = side * np.array([[0, 0], [0, 1], [1, 1], [1, 0]])
    
    sq = (np.array([[np.cos(alpha), -np.sin(alpha)], [np.sin(alpha), np.cos(alpha)]]) @ sq.T).T

    return sq + point

## print(square([0, 0], 2, alpha = np.pi*0.5))

def regular_poly(center, radius, n_sides):
    alphas = (2 * np.pi * np.arange(n_sides))/n_sides 
    rad = np.array([[radius], [0]])

    rot_a = np.moveaxis(np.array([[np.cos(alphas), -np.sin(alphas)], [np.sin(alphas), np.cos(alphas)]]), 2, 0)

    return center + rot_a @ rad
regular_poly(np.array([[0], [0]]), 1, 4)
