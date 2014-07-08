from brian import *

class LIFmodel:
	"""
	TODO
	"""
	dynamics = '''
	dV/dt = ((E0 - V) + Gexc * (Eexc - V) + Ginh * (Einh - V)) / taum : volt
	'''
	threshold = -57*mV
	clamp_time = 2*ms
	Ek = -90*mV
	E0 = -65*mV
	Eexc = 0*mV
	Einh = -80*mV
	Gexc_eq = ''' ''' # TODO not needed, include in dynamics
	Ginh_eq = ''' ''' # TODO not needed, include in dynamics
	taum = 20*ms
	taupeakexc = 0 # TODO set default vals
	tau1exc = 0
	tau2exc = 0
	taupeakinh = 0
	tau1inh = 0
	tau2inh = 0
