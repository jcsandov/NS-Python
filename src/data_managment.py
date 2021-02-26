import numpy as np
import os


def collocated2staggered(p, u, v, parameters):

    pstaggered = collocated2cellcentered(p, parameters)
    ustaggered = collocated2xfacecentered(u, parameters)
    vstaggered = collocated2yfacecentered(v, parameters)

    return pstaggered, ustaggered, vstaggered


def collocated2cellcentered(var, parameters):

    var_cellcentered = np.zeros((parameters.imax + 1, parameters.jmax + 1))
    for J in range(1, parameters.jmax):
        for I in range(1, parameters.imax):
            var_cellcentered[I, J] = 0.25 * (
                var[I, J] + var[I - 1, J] + var[I, J - 1] + var[I - 1, J - 1]
            )

    return var_cellcentered


def collocated2xfacecentered(var, parameters):
    var_xfacecentered = np.zeros((parameters.imax, parameters.jmax + 1))

    for I in range(0, parameters.imax):
        for J in range(1, parameters.jmax):
            var_xfacecentered[I, J] = 0.5 * (var[I, J] + var[I, J - 1])

    # Linear extrapolation to the ghost-points

    # j=1 boundary
    for I in range(0, parameters.imax):
        var_xfacecentered[I, 0] = 2 * var[I, 0] - var_xfacecentered[I, 1]

    # j=jm boundary
    for I in range(0, parameters.imax):
        var_xfacecentered[I, -1] = 2 * var[I, -1] - var_xfacecentered[I, -2]

    return var_xfacecentered


def collocated2yfacecentered(var, parameters):
    var_yfacecentered = np.zeros((parameters.imax + 1, parameters.jmax))

    for J in range(0, parameters.jmax):
        for I in range(1, parameters.imax):
            var_yfacecentered[I, J] = 0.5 * (var[I, J] + var[I - 1, J])

    # Linear extrapolation to the ghost-points

    # i=1 boundary
    for J in range(0, parameters.jmax):
        var_yfacecentered[0, J] = 2 * var[0, J] - var_yfacecentered[1, J]

    # i=im boundary
    for J in range(0, parameters.jmax):
        var_yfacecentered[-1, J] = 2 * var[-1, J] - var_yfacecentered[-2, J]

    return var_yfacecentered


def staggered2collocated(p, u, v, parameters):
    pcollocated = cellcentered2collocated(p, parameters)
    ucollocated = xfacecentered2collocated(u, parameters)
    vcollocated = yfacecentered2collocated(v, parameters)

    return pcollocated, ucollocated, vcollocated


def cellcentered2collocated(var, parameters):

    var_collocated = np.zeros((parameters.imax, parameters.jmax))

    var_collocated = 0.25 * (
        var[0 : parameters.imax, 0 : parameters.jmax]
        + var[1 : parameters.imax + 1, 0 : parameters.jmax]
        + var[0 : parameters.imax, 1 : parameters.jmax + 1]
        + var[1 : parameters.imax + 1, 1 : parameters.jmax + 1]
    )

    return var_collocated


def xfacecentered2collocated(var, parameters):
    var_collocated = 0.5 * (
        var[0 : parameters.imax, 1 : parameters.jmax + 1]
        + var[0 : parameters.imax, 0 : parameters.jmax]
    )

    return var_collocated


def yfacecentered2collocated(var, parameters):
    var_collocated = 0.5 * (
        var[1 : parameters.imax + 1, 0 : parameters.jmax]
        + var[0 : parameters.imax, 0 : parameters.jmax]
    )

    return var_collocated


