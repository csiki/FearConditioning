from brian import *
from inspect import isfunction

from context import *
from lif_model import *
from current_injection import *
from conditional_stimulus import *

class BasalAmygdala:
	"""
	Represent the functioning of the basal amygdala, and its relevance
	in fear conditioning and extinction.
	"""
	N  = 4000
	Ne = 3400
	Ni = 600
	#Nb = 0 # TODO not needed ?
	dt = 0 # TODO set compile time default values
	BtoEcurr_inj = CurrentInjection(85*pA, 330*pA)
	BtoIcurr_inj = CurrentInjection(110*pA, 220*pA)
	neuron_model = LIFmodel()
	neuro_modulators = [1.0] # vector of functions, or float numbers (use isfunction())
	CTXs = dir()
	exc_neurons = None
	inh_neurons = None
	bg_neurons  = None
	curr_ctx = None
	c_eq = '''dc/dt = -c/tauc + A * delta(tpre)''' # TODO !!! tauc, tauh, A, B ??
	h_eq = '''dh/dt = -h/tauh + B * delta(tpre)'''
	# TODO weights paramters ??
	wmax = 0 # TODO ?
	wmin = 0
	
	def __init__(self, network_size = N, **connection_prob):
		"""
		TODO
		"""
		# connection probability default values
		conn_prob = { 'pEE': 0.01, 'pEI': 0.15, 'pIE': 0.15, 'pII': 0.1 }
		for c in connection_prob.keys():
			conn_prob[c] = connection_prob[c]
		
		# neuron group initaliziation
		# TODO
	
	
	def add_context(self, ctx):
		"""
		TODO
		"""
		self.CTXs[ctx.name] = ctx
	
	def switch_context(self, to_ctx):
		"""
		TODO
		"""
		CTXs[to_ctx.name] = to_ctx
		self.curr_ctx = to_ctx
			
	def add_neuromodulator(self, neuro_mod):
		"""
		TODO
		"""
		neuro_modulators.append(neuro_mod)
	
	def present_stimulus(self, CS, US='extinction'):
		"""
		TODO
		"""
		pass
	
	def run(self, runtime):
		"""
		TODO
		"""
		pass
	
