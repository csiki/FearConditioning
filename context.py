from brian import *

class Context:
	"""
	TODO
	"""
	name = ''
	associated_neurons = None # TODO needed?
	spiking_rate = 300*Hz
	lrate_pot   = 16e-4
	lrate_depot = 16e-4
	weight = 0 # TODO mx?
	poisson_gen = None
	poisson_con = None
	c = None # TODO mx?
	h = None
	
	def __init__(self, name, associated_neurons, weight=0.05, spiking_rate=spiking_rate):
		"""
		TODO
		"""
		self.name = name
		self.associated_neurons = associated_neurons
		self.spiking_rate = spiking_rate
		self.poisson_gen = PoissonGroup(len(self.associated_neurons), \
			rates=self.spiking_rate)
		self.poisson_con = IdentityConnection(self.poisson_gen, self.associated_neurons, \
			'Gexc', weight=weight) # TODO mx? brian.ConnectionMatrix?
	
	def update_weight(self, neuro_modulators, wmax, wmin, CSpresent=False):
		"""
		TODO
		"""
		pass # TODO
	
	# TODO def activate, deactivate
