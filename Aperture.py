import math

class Aperture:
    def __init__(self, z_a, d):
        self.z_a = z_a
        self.d = d
    
    def get_aperture_diameter(self):
        return self.d
    
    def get_aperture_radius(self):
        return self.d/2
    
    def get_aperture_area(self):
        return math.pi*(self.d/2)**2
    
    def query_point_in_aperture(self, x, y):
        return x**2 + y**2 <= (self.d/2)**2