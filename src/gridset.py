import numpy as np


class GridSet:
    @classmethod
    def read_grid_file(cls, parameters):
        # grid file path
        file_path = parameters.grid_file_path

        # mesh arrays (x,y)

        x = np.zeros((parameters.imax, parameters.jmax))
        y = np.zeros((parameters.imax, parameters.jmax))

        # open the grid file
        f = open(file_path, "r")

        # loop reading grid file
        # the format of grid file is the output of Teplot written file

        # skip the header lines in the grid file
        for cont in range(parameters.grid_header_rows):
            next(f)
            
        for j in range(parameters.jmax):
            for i in range(parameters.imax):
                l = f.readline().strip()
                xread, yread = l.split(" ")
                x[i, j] = float(xread)
                y[i, j] = float(yread)

        f.close()

        return x, y

    def __init__(self, parameters):
        # TO DO: for more than one grid implementation, it has to create an array
        # of grid objects, where each has their attributes (dimensions and bcs)
        # now, the bcs are an attribute of parameters object

        x, y = GridSet.read_grid_file(parameters)
        self.x = x
        self.y = y
