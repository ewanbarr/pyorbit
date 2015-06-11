import numpy as np
import copy
from scipy.optimize import minimize,leastsq
from collections import OrderedDict
import warnings

class FittingParameters(object):
    def __init__(self,model):
        self.spin = OrderedDict()
        self.spin["p0"] = False
        self.spin["p1"] = False
        self.spin["pepoch"] = False
        self.orbits = []
        for orbit in model.orbits:
            orbit_params = OrderedDict()
            orbit_params["pb"] = False
            orbit_params["asini"] = False
            orbit_params["t0"] = False
            orbit_params["ecc"] = False
            orbit_params["om"] = False
            self.orbits.append(orbit_params)

    def get_values(self,model):
        vals = []
        for key,val in self.spin.items():
            if val:
                vals.append(model.__getattribute__(key))
        for ii,orbit in enumerate(self.orbits):
            for key,val in orbit.items():
                if val:
                    vals.append(model.orbits[ii].__getattribute__(key))
        return np.array(vals)
    
    def set_values(self,model,vals):
        vals = list(vals)
        for key,val in self.spin.items():
            if val:
                model.__setattr__(key,vals.pop(0))
        for ii,orbit in enumerate(self.orbits):
            for key,val in orbit.items():
                if val:
                    model.orbits[ii].__setattr__(key,vals.pop(0))
                    
    def __repr__(self):
        out = []
        out.append("-- Spin --")
        for key,val in self.spin.items():
            out.append("%s%s"%(key.ljust(10),val))
        for ii,orbit in enumerate(self.orbits):
            out.append("-- Orbit %d --"%(ii))
            for key,val in orbit.items():
                out.append("%s%s"%(key.ljust(10),val))
        return "\n".join(out)


class Fitter(object):
    def __init__(self,pdata,model):
        self.pdata = pdata
        self.model = model
        self.fits = []
        self.params = FittingParameters(model)
        self.use_weightings = True
        
    def _func(self,values):
        self.params.set_values(self.model,values)
        print "Func called"
        print self.model
        if self.use_weightings:
            return self.residuals()/self.pdata["perr"]
        else:
            return self.residuals()

    def residuals(self):
        periods = self.model.evaluate(self.pdata['t'])
        return self.pdata['p0']-periods

    def fitness(self):
        resid = self.residuals()
        return sum((resid/self.pdata['perr'])**2)
    
    def revert(self):
        self.model = self.fits.pop(-1)

    def fit(self,**kwargs):
        self.fits.append(copy.deepcopy(self.model))
        init_values = self.params.get_values(self.model)
        new_values,success = leastsq(self._func,init_values,**kwargs)
        self.params.set_values(self.model,new_values)
        if not success:
            warnings.warn("Fit unsuccessful.")
        
    
    
