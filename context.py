from brian import *
from misc import normalvariate_vec

class Context:
	"""
	TODO
	"""
	name = ''
	spiking_rate = 300*Hz
	#~ lrate_pot   = 16e-4
	#~ lrate_depot = -16e-4 # TODO needed?
	weight = None # TODO mx?
	associated_neurons = None
	poisson_gen = None
	poisson_con = None
	
	def __init__(self, name, associated_neurons, spiking_rate=spiking_rate, weight=None):
		"""
		TODO
		"""
		self.name = name
		self.spiking_rate = spiking_rate
		self.associated_neurons = associated_neurons
		self.poisson_gen = PoissonGroup(len(associated_neurons), rates=0*Hz)
		
		if weight == None:
			# plastic synapses
			weight = normalvariate_vec(1, 0.1, len(associated_neurons))
			self.poisson_con = Synapses(self.poisson_gen, associated_neurons, \
				pre='Gexc_post += w', model='w : 1')
			self.poisson_con.connect_one_to_one(self.poisson_gen, associated_neurons)
			self.poisson_con.w[:,:] = weight
		else:
			# static connections
			self.poisson_con = IdentityConnection(self.poisson_gen, associated_neurons, \
				'Gexc', weight=weight)
		
	
	def update_weight(self, delta, t_modulator, neuro_modulators, wextreme, lrate_pot):
		"""
		TODO
		"""
		m = 1 # TODO neuro_modulators ?
		self.poisson_con.w[:,:] += delta * lrate_pot * m * abs(self.poisson_con.w[:,:] - wextreme)
	
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
