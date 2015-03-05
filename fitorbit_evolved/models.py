import numpy as np
import utils

class IsolatedPulsar(object):
    def __init__(self,p0,p1,pepoch):
        self.p0 = p0
        self.p1 = p1
        self.pepoch = pepoch
        
    def period(self,epoch):
        return self.p0 + self.p1 * (epoch - self.pepoch)
    
    def evaluate(self,epochs):
        return self.period(np.array(epochs))

class BinaryPulsar(IsolatedPulsar):
    def __init__(self,p0,p1,pepoch,pb,asini,t0,ecc,om):
        super(BinaryPulsar,self).__init__(p0,p1,pepoch)
        self.pb = pb
        self.asini = asini
        self.t0 = t0
        self.ecc = ecc
        self.om = om

    def velocity(self,epoch):
        return utils.los_velocity(self.pb,self.asini,self.t0,self.ecc,self.om,epoch)
    
    def acceleration(self,epoch):
        return utils.los_acceleration(self.pb,self.asini,self.t0,self.ecc,self.om,epoch)

    def period(self,epoch):
        return super(BinaryPulsar,self).period(epoch) * self.doppler_factor(epoch)

    def evalulate(self,epochs):
        return np.array([self.period(epoch) for epoch in epochs])

    def doppler_factor(self,epoch):
        vlos = self.velocity(epoch)
        return utils.C / (utils.C + vlos)

    
    
        
