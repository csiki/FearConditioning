#Behavior simulation script

from brian import *

def fear_conditioning(amygdala, stim_fear, stim_ext, ctx_fear, ctx_ext):
	"""
	Script function to run the fear conditioning experiment
	"""	
	amygdala.switch_context(ctx_fear)

	for i in range(5):
		amygdala.run(100*ms)
		stim_fear.activate()
		stim_ext.activate()
		amygdala.run(50*ms)
		stim_fear.deactivate()
		stim_ext.deactivate()

	amygdala.run(100*ms)

	amygdala.switch_context(ctx_ext)

	for i in range(5):
		amygdala.run(100*ms)
		stim_fear.activate()
		stim_ext.activate()
		amygdala.run(50*ms)
		stim_fear.deactivate()
		stim_ext.deactivate()

	amygdala.run(100*ms)