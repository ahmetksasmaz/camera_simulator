class Pixel:
    def __init__(self, i, j, dx, dy, z_o, lx, ly):
        self.i = i
        self.j = j
        self.dx = dx
        self.dy = dy
        self.z_o = z_o
        self.lx = lx
        self.ly = ly
    
    def get_pixel_discrete_resolution(self):
        return 1, 1

    def get_pixel_continous_resolution(self):
        return self.lx, self.ly
    
    def get_pixel_area(self):
        return self.lx * self.ly
    
    def get_pixel_discrete_coordinates(self):
        return self.i, self.j
    
    def get_pixel_continuous_coordinates(self):
        return self.dx, self.dy
    
    def query_point_in_pixel(self, x, y):
        return self.dx - self.lx/2 <= x <= self.dx + self.lx/2 and self.dy - self.lx/2 <= y <= self.dy + self.ly/2
    
    def get_pixel_corners(self):
        return ((self.dx - self.lx/2, self.dy - self.lx/2, self.z_o),
                (self.dx - self.lx/2, self.dy + self.lx/2, self.z_o),
                (self.dx + self.lx/2, self.dy + self.lx/2, self.z_o),
                (self.dx + self.lx/2, self.dy - self.lx/2, self.z_o))