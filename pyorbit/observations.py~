import numpy as np
from pyorbit import utils

PER_FILE_DTYPE = [("t","float64"),
                  ("p0","float64"),
                  ("perr","float64"),
                  ("dm","float32"),
                  ("dmerr","float32"),
                  ("w50","float32"),
                  ("snr","float32")]

class Observation(object):
    """
    Container class for observation data
    """
    def __init__(self,p,perr,epoch,acc=None,tobs=None):
        """
        Create an observation object.
        
        Inputs:
        p - period (s)
        perr - period error (s)
        epoch - observing epoch (s)
        acc - acceleration (m/s/s)
        tobs - observation time (s)
        """
        self.p = p             # s
        self.perr = perr       # s
        self.epoch = epoch     # s
        self.acc = acc         # m/s/s
        self.tobs = tobs       # s

    def __repr__(self):
        p_ms = self.p * 1e3
        epoch_mjd = self.epoch / utils.DAY_2_SEC
        perr_ms = self.perr * 1e3
        args = (epoch_mjd,p_ms,perr_ms,self.acc,self.tobs)
        return "(%s)"%(",".join([repr(i) for i in args]))


def from_per_file(fname):
    """
    Read observation data from a pdmp.per file.
    
    Inputs:
    fname -- per file filename
    
    Notes:
    per files do not contain acceleration information
    """
    pdata = np.genfromtxt(fname,usecols=[0,1,2],dtype=PER_FILE_DTYPE)
    pdata["p0"]   /= 1e3 # milliseconds to seconds  
    pdata["perr"] /= 1e3 # milliseconds to seconds
    pdata["t"]    *= utils.DAY_2_SEC # days to seconds
    return pdata

        
