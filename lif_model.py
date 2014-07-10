from brian import *

class LIFmodel:
	"""
	TODO
	"""
	Vt = -57*mV 	 # threshold
	refractory = 2*ms # clamping time
	Ek = -90*mV 	 # reset potential
	E0 = -65*mV 	 # resting potential
	Eexc = 0*mV
	Einh = -80*mV
	taum = 20*ms
	taupeakexc = 0 # TODO set default vals
	tau1exc = 5*ms # TODO just for testing!
	tau2exc = 0
	taupeakinh = 0
	tau1inh = 1*ms # TODO just for testing!
	tau2inh = 0
	# TODO Gexc, Ginh fix eq
	# Ibg = AC*sin(inj_freq*t)+DC : 1
	dynamics = Equations('''
		dV/dt = ((E0 - V) + Gexc * (Eexc - V) + Ginh * (Einh - V) + Ibg) / taum : volt
		dGexc/dt = -Gexc/tau1exc : 1
		dGinh/dt = -Ginh/tau1inh : 1
		Ibg = AC*exp(inj_freq*t)+DC : volt
		AC : volt
		DC : volt
		inj_freq : 1''', \
		E0=E0, Eexc=Eexc, Einh=Einh, taum=taum, tau1exc=tau1exc, tau1inh=tau1inh) # TODO change Gexc, Ginh
