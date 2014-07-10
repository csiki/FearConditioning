from brian import *

class ConditionalStimulus:
	"""
	TODO
	"""
	weight = 0
	duration = 50*ms
	spiking_rate = 500*Hz
	lrate_pot   = 16e-4
	lrate_depot = 16e-4
	poisson_gen = None
	poisson_con = None
	c = None # TODO mx?
	h = None
	
	def __init__(self, associated_neurons, duration=duration, spiking_rate=spiking_rate, weight=weight):
		"""
		TODO
		"""
		self.weight = weight
		self.duration = duration
		self.spiking_rate = spiking_rate
		self.poisson_gen = PoissonGroup(len(associated_neurons), rates=0*Hz)
		self.poisson_con = IdentityConnection(self.poisson_gen, \
			associated_neurons, 'Gexc', weight=weight)
	
	def activate(self):
		"""
		TODO
		"""
		self.poisson_gen.rate = self.spiking_rate
		# TODO activate for duration!
	
	def deactivate(self):
		"""
		TODO
		"""
		self.poisson_gen.rate = 0*Hz
	
	def update_weight(self, neuro_modulators, wmax, wmin):
		"""
		TODO
		"""
		# TODO
