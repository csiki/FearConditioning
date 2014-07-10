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
	N    = 4000
	Nexc = 3400
	Ninh = 600
	dt = 0.1*ms
	BtoEcurr_inj = CurrentInjection(85*pA, 330*pA, 0.5*Hz)
	BtoIcurr_inj = CurrentInjection(110*pA, 220*pA, 13*Hz)
	neuron_model = LIFmodel()
	neuro_modulators = [1.0] # vector of functions, or float numbers (use isfunction())
	CTXs = {}
	network = Network()
	neurons = None
	exc_neurons = None
	inh_neurons = None
	Cee = None
	Cei = None
	Cie = None
	Cii = None
	curr_ctx = None
	wmax = 1
	wmin = 0
	
	def __init__(self, Nexc=Nexc, Ninh=Ninh, neuron_model=neuron_model, dt=dt, **connection_prob):
		"""
		TODO
		"""
		# connection probability default values
		self.conn_prob = { 'pEE': 0.01, 'pEI': 0.15, 'pIE': 0.15, 'pII': 0.1 }
		for c in connection_prob.keys():
			self.conn_prob[c] = connection_prob[c]
		
		# attribute settings
		self.Nexc = Nexc
		self.Ninh = Ninh
		self.N = Nexc + Ninh
		self.neuron_model = neuron_model
		
		# neuron group initaliziation
		self.neurons = NeuronGroup(self.N, model=self.neuron_model.dynamics, \
			threshold=self.neuron_model.Vt, reset=self.neuron_model.Ek, \
			refractory=self.neuron_model.refractory)
		self.neurons.V = uniform(self.neuron_model.E0, self.neuron_model.Vt, self.N)
		
		self.exc_neurons = self.neurons.subgroup(self.Nexc)
		self.inh_neurons = self.neurons.subgroup(self.Ninh)
		
		self.network.add(self.neurons)
		
		# group connectivity
		# TODO what with Gexc?
		self.Cee = Synapses(self.exc_neurons, target=self.exc_neurons, \
			pre='Gexc_post += 0.1')
		self.Cei = Synapses(self.exc_neurons, target=self.inh_neurons, \
			pre='Gexc_post += 0.1')
		self.Cie = Synapses(self.inh_neurons, target=self.exc_neurons, \
			pre='Ginh_post += 4')
		self.Cii = Synapses(self.inh_neurons, target=self.inh_neurons, \
			pre='Ginh_post += 4')
		self.Cee.connect_random(sparseness=self.conn_prob['pEE'])
		self.Cei.connect_random(sparseness=self.conn_prob['pEI'])
		self.Cie.connect_random(sparseness=self.conn_prob['pIE'])
		self.Cii.connect_random(sparseness=self.conn_prob['pII'])
		
		#~ self.Cee = Connection(self.exc_neurons, self.exc_neurons, 'Gexc', \
			#~ sparseness=self.conn_prob['pEE'])
		#~ self.Cei = Connection(self.exc_neurons, self.inh_neurons, 'Gexc', \
			#~ sparseness=self.conn_prob['pEI'])
		#~ self.Cie = Connection(self.inh_neurons, self.exc_neurons, 'Ginh', \
			#~ sparseness=self.conn_prob['pIE'])
		#~ self.Cii = Connection(self.inh_neurons, self.inh_neurons, 'Ginh', \
			#~ sparseness=self.conn_prob['pII'])
		
		#~ self.network.add(self.Cee, self.Cei, self.Cie, self.Cii)
		
		# background input parameters init
		#~ self.exc_neurons.AC = self.BtoEcurr_inj.AC
		#~ self.exc_neurons.DC = self.BtoEcurr_inj.DC
		#~ self.exc_neurons.inj_freq = self.BtoEcurr_inj.freq
		#~ self.inh_neurons.AC = self.BtoIcurr_inj.AC
		#~ self.inh_neurons.DC = self.BtoIcurr_inj.DC
		#~ self.inh_neurons.inj_freq = self.BtoIcurr_inj.freq
		
	
	def create_context(self, name, associated_neurons=exc_neurons, sparseness=0.2, weight=0.05, spiking_rate=10*Hz):
		"""
		Creates a context with the given name, and connects a poisson
		group to 20% of the excitation neurons. Also adds the context
		to CTXs, indexed by name.
		"""
		if associated_neurons == None:
			associated_neurons = self.exc_neurons
		tmpctx = Context(name, associated_neurons, sparseness, weight)
		self.CTXs[name] = tmpctx
		
		self.network.add(tmpctx.poisson_gen, tmpctx.poisson_con)
		
		return tmpctx
	
	def add_context(self, ctx):
		"""
		TODO
		"""
		self.CTXs[ctx.name] = ctx
	
	def switch_context(self, to_ctx):
		"""
		TODO
		"""
		self.CTXs[to_ctx.name] = to_ctx
		self.curr_ctx = to_ctx
			
	def add_neuromodulator(self, neuro_mod):
		"""
		TODO
		"""
		self.neuro_modulators.append(neuro_mod)
	
	def present_stimulus(self, CS, US='extinction'):
		"""
		TODO
		"""
		pass
	
	def run(self, runtime):
		"""
		TODO
		"""
		self.network.run(runtime, report='stdout')
	
	# TODO def add_monitor or whatever
	

btest = BasalAmygdala(200, 40)
bgctx_exc = btest.create_context('background_exc', btest.exc_neurons, 1.0, 0.02, 0.1)
bgctx_inh = btest.create_context('background_inh', btest.inh_neurons, 1.0, 0.2, 13)
#~ ext = btest.create_context('extinction')
#~ btest.switch_context(ext)


spiking_all = SpikeMonitor(btest.neurons)
pmon = StateMonitor(btest.neurons, 'V', record=True)
btest.network.add(pmon, spiking_all)
btest.run(1*second)

#~ subplot(311)
#~ raster_plot(Ms_inh)
subplot(211)
raster_plot(spiking_all)
subplot(212)
pmon.plot()
show()
