import numpy as np
from parameterset import ParameterSet
from flowvarset import FlowVarsSet
from gridset import GridSet
import copy


def init_parameters(filepath):
    parameterset = ParameterSet(filepath)
    return parameterset


def init_grid(parameters):
    grid = GridSet(parameters)
    return grid


def init_solu(parameters):
    q = FlowVarsSet(parameters)
    qtmp = copy.deepcopy(q)  # New independent object

    return q, qtmp

