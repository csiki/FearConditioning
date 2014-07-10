from brian import *

class CurrentInjection:
	"""
	TODO
	"""
	AC = 0
	DC = 0
	freq = 0
	
	def __init__(self, AC, DC, freq):
		"""
		TODO
		"""
		self.AC = AC
		self.DC = DC
		self.freq = freq
