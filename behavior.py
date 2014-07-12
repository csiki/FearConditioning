#Behavior simulation script

from brian import *

def fear_conditioning(amygdala, stim_fear, stim_ext, ctx_fear, ctx_ext):
	"""
	Script function to run the fear conditioning experiment
	"""	
	amygdala.switch_context(200, 40, ctx_fear)

	for i in range(5):
		amygdala.run(100*ms, report='stdout')
		amygdala.present_stimulus(stim_fear, stim_ext, report='stdout')

	amygdala.run(100*ms)

	amygdala.switch_context(ctx_ext)

	for i in range(5):
		amygdala.run(100*ms, report='stdout')
		amygdala.present_stimulus(stim_ext, stim_fear, report='stdout')

	amygdala.run(100*ms)


def fear_renewal(amygdala, stim_fear, stim_ext, ctx_fear, ctx_ext):
	"""
	Script function to run the fear conditioning experiment
	"""	
	amygdala.switch_context(ctx_fear)

	for i in range(5):
		amygdala.run(100*ms, report='stdout')
		amygdala.present_stimulus(stim_fear, stim_ext, report='stdout')

	amygdala.run(100*ms)

	amygdala.switch_context(ctx_ext)

	for i in range(5):
		amygdala.run(100*ms, report='stdout')
		amygdala.present_stimulus(stim_ext, stim_fear, report='stdout')

	amygdala.run(100*ms)

	amygdala.switch_context(ctx_fear) 

	amygdala.present_stimulus(stim_fear, stim_ext, report='stdout')
     
