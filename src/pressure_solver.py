import numpy as np
import copy


def SOR(grid, q, qtmp, parameters):
    # p^{m+1} = beta*tmp1*(tmp2 + f(p^{m},p^{m+1})+ (1-beta)*p^{m}
    # where m is the solver iteration step

    aux = np.zeros((parameters.imax + 1, parameters.jmax + 1))
    divergence_term = np.zeros((parameters.imax + 1, parameters.jmax + 1))

    dt = parameters.dt
    beta = parameters.beta_SOR
    max_error = parameters.max_error
    max_iter = parameters.max_iter

    for j in range(1, parameters.jmax):
        for i in range(1, parameters.imax):

            dx = grid.x[i, j] - grid.x[i - 1, j]
            dy = grid.y[i, j] - grid.y[i, j - 1]

            aux[i, j] = 1.0 / (-2.0 / dx ** 2 - 2.0 / dy ** 2)

            divergence_term[i, j] = (1.0 / dt) * (
                (qtmp.u[i, j] - qtmp.u[i - 1, j]) / dx
                + (qtmp.v[i, j] - qtmp.v[i, j - 1]) / dy
            )

    # Iteration step of SOR method
    iter = 0
    while True:
        pn = copy.deepcopy(q.p)
        iter = iter + 1
        for i in range(1, parameters.imax):
            for j in range(1, parameters.jmax):
                pressure_term = (q.p[i + 1, j] + q.p[i - 1, j]) / dx ** 2 + (
                    q.p[i, j + 1] + q.p[i, j - 1]
                ) / dy ** 2

                q.p[i, j] = (1.0 - beta) * q.p[i, j] + beta * aux[i, j] * (
                    divergence_term[i, j] - pressure_term
                )

        if np.abs(pn - q.p).max() < max_error:
            break
        if iter > max_iter:
            break
