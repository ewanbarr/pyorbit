import numpy as np
import logging
from scipy.optimize import minimize
from functools import wraps

logging.basicConfig(level=logging.DEBUG)

TWOPI = np.pi * 2
C = 299792458.0
DAY_2_SEC = 86400.0

def log_args(func):
    @wraps(func)
    def wrapped(*args,**kwargs):
        args_str = ", ".join([repr(i) for i in args])
        kwargs_str = ", ".join(["%s=%s"%(a,repr(b)) for a,b in kwargs.items()])
        logging.debug("%s(%s,%s)"%(func.__name__,args_str,kwargs_str))
        return func(*args,**kwargs)
    return wrapped

@log_args
def mean_anomaly(pb,t):
    """
    Calculate the Mean Anomaly.
    
    Inputs:
    pb - orbital period
    t - time since periapsis
    
    Notes:
    Units of period and t are arbitrary but must
    be consistent
    """
    return (TWOPI * t / pb)%TWOPI

@log_args
def eccentric_anomaly(M,ecc):
    """
    Calculate the eccentric anomaly from the mean anomaly.
    
    Inputs:
    M   - mean anomaly
    ecc - eccentricity
    
    Notes:
    As sine is transendental, we use scipy.optimize.minimize
    and Kepler's equation to determine E
    """
    func = lambda E: abs( M - ( E - ecc * np.sin( E ) ) )    
    solution = minimize(func,1.0)
    return solution["x"][0]

@log_args
def true_anomaly(E,ecc):
    """
    Calculate the true anomaly from the eccentric anomaly.
    
    Inputs:
    E   - eccentric anomaly
    ecc - eccentricity
    """
    return 2*np.arctan2(np.sqrt(1+ecc)*np.sin(E/2.),
                        np.sqrt(1-ecc)*np.cos(E/2.))

@log_args
def true_anomaly_from_orbit(pb,ecc,t):
    """
    Calculate the true anomaly from orbital parameters
    
    Inputs:
    pb  - binary period
    ecc - eccentricity
    t   - time since periapsis
    
    Notes:
    This is an abstraction to calculate the true anomaly
    without having to explicitly calculate mean and 
    eccentric anomalies.
    """
    mean_anom = mean_anomaly(pb,t)
    ecc_anom  = eccentric_anomaly(mean_anom,ecc)
    true_anom = true_anomaly(ecc_anom,ecc)
    return true_anom
    
@log_args
def los_velocity(pb, asini, t0, ecc, om, t):
    """
    Calculate the l.o.s. velocity.
    
    Inputs:
    pb    - binary period (s)
    asini - projected semi-major axis (m)
    t0    - epoch of periapsis (s)
    ecc   - eccentricity
    om    - longitude of periastron (radians)
    t     - epoch of measurement (s)
    
    Notes:
    Will convert t to time since last periapsis
    """
    t = t-t0
    true_anom = true_anomaly_from_orbit(pb,ecc,t)
    angle  = (np.cos( true_anom + om ) + ecc * np.cos(om))
    return -(TWOPI/pb) * asini * angle / np.sqrt( 1-ecc**2 )
    
@log_args
def los_velocity_circ(pb, asini, t0, t):
    """
    Calculate l.o.s. velocity for a circular orbit.
    
    Inputs:
    pb    - binary period (s)
    asini - projected semi-major axis (m)
    t0    - epoch of periapsis (s)
    t     - epoch of measurement (s)
    
    Notes:
    Epoch of measurement [t] can be an array to improve performance.
    """
    # ecc = 0 so Mean == Eccentric == True
    return -(TWOPI/pb) * asini * np.cos(mean_anomaly(pb,t-t0))
       

@log_args
def los_acceleration(pb, asini, t0, ecc, om, t):
    """
    Calculate the l.o.s. acceleration.
    
    Input:
    pb    - binary period (s) 
    asini - projected semi-major axis (m)
    t0    - epoch of periapsis (s)
    ecc   - eccentricity 
    om    - longitude of periastron (radians) 
    t     - epoch of measurement (s) 
    
    Notes:
    Will convert t to time since last periapsis
    """
    t = t-t0
    true_anom = true_anomaly_from_orbit(pb,ecc,t)
    angle = (np.sin(om + true_anom)) * (1 + ecc * np.cos(true_anom) )**2
    return (TWOPI/pb)**2 * asini * angle / np.sqrt( 1-ecc**2 )

@log_args
def los_acceleration_circ(pb, asini, t0, t):
    """
    Calculate the l.o.s. acceleration for a circular orbit.
    
    Inputs:
    pb    - binary period (s) 
    asini - projected semi-major axis (m) 
    t0    - epoch of periapsis (s)
    t     - epoch of measurement (s)
    
    Notes:
    Epoch of measurement [t] can be an array to improve performance.
    """
    # ecc = 0 so Mean == Eccentric == True
    return -(TWOPI/pb)**2 * asini * np.sin(mean_anomaly(pb,t-t0))

@log_args
def period(p0,p1,pb,asini,t0,ecc,om,t,pepoch):
    """
    Calculate apparent pulse period, given los velocity.
    
    Inputs:
    p0 - pulsar spin period (s)
    p1 - pulsar period derivative (s/s)
    pb - orbital period (s)
    asini - projected semi-major axis (m)
    t0 - epoch of periapsis (s)
    ecc - eccentricity 
    om - longitude of periastron (rad)
    t - measurement epoch (s)
    pepoch - epoch of period measurement (s)
    """
    p_actual = p0 + p1*(t-pepoch)
    velocity = los_velocity(pb, asini, t0, ecc, om, t)
    p_apparent = (C / (C+velocity)) * p_actual
    return p_apparent

def period_circ(p0,p1,pb,asini,t0,t,pepoch):
    """
    Calculate apparent pulse period, given los velocity.

    Inputs:
    p0 - pulsar spin period (s)
    p1 - pulsar period derivative (s/s)
    pb - orbital period (s)
    asini - projected semi-major axis (m)
    t0 - epoch of periapsis (s)
    t - measurement epoch (s)
    pepoch - epoch of period measurement (s)
    """
    p_actual = p0 + p1*(t-pepoch)
    velocity = los_velocity_circ(pb, asini, t0, t)
    p_apparent = (C / (C+velocity)) * p_actual
    return p_apparent
    
