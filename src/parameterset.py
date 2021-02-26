class ParameterSet:
    @classmethod
    def read_config_file(cls, control_file_path):
        # empty dictionary to save the parameters
        parameters = {}

        # open the control file
        f = open(control_file_path, "r")

        # loop reading the entries of the control file
        for l in f:
            parameter_entry = l.split("=")
            if len(parameter_entry) > 1:  # it means there is a '=' in
                # line and therefore it is an entry and not a header
                parameters[parameter_entry[0].strip()] = parameter_entry[1].strip()
                print(parameter_entry[0].strip(), " = ", parameter_entry[1].strip())
        f.close()

        return parameters

    def __init__(self, control_file_path):
        parameters = ParameterSet.read_config_file(control_file_path)

        # Flow parameters
        self.rho = float(parameters["rho"])
        self.mu = float(parameters["mu"])

        # Simulation parameters
        self.imax = int(parameters["imax"])
        self.jmax = int(parameters["jmax"])
        self.dt = float(parameters["dt"])
        self.total_time_steps = int(parameters["total_time_steps"])
        self.mesh_type = str(parameters["mesh_type"])

        # Simulation options

        self.convection_method = str(parameters["convection_method"])
        self.viscous_method = str(parameters["viscous_method"])
        self.beta_SOR = float(parameters["beta_SOR"])
        self.max_error = float(parameters["max_error"])
        self.max_iter = float(parameters["max_iter"])

        # Boundary conditions

        self.bcond_i1 = str(parameters["i1"])
        self.bcond_im = str(parameters["im"])
        self.bcond_j1 = str(parameters["j1"])
        self.bcond_jm = str(parameters["jm"])

        # TO DO: this is temporal, for simulating example cases. When we have a more
        # complete version, these parameters should be read from initial solution
        self.u_tangent_j1 = float(parameters["u_tangent_j1"])
        self.u_tangent_jm = float(parameters["u_tangent_jm"])
        self.v_tangent_i1 = float(parameters["v_tangent_i1"])
        self.v_tangent_im = float(parameters["v_tangent_im"])

        # Directories

        # Input Directories

        self.grid_file_path = str(parameters["grid"])
        self.initial_solution_file_path = str(parameters["initial_solution"])
        self.grid_header_rows = int(parameters["grid_header_rows"])
        self.solu_header_rows = int(parameters["solu_header_rows"])
        self.solu_ini_mesh_type = str(parameters["solu_ini_mesh_type"])

        # Output Directories
        self.tsave_restart = int(parameters["tsave_restart"])
        self.tsave_tecplot = int(parameters["tsave_tecplot"])
        self.solu_restart_file_path = str(parameters["solu_restart"])
        self.solu_tecplot_file_path = str(parameters["tecplot_solu"])
        self.solu_restart_mesh_type = str(parameters["solu_restart_mesh_type"])

