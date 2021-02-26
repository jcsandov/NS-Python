def bcond_flowvars(q, parameters):
    # _________________________________
    # i = 1
    # ---------------------------------
    if parameters.bcond_i1 == "wall":
        q.u[0, :] = 0.0
        # reflection technique to set zero v-velocity at the wall
        q.v[0, :] = -1.0 * q.v[1, :]

    elif parameters.bcond_i1 == "tangent_velocity":
        q.u[0, :] = 0.0
        q.v[0, :] = 2.0 * parameters.v_tangent_i1 - q.v[1, :]

    # _________________________________
    # i = im
    # ---------------------------------
    if parameters.bcond_im == "wall":
        q.u[-1, :] = 0.0
        # reflection technique to set zero v-velocity at the wall
        q.v[-1, 1:-1] = -1.0 * q.v[-2, 1:-1]

    elif parameters.bcond_im == "tangent_velocity":
        q.u[0, :] = 0.0
        q.v[-1, 1:-1] = 2.0 * parameters.v_tangent_im - q.v[-2, 1:-1]

    # _________________________________
    # j = 1
    # ---------------------------------
    if parameters.bcond_j1 == "wall":
        # reflection technique to set zero u-velocity at the wall
        q.u[:, 0] = -1.0 * q.u[:, 1]
        q.v[:, 0] = 0.0

    elif parameters.bcond_j1 == "tangent_velocity":
        q.u[1:-1, 0] = 2.0 * parameters.u_tangent_j1 - q.u[1:-1, 1]
        q.v[:, 0] = 0.0

    # _________________________________
    # j = jm
    # ---------------------------------
    if parameters.bcond_jm == "wall":
        # reflection technique to set zero u-velocity at the wall
        q.u[:, -1] = -1.0 * q.u[:, -2]
        q.v[:, -1] = 0.0

    elif parameters.bcond_jm == "tangent_velocity":
        q.u[1:-1, -1] = 2.0 * parameters.u_tangent_jm - q.u[1:-1, -2]
        q.v[:, -1] = 0.0

