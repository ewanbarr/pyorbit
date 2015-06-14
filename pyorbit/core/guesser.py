import numpy as np

class Guesser(object):
    def __init__(self,pdata):
        self.pdata = pdata

    def guess_pb(self,min_pb,max_pb,ntrials):
        pb = 86400.0/np.linspace(1/max_pb,1/min_pb,ntrials)
        r = np.array([roughness(self.pdata,i) for i in pb])
        return pb[r.argmin()]
        
    def guess_p0(self):
        p0 = self.pdata["p0"]
        return p0.min()+(p0.max()-p0.min())/2.
    

def roughness(x,pb,s=1):
    x = np.copy(x)
    x["t"]%=pb
    x = np.sort(x,order="t")
    a = np.diff(x["p0"])**2
    b = np.diff(x["t"])**2
    e = x["perr"][:-1]*x["perr"][1:]
    return sum(a/(s**2+b))

def simple_roughness(x,pb):
    x = np.copy(x)
    x["t"]%=pb
    x = np.sort(x,order="t")
    return sum(np.diff(x["p0"])**2)

