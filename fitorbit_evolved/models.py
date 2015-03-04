import numpy as np
import utils

class Parameter(np.float64):
    def __init__(self,value,fit):
        self.name = name
        self.fit
        

class OrbitalModel(object):
    def __init__(self,pb,asini,t0,ecc=0.,om=0.):
        self.pb = pb
        self.asini = asini
        self.t0 = t0
        self.ecc = ecc
        self.om = om

    def __getattr__(self,name):
        assert hasattr(self,name), "attribute '%s' not found"%(name)
        attr = super(OrbitalModel,self).__getattr__(name)
        if isinstance(attr,Parameter)

    def velocity(self,epoch):
        return utils.los_velocity(self.pb,self.asini,self.t0,self.ecc,self.om,epoch)
    
    def acceleration(self,epoch):
        return utils.los_acceleration(self.pb,self.asini,self.t0,self.ecc,self.om,epoch)

    def evaluate(self,epochs):
        vel = np.array([self.velocity(epoch) for epoch in epochs])
        acc = np.array([self.acceleration(epoch) for epoch in epochs])
        return vel,acc
    
class SpinModel(object):
    def __init__(self,p0,p1,pepoch):
        self.p0 = p0
        self.p1 = p1
        self.pepoch = pepoch
        
    def period(self,epoch,orbital_model=None):
        p = self.p0 + self.p1 * (epoch - self.pepoch)
        if orbital_model is not None:
            vlos = orbital_model.velocity(epoch)
            p = (utils.C / (utils.C + vlos)) * p
        return p
        
    def evaluate(self,epochs,orbital_model=None):
        periods = np.array([self.period(epoch,orbital_model) for epoch in epochs])
        return periods
    
    
        
