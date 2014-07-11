from brian import *
from inspect import isfunction

from context import *
from lif_model import *
from conditional_stimulus import *
from behavior import *

class BasalAmygdala:
	"""
	Represent the functioning of the basal amygdala, and its relevance
	in fear conditioning and extinction.
	"""
	N    = 4000
	Nexc = 3400
	Ninh = 600
	plastic_inh = True
	dt = 0.1*ms
	neuron_model = LIFmodel()
	neuro_modulators = [1.0] # vector of functions, or float numbers (use isfunction())
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
	lrate_pot = 1e-4
	lrate_depot = -16e-4
	wmax = 1
	wmin = 0
	
	def __init__(self, Nexc=Nexc, Ninh=Ninh, neuron_model=neuron_model, dt=dt, plastic_inh = plastic_inh, **connection_prob):
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
		self.plastic_inh = plastic_inh
		
		# neuron group initaliziation
		self.neurons = NeuronGroup(self.N, model=self.neuron_model.dynamics, \
			threshold=self.neuron_model.Vt, reset=self.neuron_model.Ek, \
			refractory=self.neuron_model.refractory)
		self.neurons.V = uniform(self.neuron_model.E0, self.neuron_model.Vt, self.N)
		
		self.exc_neurons = self.neurons.subgroup(self.Nexc)
		self.inh_neurons = self.neurons.subgroup(self.Ninh)
		
		self.network.add(self.neurons)
		
		# plastic connection I->E equations
		stdp_eqns = ''' w : 1
		dApre/dt=-Apre/Apre_tau : 1
		dApost/dt=-Apost/Apost_tau : 1
		Apre_tau : ms
		Apost_tau : ms
		Apre0 : 1
		Apost0 : 1
		eta : 1
		wmax : 1
		'''
		pre_eqns = 'Ginh_post += w; Apre+=Apre0; w+=-Apost*eta; w=clip(w,0,wmax);'
		post_eqns = 'Apost+=Apost0; w+=Apre*eta; wsyn=clip(w,0,wmax)'
		
		# group connectivity
		self.Cee = Synapses(self.exc_neurons, target=self.exc_neurons, \
			pre='Gexc_post += 0.1')
		self.Cei = Synapses(self.exc_neurons, target=self.inh_neurons, \
			pre='Gexc_post += 0.1')
		if plastic_inh:
			self.Cie = Synapses(self.inh_neurons, target=self.exc_neurons, \
				pre=pre_eqns, post=post_eqns, model=stdp_eqns) # plastic
		else:
			self.Cie = Synapses(self.inh_neurons, target=self.exc_neurons, \
				pre='Ginh_post += 4.0') # not plastic
		self.Cii = Synapses(self.inh_neurons, target=self.inh_neurons, \
			pre='Ginh_post += 4.0')
		self.Cee.connect_random(sparseness=self.conn_prob['pEE'])
		self.Cei.connect_random(sparseness=self.conn_prob['pEI'])
		self.Cie.connect_random(sparseness=self.conn_prob['pIE'])
		self.Cii.connect_random(sparseness=self.conn_prob['pII'])
		
		# plastic connection I->E parameters
		self.Cie.w = 4.0
		self.Cie.wmax = 6.0
		self.Cie.Apre_tau = 40*ms
		self.Cie.Apost_tau = 20*ms
		self.Cie.Apre0 = 1.0
		self.Cie.Apost0 = 0.5
		self.Cie.eta = 2.0
		
		self.network.add(self.Cee, self.Cei, self.Cie, self.Cii)
		
		# background current injection using contexts
		self.bg_exc_curr_inj = self.create_context('background_exc', \
			self.exc_neurons, 1.0, 300*Hz, 0.08)
		self.bg_inh_curr_inj = self.create_context('background_inh', \
			self.inh_neurons, 1.0, 300*Hz, 0.18)
		self.bg_exc_curr_inj.activate()
		self.bg_inh_curr_inj.activate()
	
	def create_context(self, name, associated_neurons=None, sparseness=0.2, spiking_rate=300*Hz, weight=None):
		"""
		Creates a context with the given name, and connects a poisson
		group to [sparseness]% of the excitation neurons. Also adds the
		context to CTXs, indexed by name.
		"""
		if associated_neurons == None:
			associated_neurons = self.exc_neurons
		
		if sparseness < 1.0:
			beg = randint(0, floor(len(associated_neurons) * (1 - sparseness)))
			end = int(beg + floor(len(associated_neurons) * sparseness))
			associated_neurons = associated_neurons[beg:end]
		
		tmpctx = Context(name, associated_neurons, spiking_rate, weight)
		self.network.add(tmpctx.poisson_gen, tmpctx.poisson_con)
		
		return tmpctx
	
	def create_cs(self, associated_neurons, spiking_rate=500*Hz, duration=50*ms):
		"""
		TODO
		"""
		tmpstim = ConditionalStimulus(associated_neurons, duration, \
			spiking_rate)
		self.network.add(tmpstim.poisson_con, tmpstim.poisson_gen)
		
		return tmpstim
	
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
	
	def present_stimulus(self, CScurr, CSother, **runargs):
		"""
		TODO
		"""
		# constants
		tauc = 10*ms
		tauh = 10*ms
		binsize = 1*ms
		
		# create monitors
		sm_cscurr  = SpikeMonitor(CScurr.poisson_gen)
		sm_csother = SpikeMonitor(CSother.poisson_gen)
		sm_ctxcurr = SpikeMonitor(self.curr_ctx.poisson_gen)
		self.network.add(sm_cscurr, sm_csother, sm_ctxcurr)
		curr_time = self.neurons.t[0]
		
		# present stimulus
		CScurr.activate()
		CSother.activate()
		self.network.run(CScurr.duration, **runargs)
		CScurr.deactivate()
		CSother.deactivate()
		
		# create refs to spiketimes
		dic_cscurr = sm_cscurr.spiketimes
		dic_csother = sm_csother.spiketimes
		dic_ctxcurr = sm_ctxcurr.spiketimes
		
		# substract first element from arrays
		for i in range(len(dic_cscurr)):
			dic_cscurr[i] -= curr_time
		for i in range(len(dic_csother)):
			dic_csother[i] -= curr_time
		for i in range(len(dic_ctxcurr)):
			dic_ctxcurr[i] -= curr_time
		
		# histograms & convolution
		c_exp = array([exp(-x*ms/tauc) for x in arange(0., CScurr.duration / ms, 1.)])
		h_exp = array([exp(-x*ms/tauh) for x in arange(0., CScurr.duration / ms, 1.)])
		arr_curr  = zeros(len(dic_cscurr))
		arr_other = zeros(len(dic_csother))
		
		for i in range(len(dic_cscurr)):
			arr_curr[i] = dot(convolve(c_exp, histogram(dic_cscurr[i], \
				int(CScurr.duration / ms), range=(0., float(CScurr.duration / second)))[0]), \
				convolve(h_exp, histogram(dic_ctxcurr[i], \
				int(CScurr.duration / ms), range=(0., float(CScurr.duration / second)))[0]))
		for i in range(len(dic_csother)):
			arr_other[i] = sum(convolve(c_exp, histogram(dic_csother[i], \
				int(CSother.duration / ms), range=(0., float(CSother.duration / second)))[0]))
			
		# update weights
		CScurr.update_weight(arr_curr, 0, self.neuro_modulators, self.wmax, self.lrate_pot)
		CSother.update_weight(arr_other, 0, self.neuro_modulators, self.wmin, self.lrate_depot)
		self.curr_ctx.update_weight(arr_curr, 0, self.neuro_modulators, self.wmax, self.lrate_pot)
		
		# remove monitors
		self.network.remove(sm_cscurr, sm_csother, sm_ctxcurr)
		
	
	def run(self, runtime, **args):
		"""
		Runs the system for the given time.
		"""
		self.network.run(runtime, **args)
	


###############################################################
##################### MAIN ####################################
###############################################################
if __name__ == '__main__':
	
	# set seed
	seed(1000)
	
	# basal init
	btest = BasalAmygdala(200, 40, plastic_inh=True)

	# context, cs init
	ctx_ext = btest.create_context('extinction')
	ctx_fear = btest.create_context('fear')
	stim_ext = btest.create_cs(ctx_ext.associated_neurons)
	stim_fear = btest.create_cs(ctx_fear.associated_neurons)

	# monitor init
	spiking_all = SpikeMonitor(btest.neurons)
	voltage_all = StateMonitor(btest.neurons[195:205], 'V', record=True)
	poprate_exc = PopulationRateMonitor(ctx_fear.associated_neurons, bin=10*ms)
	poprate_inh = PopulationRateMonitor(ctx_ext.associated_neurons, bin=10*ms)
	btest.network.add(voltage_all, spiking_all, poprate_exc, poprate_inh)

	# run
	#fear_conditioning(btest, stim_fear, stim_ext, ctx_fear, ctx_ext)
	fear_renewal(btest, stim_fear, stim_ext, ctx_fear, ctx_ext)

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
