from brian import *

class LIFmodel:
	"""
	TODO
	"""
	Vt = -55*mV 	  # threshold
	refractory = 2*ms # clamping time
	Ek = -65*mV 	  # reset potential
	E0 = -65*mV 	  # resting potential
	Eexc = 0*mV
	Einh = -80*mV
	taum = 20*ms
	tauexc = 5*ms
	tauinh = 10*ms
	dynamics = Equations('''
		dV/dt = ((E0 - V) + Gexc * (Eexc - V) + Ginh * (Einh - V)) / taum : volt
		dGexc/dt = -Gexc/tauexc : 1
		dGinh/dt = -Ginh/tauinh : 1''', \
		E0=E0, Eexc=Eexc, Einh=Einh, taum=taum, tauexc=tauexc, tauinh=tauinh)
