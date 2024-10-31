import numpy as np

# Матрица точек
POINTS = np.array([
    [0, 0, 0],
    [1, 0, 0],
    [3, 0, 0],
    [4, 0, 0],

    [1, 1, 0],
    [3, 1, 0],

    [1, 2, 0],
    [3, 2, 0],

    [0, 3, 0],
    [1, 3, 0],
    [3, 3, 0],
    [4, 3, 0],

    [0, 0, 5],
    [1, 0, 5],
    [3, 0, 5],
    [4, 0, 5],

    [1, 1, 5],
    [3, 1, 5],

    [1, 2, 5],
    [3, 2, 5],

    [0, 3, 5],
    [1, 3, 5],
    [3, 3, 5],
    [4, 3, 5],
])

# Матрица полигонов
POLYGONS = [
    [0, 1, 9, 8],
    [1, 2, 5, 4],
    [2, 3, 11, 10],
    [6, 7, 10, 9],

    [12, 13, 21, 20],
    [13, 14, 17, 16],
    [14, 15, 23, 22],
    [18, 19, 22, 21],

    [0, 8, 20, 12],
    [3, 11, 23, 15],
    [0, 3, 15, 12],
    [8, 11, 23, 20],
    
    [4, 5, 17, 16],
    [6, 7, 19, 18],
    [4, 6, 18, 16],
    [5, 7, 19, 17]
]

def get_poly_points(polygon, points):
    poly_points = []

    for p in polygon:
        poly_points.append(points[p])

    return np.array(poly_points)

def calc_poly_order(points:list[float]) -> list[list[float]]:
    sorted_polygons = sorted(POLYGONS, key=lambda polygon: (
        np.min(get_poly_points(polygon, points)[:, 2]),
        np.max(get_poly_points(polygon, points)[:, 2])
    ))

    return sorted_polygons