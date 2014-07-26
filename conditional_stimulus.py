from brian import *
from misc import normalvariate_vec

class ConditionalStimulus:
    """
    Can be a CS or CS-US coupling - depends on the contexts to which
    it is connected.
    """
    weight = None
    associated_neurons = None
    duration = 50*ms
    spiking_rate = 500*Hz
    poisson_gen = None
    poisson_con = None
    
    def __init__(self, associated_neurons, duration=duration, spiking_rate=spiking_rate):
        """
        Creates a PoissonGroup connected to the associated_neurons
        one-to-one. associated_neurons should come from the
        corresponding context.
        """
        self.weight = normalvariate_vec(1, 0.1, len(associated_neurons))
        self.duration = duration
        self.spiking_rate = spiking_rate
        self.associated_neurons = associated_neurons
        self.poisson_gen = PoissonGroup(len(associated_neurons), rates=0*Hz)
        
        # plastic synapses
        weight = normalvariate_vec(1, 0.1, len(associated_neurons))
        self.poisson_con = Synapses(self.poisson_gen, associated_neurons, \
            pre='Gexc_post += w', model='w : 1')
        self.poisson_con.connect_one_to_one(self.poisson_gen, associated_neurons)
        self.poisson_con.w[:,:] = weight
    
    def activate(self):
        """
        Activates the PoissonGroup.
        """
        self.poisson_gen.rate = self.spiking_rate
    
    def deactivate(self):
        """
        Deactivates the PoissonGroup - no firing.
        """
        self.poisson_gen.rate = 0*Hz
    
    def update_weight(self, delta, t_modulator, neuro_modulators, wextreme, lrate_pot):
        """
        Updates the weights between the PoissonGroup and associated_neurons.
        """
        m = 1 # TODO neuromodulators
        self.poisson_con.w[:,:] += delta * lrate_pot * m * abs(self.poisson_con.w[:,:] - wextreme)
        
        
