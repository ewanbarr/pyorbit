import numpy as np
from scipy.optimize import minimize

class Fitter(object):
    def __init__(self,pdata,model):
        self.pdata = pdata
        self.model = model
        self.params_to_fit = []

    def _func(self,values):
        print values
        d = dict(zip(self.params_to_fit,values))
        self.model.__dict__.update(d)
        return self.fitness()

    def residuals(self):
        periods = self.model.evaluate(self.pdata['t'])
        return self.pdata['p0']-periods

    def fitness(self):
        resid = self.residuals()
        return sum((resid/self.pdata['perr'])**2)
    
    def optimize(self):
        assert self.params_to_fit, "No fitting parameters set"
        params = np.array([self.model.__dict__[key] for key in self.params_to_fit])
        return minimize(self._func,params)
    

class SimpleFitter(object):
    def __init__(self,pdata):
        self.data = pdata

    def residuals(self,spin_model,orbital_model=None):
        periods = spin_model.evaluate(self.data['t'],orbital_model)
        return self.data['p0']-periods

    def fitness(self,spin_model,orbital_model=None):
        resid = self.residuals(spin_model,orbital_model=None)
        return sum((resid/self.data['perr'])**2)

    def minimize(self,spin_model,orbital_model=None):
        pass
    

        
    
