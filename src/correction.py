def correction_step(grid, q, qtmp, parameters):
    # Correct the u-velocity
    # u = utmp - dt * (P_{i+1,j}-P_{i,j})/dx
    for i in range(1, parameters.imax - 1):
        for j in range(1, parameters.jmax):
            dt = parameters.dt
            dx = grid.x[i, j] - grid.x[i - 1, j]

            q.u[i, j] = qtmp.u[i, j] - dt / dx * (q.p[i + 1, j] - q.p[i, j])

    # Correct the v-velocity
    # v = vtmp - dt * (P_{i,j+1}-P_{i,j})/dy

    for i in range(1, parameters.imax):
        for j in range(1, parameters.jmax - 1):
            dt = parameters.dt
            dy = grid.y[i, j] - grid.y[i, j - 1]

            q.v[i, j] = qtmp.v[i, j] - dt / dy * (q.p[i, j + 1] - q.p[i, j])
