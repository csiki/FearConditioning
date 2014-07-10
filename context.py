from brian import *

class Context:
	"""
	TODO
	"""
	name = ''
	spiking_rate = 300*Hz
	lrate_pot   = 16e-4
	lrate_depot = 16e-4
	weight = 0 # TODO mx?
	associated_neurons = None
	poisson_gen = None
	poisson_con = None
	c = None # TODO mx?
	h = None
	
	def __init__(self, name, associated_neurons, weight=0.05, spiking_rate=spiking_rate):
		"""
		TODO
		"""
		self.name = name
		self.weight = weight
		self.spiking_rate = spiking_rate
		self.associated_neurons = associated_neurons
		self.poisson_gen = PoissonGroup(len(associated_neurons), rates=0*Hz)
		self.poisson_con = IdentityConnection(self.poisson_gen, associated_neurons, \
			'Gexc', weight=weight) # TODO mx? brian.ConnectionMatrix?
	
	def update_weight(self, neuro_modulators, wmax, wmin, CSpresent=False):
		"""
		TODO
		"""
		pass # TODO
	
	# TODO def activate, deactivate
	def activate(self):
		"""
		TODO
		"""
		self.poisson_gen.rate = self.spiking_rate
	
	def deactivate(self):
		"""
		TODO
		"""
		self.poisson_gen.rate = 0*Hz
