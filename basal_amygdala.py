from brian import *
from inspect import isfunction

from context import *
from lif_model import *
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
	bg_exc_curr_inj = None
	bg_inh_curr_inj = None
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
		
		self.network.add(self.Cee, self.Cei, self.Cie, self.Cii)
		
		# current injection using contexts
		self.bg_exc_curr_inj = self.create_context('background_exc', self.exc_neurons, 1.0, 0.08)
		self.bg_inh_curr_inj = self.create_context('background_inh', self.inh_neurons, 1.0, 0.12)
		self.bg_exc_curr_inj.activate()
		self.bg_inh_curr_inj.activate()
	
	def create_context(self, name, associated_neurons=None, sparseness=0.2, weight=0.05, spiking_rate=300*Hz):
		"""
		Creates a context with the given name, and connects a poisson
		group to 20% of the excitation neurons. Also adds the context
		to CTXs, indexed by name.
		"""
		if associated_neurons == None:
			associated_neurons = self.exc_neurons
		
		if sparseness < 1.0:
			beg = randint(0, floor(len(associated_neurons) * (1 - sparseness)))
			end = int(beg + floor(len(associated_neurons) * sparseness))
			associated_neurons = associated_neurons[beg:end]
		
		tmpctx = Context(name, associated_neurons, weight, spiking_rate)
		self.network.add(tmpctx.poisson_gen, tmpctx.poisson_con)
		
		return tmpctx
	
	def create_cs(self, associated_neurons, weight=0.05, spiking_rate=500*Hz, duration=50*ms):
		"""
		TODO
		"""
		tmpstim = ConditionalStimulus(associated_neurons, duration, \
			spiking_rate, weight)
		self.network.add(tmpstim.poisson_con, tmpstim.poisson_gen)
		
		return tmpstim
	
	def add_context(self, ctx): # TODO not sure if needed
		"""
		TODO
		"""
		self.CTXs[ctx.name] = ctx
	
	def switch_context(self, to_ctx):
		"""
		TODO
		"""
		if self.curr_ctx != None:
			self.curr_ctx.deactivate()
		self.curr_ctx = to_ctx
		self.curr_ctx.activate()
			
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
		# TODO ctx?
	
	# TODO def add_monitor or whatever
	

###############################################################
##################### MAIN ####################################
###############################################################

# basal init
btest = BasalAmygdala(200, 40)

# context, cs init
ctx_ext = btest.create_context('extinction')
ctx_fear = btest.create_context('fear')
btest.add_context(ctx_ext)
btest.add_context(ctx_fear)
stim_ext = btest.create_cs(ctx_ext.associated_neurons)
stim_fear = btest.create_cs(ctx_fear.associated_neurons)

# monitor init
spiking_all = SpikeMonitor(btest.neurons)
voltage_all = StateMonitor(btest.neurons[195:205], 'V', record=True)
poprate_exc = PopulationRateMonitor(btest.exc_neurons, bin=100*ms)
poprate_inh = PopulationRateMonitor(btest.inh_neurons, bin=100*ms)
btest.network.add(voltage_all, spiking_all, poprate_exc, poprate_inh)

# run
btest.switch_context(ctx_fear)

for i in range(5):
	btest.run(100*ms)
	stim_fear.activate()
	btest.run(50*ms)
	stim_fear.deactivate()

btest.run(100*ms)

# plots
subplot(221)
plot(poprate_exc.times, poprate_exc.rate)
subplot(222)
plot(poprate_inh.times, poprate_inh.rate)
subplot(223)
raster_plot(spiking_all)
subplot(224)
voltage_all.plot()
show()
