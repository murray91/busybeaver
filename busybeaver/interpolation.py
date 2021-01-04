# This module includes implementation for bilinear interpolation

# Returns 4 points to do bilinear interpolation with
#
# Arg: interp_pnt, tuple point (x,y), ndarray of points from Dfsu.element_coordinates [[x,y,z], [x,y,z], [x,y,z], ...]
#
# Returns index of closest points in each quadrant in form of array [quad0, quad1, quad2, quad3]
def get_interpolants(interp_pnt, element_coords, ds_data):

    # placeholders for quadrant points
    quad0 = [1000, None]
    quad1 = [1000, None]
    quad2 = [1000, None]
    quad3 = [1000, None]
    xi = interp_pnt[0]
    yi = interp_pnt[1]

    # find the closest point in each quadrant
    for index, pnt in enumerate(element_coords):

        x = pnt[0]
        y = pnt[1]
        dist = distance_between_points(interp_pnt, pnt)

        # quad 0
        if x >= xi and y >= yi:
            if quad0[0] >= dist:
                quad0 = [dist, index]
        # quad 1
        elif x < xi and y >= yi:
            if quad1[0] >= dist:
                quad1 = [dist, index]
        # quad 2
        elif x < xi and y < yi:
            if quad2[0] >= dist:
                quad2 = [dist, index]
        #quad 3
        else:
            if quad3[0] >= dist:
                quad3 = [dist, index]    

    # return list of points
    return [id_to_xyz(quad0[1], element_coords, ds_data),
            id_to_xyz(quad1[1], element_coords, ds_data),
            id_to_xyz(quad2[1], element_coords, ds_data),
            id_to_xyz(quad3[1], element_coords, ds_data)]

# returns horizontal distance
def distance_between_points(pnt1, pnt2):
    dx = pnt1[0] - pnt2[0]
    dy = pnt1[1] - pnt2[1]
    return (dx**2 + dy**2)**0.5

# converts a point based on dfs coords and data
def id_to_xyz(id, dfs_coords, dfs_data):

    x = dfs_coords[id][0]
    y = dfs_coords[id][1]
    z = dfs_data[id]

    return (x, y, z)

# Accepts xyz points as args in each quadrant, and interpolates based on that.
def interp_point(interp_pnt, quad0, quad1, quad2, quad3):

    #point to interpolate
    xc = interp_pnt[0]
    yc = interp_pnt[1]

    print(xc)
    print(yc)

    # quad coords
    x0 = quad0[0]
    y0 = quad0[1]
    z0 = quad0[2]

    x1 = quad1[0]
    y1 = quad1[1]
    z1 = quad1[2]

    x2 = quad2[0]
    y2 = quad2[1]
    z2 = quad2[2]

    x3 = quad3[0]
    y3 = quad3[1]
    z3 = quad3[2]

    print(x0,y0,z0)
    print(x1,y1,z1)
    print(x2,y2,z2)
    print(x3,y3,z3)

    A1=x0
    A2=y0
    B1=x1-x0
    B2=y1-y0
    C1=x3-x0
    C2=y3-y0
    D1=x2-x1+x0-x3
    D2=y2-y1+y0-y3

    a = D1*B2 - D2*B1
    b = D2*xc - D1*yc - D2*A1 + D1*A2 + C1*B2 - C2*B1
    c = C2*xc - C1*yc + C1*A2 - C2*A1

    dx = (-b+(b**2-4*a*c)**0.5)/(2*a)
    if dx < 0 or dx > 1:
        dx = (-b-(b**2-4*a*c)**0.5)/(2*a)

    if (C1-D1*dx):
        dy = (xc-A1-B1*dx)/(C1-D1*dx)
    else:
        dy = (xc-A2-B2*dx)/(C2-D2*dx)

    zc = (1-dx)*(1-dy)*z2 + dx*(1-dy)*z3 + (1-dx)*dy*z1 + dx*dy*z0

    print(dx, dy)
    print((1-dx)*(1-dy)*z2)
    print(dx*(1-dy)*z3)
    print((1-dx)*dy*z1)
    print(dx*dy*z0)

    return (xc, yc, zc)

# interpolate the entire grid
#
# Takes as arguments
# mikeio Grid, and mikeio Dfsu.element_coords
def interp_grid(grid, element_coords, dfs_data):

    z = []

    # interpolate each z in grid
    for pnt in grid.xy:

        # get nearest 4 points
        interpolants = get_interpolants(pnt, points)
        # interpolate grid point based on 4 nearest points
        z_int = interp_point(pnt, interpolants[0], interpolants[1], interpolants[2], interpolants[3])
        z.append(z_int)

    return z

def write_to_shp(filename, grid, data):

    

    new_dataset = rasterio.open(
        filename,
        'w',
        driver='GTiff',
        height= grid.ny,
        width= grid.nx,
        count=1,
        dtype=,
        crs=,
        transform=transform
    )

    new_dataset.write(Z, 1)
    new_dataset.close()

    return None
