from brian import *

class Context:
	"""
	TODO
	"""
	name = ''
	associated_neurons = None
	spiking_rate = 300*Hz
	learning_rate = 16e-4
	
	def __init__(self, name, associated_neurons):
		"""
		TODO
		"""
		self.name = name
		self.associated_neurons = associated_neurons
