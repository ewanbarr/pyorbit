import numpy as np

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
    

        
    
