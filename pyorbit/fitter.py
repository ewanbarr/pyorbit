import numpy as np
import copy
from scipy.optimize import minimize,leastsq

class Fitter(object):
    def __init__(self,pdata,model):
        self.pdata = pdata
        self.model = model
        self.params_to_fit = []
        self.fits = []
        self.use_weightings = True
        
    def _func(self,values):
        d = dict(zip(self.params_to_fit,values))
        self.model.__dict__.update(d)
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
        assert self.params_to_fit, "No fitting parameters set"
        self.fits.append(copy.deepcopy(self.model))
        params = np.array([self.model.__getattribute__(key) for key in self.params_to_fit])
        new_params,success = leastsq(self._func,params,**kwargs)
        [self.model.__setattr__(key,val) for key,val in zip(self.params_to_fit,new_params)]
        
        
    
    
