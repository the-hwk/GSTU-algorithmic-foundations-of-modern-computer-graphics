import numpy as np

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
POLYGONS = np.array([
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
])

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

    # сначала отсортировать от дальнего до ближайшего (по минимальной координате) (по убыванию)
    # если минимальные координаты совпадают, то отсортировать по максимальной координате (по убыванию)

    # собрать словарь из: значение - индексы

    # poly_mins = {}
    # for ind, poly in enumerate(POLYGONS):
    #     val = np.min(get_poly_points(poly, points)[:, 2])
    #     if val not in poly_mins:
    #         poly_mins[val] = []
    #     poly_mins[val].append(ind)

    # s1 = sorted(poly_mins.items())

    # s1 = sorted(POLYGONS, key=lambda polygon: (
    #     np.min(get_poly_points(polygon, points)[:, 2])
    # ))



    # min_values = [np.min(get_poly_points(polygon, points)) for polygon in POLYGONS]
    # u1 = np.unique(min_values)
    # grouped_mins = [[]]

    # grouped_rows = {k: [row for row, _ in g] for k, g in s2}

    # for max_val, group in grouped_rows.items():
    #     print(f"Группа с максимальным значением {max_val}:")
    #     for row in group:
    #         print(row)

    return sorted_polygons