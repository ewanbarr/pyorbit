import numpy as np
import copy
from scipy.optimize import minimize

class Fitter(object):
    def __init__(self,pdata,model):
        self.pdata = pdata
        self.model = model
        self.params_to_fit = []
        self.fits = []
        
    def _func(self,values):
        d = dict(zip(self.params_to_fit,values))
        self._model.__dict__.update(d)
        return self.fitness()

    def residuals(self):
        periods = self._model.evaluate(self.pdata['t'])
        return self.pdata['p0']-periods

    def fitness(self):
        resid = self.residuals()
        return sum((resid/self.pdata['perr'])**2)
    
    def revert(self):
        self.model = self.fits.pop(-1)
        
    def optimize(self):
        assert self.params_to_fit, "No fitting parameters set"
        self.fits.append(copy.deepcopy(self.model))
        params = np.array([self.model.__getattribute__(key) for key in self.params_to_fit])
        new_params = minimize(self._func,params)["x"]
        [self.model.__setattr__(key,val) for key,val in zip(self.params_to_fit,new_params)]
        

    
    
