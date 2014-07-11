from random import normalvariate
from numpy import zeros

def normalvariate_vec(mu, sigma, size):
	vec = zeros(size)
	for e in vec:
		e = normalvariate(mu, sigma)
	
	return vec
