from brian import *
from misc import normalvariate_vec

class Context:
    """
    Represents a context. Basically different contexts mean different
    US-CS or just CS conditioning.
    """
    name = ''
    spiking_rate = 300*Hz
    weight = None
    associated_neurons = None
    poisson_gen = None
    poisson_con = None
    
    def __init__(self, name, associated_neurons, spiking_rate=spiking_rate, weight=None):
        """
        Initialise a context, creating PoissonGroup connected to
        associated_neurons. Plasticity possible.
        """
        self.name = name
        self.spiking_rate = spiking_rate
        self.associated_neurons = associated_neurons
        self.poisson_gen = PoissonGroup(len(associated_neurons), rates=0*Hz)
        
        if weight == None:
            # plastic synapses
            weight = normalvariate_vec(1, 0.1, len(associated_neurons))
            self.poisson_con = Synapses(self.poisson_gen, associated_neurons, \
                pre='Gexc_post += w', model='w : 1')
            self.poisson_con.connect_one_to_one(self.poisson_gen, associated_neurons)
            self.poisson_con.w[:,:] = weight
        else:
            # static connections
            self.poisson_con = IdentityConnection(self.poisson_gen, associated_neurons, \
                'Gexc', weight=weight)
        
    
    def update_weight(self, delta, t_modulator, neuro_modulators, wextreme, lrate_pot):
        """
        Updates the weights between the PoissonGroup and associated_neurons.
        """
        m = 1 # TODO neuromodulators
        self.poisson_con.w[:,:] += delta * lrate_pot * m * abs(self.poisson_con.w[:,:] - wextreme)
    
    def activate(self):
        """
        Activate the PoissonGroup.
        """
        self.poisson_gen.rate = self.spiking_rate
    
    def deactivate(self):
        """
        Deactivate the PoissonGroup - no firing.
        """
        self.poisson_gen.rate = 0*Hz
