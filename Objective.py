import numpy as np

class Lens:
    def __init__ (self, f):
        self.f = f
        self.rtm = np.ndarray((2, 2))
        self.rtm[0, 0] = 1
        self.rtm[0, 1] = 0
        self.rtm[1, 0] = -1/f
        self.rtm[1, 1] = 1
    
    def get_focal_length(self):
        return self.f
    
    def get_rtm(self):
        return self.rtm

class Propagation:
    def __init__(self, d):
        self.d = d
        self.rtm = np.ndarray((2, 2))
        self.rtm[0, 0] = 1
        self.rtm[0, 1] = d
        self.rtm[1, 0] = 0
        self.rtm[1, 1] = 1
    
    def get_distance(self):
        return self.d
    
    def get_rtm(self):
        return self.rtm

class PropagationLens: # Rays coming from the left, first propagated then refracted
    def __init__(self, propagation, lens):
        self.propagation = propagation
        self.lens = lens
        self.rtm = np.matmul(self.lens.get_rtm(), self.propagation.get_rtm())
    
    def get_rtm(self):
        return self.rtm

class Objective:
    def __init__(self, propagation_lenses):
        self.propagation_lenses = propagation_lenses
        self.rtm = np.identity(2)
        for propagation_lens in self.propagation_lenses:
            self.rtm = np.matmul(propagation_lens.get_rtm(), self.rtm)
    
    def get_rtm(self):
        return self.rtm
    
    def total_propagation(self):
        total_propagation = 0
        for propagation_lens in self.propagation_lenses:
            total_propagation += propagation_lens.propagation.get_distance()
        return total_propagation