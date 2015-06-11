import numpy as np
from pyorbit import utils

class KeplerianOrbit(object):
    def __init__(self,pb,asini,t0,ecc,om):
        self.pb = pb * utils.DAY_2_SEC
        self.asini = asini * utils.C
        self.t0 = t0 * utils.DAY_2_SEC
        self.ecc = ecc
        self.om = np.pi*om/180.0

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
        
    def __repr__(self):
        out = [
            "pb".ljust(10)+"%e days"%(self.pb/utils.DAY_2_SEC),
            "asini".ljust(10)+"%e lt-s"%(self.asini/utils.C),
            "t0".ljust(10)+"%e MJD"%(self.t0/utils.DAY_2_SEC),
            "ecc".ljust(10)+"%e"%(self.ecc),
            "om".ljust(10)+"%e degrees"%(180.0*self.om/np.pi)
            ]
        return "\n".join(out)

class Pulsar(object):
    def __init__(self,p0,p1,pepoch,ra,dec):
        self.p0 = p0 
        self.p1 = p1
        self.pepoch = pepoch * utils.DAY_2_SEC
        self.orbits = []
        
    def period(self,epoch):
        p = self.p0 + self.p1 * (epoch - self.pepoch)
        return p * self._doppler_factor(epoch)
    
    def evaluate(self,epochs):
        return np.array([self.period(epoch) for epoch in epochs])
    
    def _doppler_factor(self,epoch):
        if self.orbits:       
            vlos = sum([orbit.velocity(epoch) for orbit in self.orbits])
            return utils.C / (utils.C + vlos)
        else:
            return 1.0
        
    def __repr__(self):
        out = [
            "p0".ljust(10)+"%f seconds"%(self.p0),
            "p1".ljust(10)+"%f s/s"%(self.p1),
            "pepoch".ljust(10)+"%f"%(self.pepoch/utils.DAY_2_SEC)
            ]
        for ii,orbit in enumerate(self.orbits):
            out.append("\nOrbit %d:"%ii)
            out.append(repr(orbit))
        return "\n".join(out)


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
    pulsar = Pulsar(p0,p1,pepoch)
        
    if "BINARY" in par:
        pb = float(par.get("PB",0.0))
        asini = float(par.get("A1",0.0))
        t0 = float(par.get("T0",0.0))
        om = float(par.get("OM",0.0))
        ecc = float(par.get("ECC",0.0))
        pulsar.orbits.append(KeplerianOrbit(pb,asini,t0,ecc,om))
    return pulsar
        
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
    
        
        
        

        
