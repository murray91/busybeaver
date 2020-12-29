import busybeaver.interpolation as bbinterp
import pytest
from mikeio import Dfsu

# Tests getting the interpolants
# -----
@pytest.mark.interp
def test_get_interpolants_1():
    
    dfs = Dfsu(r"tests\data\MIKE\test_max_results.dfsu")
    ds = dfs.read("Maximum water depth")
    interp_point = (594238.084,6645064.994)

    interpolants = bbinterp.get_interpolants(interp_point, dfs.element_coordinates, ds.data[0][0])

    points = []
    for i in interpolants:
        x, y, z = round(i[0], 3), round(i[1], 3), round(i[2], 4)
        points.append((x, y, z))

    x0, y0, z0 = 594238.500, 6645066.167, 0.0221
    x1, y1, z1 = 594236.979, 6645065.667, 0.2365
    x2, y2, z2 = 594236.938, 6645064.167, 0.0235
    x3, y3, z3 = 594238.688, 6645063.833, 0.0226

    expected = [(x0,y0,z0),(x1,y1,z1),(x2,y2,z2),(x3,y3,z3)]

    assert points == expected

@pytest.mark.interp
def test_get_interpolants_2():
    
    dfs = Dfsu(r"tests\data\MIKE\test_max_results.dfsu")
    ds = dfs.read("Maximum water depth")
    interp_point = (594238.084,6645064.994)
    xi = interp_point[0]
    yi = interp_point[1]

    interpolants = bbinterp.get_interpolants(interp_point, dfs.element_coordinates, ds.data[0][0])

    points = []
    for i in interpolants:
        x, y, z = round(i[0], 3), round(i[1], 3), round(i[2], 4)
        points.append((x, y, z))

    x0, y0, z0 = 594238.500, 6645066.167, 0.0221
    x1, y1, z1 = 594236.979, 6645065.667, 0.2365
    x2, y2, z2 = 594236.938, 6645064.167, 0.0235
    x3, y3, z3 = 594238.688, 6645063.833, 0.0226

    assert x0 >= xi and y0 >= yi

@pytest.mark.interp
def test_get_interpolants_3():
    
    dfs = Dfsu(r"tests\data\MIKE\test_max_results.dfsu")
    ds = dfs.read("Maximum water depth")
    interp_point = (594238.084,6645064.994)
    xi = interp_point[0]
    yi = interp_point[1]

    interpolants = bbinterp.get_interpolants(interp_point, dfs.element_coordinates, ds.data[0][0])

    points = []
    for i in interpolants:
        x, y, z = round(i[0], 3), round(i[1], 3), round(i[2], 4)
        points.append((x, y, z))

    x0, y0, z0 = 594238.500, 6645066.167, 0.0221
    x1, y1, z1 = 594236.979, 6645065.667, 0.2365
    x2, y2, z2 = 594236.938, 6645064.167, 0.0235
    x3, y3, z3 = 594238.688, 6645063.833, 0.0226

    assert x1 < xi and y1 >= yi

@pytest.mark.interp
def test_get_interpolants_3():
    
    dfs = Dfsu(r"tests\data\MIKE\test_max_results.dfsu")
    ds = dfs.read("Maximum water depth")
    interp_point = (594238.084,6645064.994)
    xi = interp_point[0]
    yi = interp_point[1]

    interpolants = bbinterp.get_interpolants(interp_point, dfs.element_coordinates, ds.data[0][0])

    points = []
    for i in interpolants:
        x, y, z = round(i[0], 3), round(i[1], 3), round(i[2], 4)
        points.append((x, y, z))

    x0, y0, z0 = 594238.500, 6645066.167, 0.0221
    x1, y1, z1 = 594236.979, 6645065.667, 0.2365
    x2, y2, z2 = 594236.938, 6645064.167, 0.0235
    x3, y3, z3 = 594238.688, 6645063.833, 0.0226

    assert x2 < xi and y2 < yi

@pytest.mark.interp
def test_get_interpolants_4():
    
    dfs = Dfsu(r"tests\data\MIKE\test_max_results.dfsu")
    ds = dfs.read("Maximum water depth")
    interp_point = (594238.084,6645064.994)
    xi = interp_point[0]
    yi = interp_point[1]

    interpolants = bbinterp.get_interpolants(interp_point, dfs.element_coordinates, ds.data[0][0])

    points = []
    for i in interpolants:
        x, y, z = round(i[0], 3), round(i[1], 3), round(i[2], 4)
        points.append((x, y, z))

    x0, y0, z0 = 594238.500, 6645066.167, 0.0221
    x1, y1, z1 = 594236.979, 6645065.667, 0.2365
    x2, y2, z2 = 594236.938, 6645064.167, 0.0235
    x3, y3, z3 = 594238.688, 6645063.833, 0.0226

    assert x3 >= xi and y3 < yi


# Tests distance between points
# -----
@pytest.mark.interp
def test_distance_between_points_1():
    pnt1 = (594238.500, 6645066.167)
    pnt2 = (594236.979, 6645065.667)

    expected = ((594236.979-594238.500)**2 + (6645066.167-6645065.667)**2)**0.5

    assert expected == bbinterp.distance_between_points(pnt1, pnt2)

# Tests interpolation of a point
# -----
@pytest.mark.interp
def test_interp_point_1():
    
    dfs = Dfsu(r"tests\data\MIKE\test_max_results.dfsu")
    ds = dfs.read("Maximum water depth")
    interp_point = (594238.084,6645064.994)

    interpolants = bbinterp.get_interpolants(interp_point, dfs.element_coordinates, ds.data[0][0])

    quad0 = interpolants[0]
    quad1 = interpolants[1]
    quad2 = interpolants[2]
    quad3 = interpolants[3]

    interpolants = None

    z = bbinterp.interp_point(interp_point, quad0, quad1, quad2, quad3)

    assert round(z[2],6) == 0.055493