from brian import *

class ConditionalStimulis:
	"""
	TODO
	"""
	ctx_name = ''
	phasic_drive = 50*ms # time of the stimulus
	spiking_rate = 500*Hz
	
	def __init__(self, ctx_name):
		"""
		TODO
		"""
		self.ctx_name = ctx_name
