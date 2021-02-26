from init import init_parameters, init_grid, init_solu
from bcond import bcond_flowvars
from convection import convec
from viscous import visc
from pressure_solver import SOR
from correction import correction_step
from data_managment import save_restartfile, save_tecplotfile
import sys
import copy

# TO EXECUTE: In terminal enter:
# python3 main.py control_file_path
# control_file_path is the location of the control file relative to main.py
# for example: python3 main.py ../control.dat


def main():

    control_file_path = str(sys.argv[1])
    print(control_file_path)

    parameters = init_parameters(control_file_path)
    grid = init_grid(parameters)
    q, qtmp = init_solu(parameters)

    for t in range(1, parameters.total_time_steps + 1):

        # -------------------------------------------
        # 1. BOUNDARY CONDITIONS
        # -------------------------------------------

        bcond_flowvars(q, parameters)

        # -------------------------------------------
        # 2. FRACTIONAL STEP
        # -------------------------------------------
        # utmp = u + dt * ( convective +  viscous )
        # -------------------------------------------

        # Initialization of first fractional step: utmp = u

        qtmp.u = copy.deepcopy(q.u)
        qtmp.v = copy.deepcopy(q.v)

        # Addition of convective term to the rhs of the fractional step
        # utmp = u --> utmp = u + dt * convective

        convec(grid, q, qtmp, parameters)

        # Addition of viscous term to the rhs of the fractional step
        # utmp = u + dt * convective --> utmp = u + dt * convective + dt * viscous

        visc(grid, q, qtmp, parameters)

        # -------------------------------------------
        # 3. PRESSURE STEP
        # -------------------------------------------
        # p^{n} --> p^{n+1} = f(p^{n},utmp,vtmp)
        # -------------------------------------------

        # Point Successive Over Relaxation (SOR) method for pressure equation
        SOR(grid, q, qtmp, parameters)

        # -------------------------------------------
        # 4. CORRECTION STEP
        # -------------------------------------------
        # u = utmp - dt * grad(p)
        # -------------------------------------------

        correction_step(grid, q, qtmp, parameters)

        # -------------------------------------------
        # 5. OUTPUTS
        # -------------------------------------------

        if t % parameters.tsave_restart == 0:
            save_restartfile(grid, q, parameters, t)

        if t % parameters.tsave_tecplot == 0:
            save_tecplotfile(grid, q, parameters, t)


main()
