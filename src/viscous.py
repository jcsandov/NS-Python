def visc(grid, q, qtmp, parameters):
    if parameters.viscous_method == "central":
        visc_central(grid, q, qtmp, parameters)


def visc_central(grid, q, qtmp, parameters):

    dt = parameters.dt
    nu = parameters.mu / parameters.rho

    # Viscous component of temporary u-velocity
    for j in range(1, parameters.jmax):
        for i in range(1, parameters.imax - 1):

            # u control-volume is shifted by i+1/2
            dx = grid.x[i + 1, j] - grid.x[i, j]
            dy = grid.y[i, j] - grid.y[i, j - 1]

            # Update the x-rhs by adding the viscous term
            qtmp.u[i, j] = qtmp.u[i, j] + dt * nu * (
                (q.u[i + 1, j] - 2 * q.u[i, j] + q.u[i - 1, j]) / dx ** 2
                + (q.u[i, j + 1] - 2 * q.u[i, j] + q.u[i, j - 1]) / dy ** 2
            )

    # Viscous component of temporary v-velocity
    for j in range(1, parameters.jmax - 1):
        for i in range(1, parameters.imax):

            # v control-volume is shifted by j+1/2
            dx = grid.x[i, j] - grid.x[i - 1, j]
            dy = grid.y[i, j + 1] - grid.y[i, j]

            # Update the y-rhs by adding the viscous term
            qtmp.v[i, j] = qtmp.v[i, j] + dt * nu * (
                (q.v[i + 1, j] - 2 * q.v[i, j] + q.v[i - 1, j]) / dx ** 2
                + (q.v[i, j + 1] - 2 * q.v[i, j] + q.v[i, j - 1]) / dy ** 2
            )

