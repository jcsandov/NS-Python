import numpy as np
from data_managment import collocated2staggered


class FlowVarsSet:
    @classmethod
    def read_initial_solution_file(cls, parameters):
        # solu file path
        file_path = parameters.initial_solution_file_path

        if parameters.solu_ini_mesh_type == "collocated":
            # mesh arrays (p,u,v)

            p = np.zeros((parameters.imax, parameters.jmax))
            u = np.zeros((parameters.imax, parameters.jmax))
            v = np.zeros((parameters.imax, parameters.jmax))

            # open the solu file
            f = open(file_path, "r")

            # loop reading solu file
            # the format of solu file is the output of Tecplot written file

            # skip the header lines in the solu file
            for cont in range(parameters.solu_header_rows):
                next(f)

            for j in range(parameters.jmax):
                for i in range(parameters.imax):
                    l = f.readline().strip()
                    xread, yread, pread, uread, vread = l.split(" ")
                    p[i, j] = float(pread)
                    u[i, j] = float(uread)
                    v[i, j] = float(vread)

            f.close()

        else:  # staggered

            # Auxiliary arrays to save flow vars reading solu file

            paux = np.zeros((parameters.imax + 1, parameters.jmax + 1))
            uaux = np.zeros((parameters.imax + 1, parameters.jmax + 1))
            vaux = np.zeros((parameters.imax + 1, parameters.jmax + 1))

            # open the grid file
            f = open(file_path, "r")

            # loop reading solu file
            # the output solu file has to be written in the same way as it
            # is read (see data_managment.py)

            # skip the header lines in the solu file
            for cont in range(parameters.solu_header_rows):
                next(f)

            for j in range(parameters.jmax + 1):
                for i in range(parameters.imax + 1):
                    l = f.readline().strip()
                    pread, uread, vread = l.split(" ")
                    paux[i, j] = float(pread)
                    uaux[i, j] = float(uread)
                    vaux[i, j] = float(vread)

            f.close()
            p = paux
            u = uaux[1::, :]
            v = vaux[:, 1::]

        return p, u, v

    def __init__(self, parameters):

        # flow variables
        # TO DO: this is a formulation for staggered grid (FVM) using ghost points
        # following the Tryggvason lectures. For different formulations (collocated
        # grids for example), the size of the arrays has to adapt

        p, u, v = FlowVarsSet.read_initial_solution_file(parameters)

        if (
            parameters.solu_ini_mesh_type == "collocated"
            and parameters.mesh_type == "staggered"
        ):
            p, u, v = collocated2staggered(p, u, v, parameters)

        self.p = p
        self.u = u
        self.v = v

