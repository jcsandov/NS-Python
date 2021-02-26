def convec(grid, q, qtmp, parameters):
    if parameters.convection_method == "central":
        convec_central(grid, q, qtmp, parameters)


def convec_central(grid, q, qtmp, parameters):

    dt = parameters.dt

    # Convective component of temporary u-velocity
    for j in range(1, parameters.jmax):
        for i in range(1, parameters.imax - 1):

            # u control-volume is shifted by i+1/2
            dx = grid.x[i + 1, j] - grid.x[i, j]
            dy = grid.y[i, j] - grid.y[i, j - 1]

            # Update the x-rhs by adding the convective term
            qtmp.u[i, j] = qtmp.u[i, j] + dt * (
                -0.25
                * (
                    (
                        (q.u[i + 1, j] + q.u[i, j]) ** 2
                        - (q.u[i, j] + q.u[i - 1, j]) ** 2
                    )
                    / dx
                    + (
                        (q.u[i, j + 1] + q.u[i, j]) * (q.v[i + 1, j] + q.v[i, j])
                        - (q.u[i, j] + q.u[i, j - 1])
                        * (q.v[i + 1, j - 1] + q.v[i, j - 1])
                    )
                    / dy
                )
            )

    # Convective component of temporary v-velocity
    for j in range(1, parameters.jmax - 1):
        for i in range(1, parameters.imax):

            # v control-volume is shifted by j+1/2
            dx = grid.x[i, j] - grid.x[i - 1, j]
            dy = grid.y[i, j + 1] - grid.y[i, j]

            # Update the y-rhs by adding the convective term
            qtmp.v[i, j] = qtmp.v[i, j] + dt * (
                -0.25
                * (
                    (
                        (q.u[i, j + 1] + q.u[i, j]) * (q.v[i + 1, j] + q.v[i, j])
                        - (q.u[i - 1, j + 1] + q.u[i - 1, j])
                        * (q.v[i, j] + q.v[i - 1, j])
                    )
                    / dx
                    + (
                        (q.v[i, j + 1] + q.v[i, j]) ** 2
                        - (q.v[i, j] + q.v[i, j - 1]) ** 2
                    )
                    / dy
                )
            )