def save_restartfile(grid, q, parameters, t):

    filename = "solu_restart_%06d.dat" % t  # exmp: "solu_restart_000001.dat"
    file_path = parameters.solu_restart_file_path + filename

    if parameters.solu_restart_mesh_type == "collocated":

        # If file already exists, remove it
        try:
            os.remove(file_path)
        except OSError:
            pass

        # open the solu_restart file
        f = open(file_path, "a")  # a = append

        # loop writing solu file
        # the format of solu file is the output of Tecplot written file

        # skip the header lines in the solu file
        for cont in range(parameters.solu_header_rows):
            f.write("dummy")

        xwrite = grid.x
        ywrite = grid.y
        pwrite, uwrite, vwrite = staggered2collocated(q.p, q.u, q.v, parameters)

        for j in range(parameters.jmax):
            for i in range(parameters.imax):

                f.write(
                    xwrite[i, j], ywrite[i, j], pwrite[i, j], uwrite[i, j], vwrite[i, j]
                )

        f.close()

    else:  # staggered

        # Auxiliary arrays to save flow vars writing solu_restart file

        pwrite = np.zeros((parameters.imax + 1, parameters.jmax + 1))
        uwrite = np.zeros((parameters.imax + 1, parameters.jmax + 1))
        vwrite = np.zeros((parameters.imax + 1, parameters.jmax + 1))

        pwrite = q.p
        uwrite[1::, :] = q.u
        vwrite[:, 1::] = q.v

        # If file already exists, remove it
        try:
            os.remove(file_path)
        except OSError:
            pass

        # open the grid file
        f = open(file_path, "a")  # a = append

        # loop reading solu file
        # the output solu file has to be written in the same way as it
        # is read (see data_managment.py)

        # skip the header lines in the solu file
        for cont in range(parameters.solu_header_rows):
            f.write("dummy \n")

        for j in range(parameters.jmax + 1):
            for i in range(parameters.imax + 1):
                formatted_output = (
                    str(pwrite[i, j])
                    + " "
                    + str(uwrite[i, j])
                    + " "
                    + str(vwrite[i, j])
                    + "\n"
                )
                f.write(formatted_output)

        f.close()


def save_tecplotfile(grid, q, parameters, t):
    filename = "solu_%06d.plt" % t  # exmp: "solu_000001.tec"
    file_path = parameters.solu_tecplot_file_path + filename

    X = grid.x
    Y = grid.y

    if parameters.mesh_type == "staggered":
        P, U, V = staggered2collocated(q.p, q.u, q.v, parameters)
    else:
        P, U, V = q.p, q.u, q.v

    # Write the data to Tecplot format
    vars = {"p": P, "u": U, "v": V}
    tecplot_writer(file_path, vars, parameters, X, Y, [])  # 2D


def tecplot_writer(filename, variables, parameters, X=[], Y=[], Z=[]):
    """
    Downloaded from (25/02/2021): 
    https://github.com/seekiu/tecplot_writer/blob/master/tecplot_writer.py
    
    X, Y, Z are the lists of xyz coordinates. If not provided, intergers
    from 0 will be used.
    `variables` is a dict of the variables to store with the variable names as
    the keys. Each variable should be 2 or 3 dimensional array using numpy's
    row-major order.
    Check the test function to see how to create input data structure.
    Notice that tecplot format use 'column-major order' as in Fortran, which is
    different from that of Numpy or C.
    """
    # if filename[-4:] != ".dat":
    #    filename += ".dat"

    with open(filename, "w") as f:
        ## 2D case
        #        if len(Z) == 0:
        if True:
            f.write('Variables = "X", "Y"')
            for key in variables.keys():
                f.write(', "' + key + '"')
            f.write(
                "\n\nZone I="
                + str(parameters.imax)
                + ", J="
                + str(parameters.jmax)
                + ", F=POINT\n"
            )

            for j in range(parameters.jmax):
                for i in range(parameters.imax):
                    f.write(str(X[i, j]) + " " + str(Y[i, j]))
                    for var in variables.values():
                        f.write(" " + str(var[i, j]))
                    f.write("\n")


#        ## 3D case
#        else:
#            f.write('Variables = "X", "Y", "Z"')
#            for key in variables.keys():
#                f.write(', "' + key + '"')
#            f.write(
#                "\n\nZone I="
#                + str(len(X))
#                + ", J="
#                + str(len(Y))
#                + ", K="
#                + str(len(Z))
#                + ", F=POINT\n"
#            )
#
#            for k in range(len(Z)):
#                for j in range(len(Y)):
#                    for i in range(len(X)):
#                        f.write(str(X[i]) + " " + str(Y[j]) + " " + str(Z[k]))
#                        for var in variables.values():
#                            f.write(" " + str(var[i, j, k]))
#                        f.write("\n")

