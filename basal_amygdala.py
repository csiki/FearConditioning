
class BasalAmygdala:
	"""
	Represent the functioning of the basal amygdala, and its relevance
	in fear conditioning and extinction.
	"""
	N  = 0
	Ne = 0
	Ni = 0
	Nb = 0
	exc_neurons = None
	inh_neurons = None
	bg_neurons  = None
	curr_ctx = None
	neuron_model = None
	BtoEcurr_inj = None
	BtoIcurr_inj = None
	c_eq = None
	h_eq = None
	neuro_modulators = []
	CTXs = set()
	
	def __init__(neuronal_model, **connection_prob):
		"""
		"""
		pass
	
	def add_context(ctx):
		"""
		"""
		pass
	
	def switch_context(to_ctx=None):
		"""
		"""
		pass
	
	def present_stimulus(CS, US='extinction'):
		"""
		"""
		pass
	
	def run(runtime):
		"""
		"""
		pass
	
	
