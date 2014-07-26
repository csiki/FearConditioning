from random import normalvariate
from numpy import zeros

def normalvariate_vec(mu, sigma, size):
    """
    Returns a vector of normal variate random value.
    """
    vec = zeros(size)
    for e in vec:
        e = normalvariate(mu, sigma)
    
    return vec
