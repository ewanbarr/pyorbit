import numpy as np
from pyorbit import utils

class IsolatedPulsar(object):
    def __init__(self,p0,p1,pepoch):
        self.p0 = p0 
        self.p1 = p1
        self.pepoch = pepoch * utils.DAY_2_SEC
        
    def period(self,epoch):
        return self.p0 + self.p1 * (epoch - self.pepoch)
    
    def evaluate(self,epochs):
        return self.period(np.array(epochs))

class BinaryPulsar(IsolatedPulsar):
    def __init__(self,p0,p1,pepoch,pb,asini,t0,ecc,om):
        super(BinaryPulsar,self).__init__(p0,p1,pepoch)
        self.pb = pb * utils.DAY_2_SEC
        self.asini = asini * utils.C
        self.t0 = t0 * utils.DAY_2_SEC
        self.ecc = ecc
        self.om = om

    def velocity(self,epoch):
        if self.ecc < 0.000001:
            return utils.los_velocity_circ(self.pb,self.asini,self.t0,epoch)
        else:
            return utils.los_velocity(self.pb,self.asini,self.t0,self.ecc,self.om,epoch)

    def acceleration(self,epoch):
        if self.ecc < 0.000001:
            return utils.los_acceleration_circ(self.pb,self.asini,self.t0,epoch)
        else:
            return utils.los_acceleration(self.pb,self.asini,self.t0,self.ecc,self.om,epoch)

    def period(self,epoch):
        return super(BinaryPulsar,self).period(epoch) * self.doppler_factor(epoch)

    def evaluate(self,epochs):
        return np.array([self.period(epoch) for epoch in epochs])

    def doppler_factor(self,epoch):
        vlos = self.velocity(epoch)
        return utils.C / (utils.C + vlos)


def read_par_file(fname):
    f = open(fname)
    par = {}
    for line in f.readlines():
        line = line.split()
        if len(line) < 2:
            continue
        key = line[0]
        val = line[1]
        par[key] = val
    
    if "P0" in par:
        p0 = float(par["P0"])
    elif "F0" in par:
        p0 = 1/float(par["F0"])
    else:
        p0 = 0.0

    if "P1" in par:
        p1 = float(par["P1"])
    elif "F1" in par:
        f1 = float(par["F1"])
        p1 = -p0**2 * f1
    else:
        p1 = 0.0

    pepoch = float(par.get("PEPOCH",0.0))
        
    if "BINARY" in par:
        pb = float(par.get("PB",0.0))
        asini = float(par.get("A1",0.0))
        t0 = float(par.get("T0",0.0))
        om = float(par.get("OM",0.0))
        ecc = float(par.get("ECC",0.0))
        return BinaryPulsar(p0,p1,pepoch,pb,asini,t0,ecc,om)
    else:
        return IsolatedPulsar(p0,p1,pepoch)
        
def write_par_file(fname,model):
    f = open(fname,"w+")
    print>>f,"P0",model.p0
    print>>f,"P1",model.p1
    print>>f,"PEPOCH",model.pepoch/utils.DAY_2_SEC
    
    if isinstance(model,BinaryPulsar):
        print>>f,"BINARY","BT"
        print>>f,"PB",model.pb/utils.DAY_2_SEC
        print>>f,"A1",model.asini/utils.C
        print>>f,"T0",model.t0/utils.DAY_2_SEC
        print>>f,"ECC",model.ecc
        print>>f,"OM",model.om
    f.close()
    
        
        
        

        
