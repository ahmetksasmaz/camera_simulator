from Pixel import Pixel

class Sensor:
    def __init__(self, w, h, z_o, lx, ly, ox, oy):
        self.w = w
        self.h = h
        self.z_o = z_o
        self.lx = lx
        self.ly = ly
        self.ox = ox
        self.oy = oy

        self.pixels = {}

        self.kx_max = int((self.w - self.lx)/(2*(self.lx + self.ox)) - 1/2)
        self.kx_min = int(-(self.w - self.lx)/(2*(self.lx + self.ox)) - 1/2)

        self.ky_max = int((self.h - self.ly)/(2*(self.ly + self.oy)) - 1/2)
        self.ky_min = int(-(self.h - self.ly)/(2*(self.ly + self.oy)) - 1/2)

        kx = self.kx_min
        ky = self.ky_min
        while kx <= self.kx_max:
            while ky <= self.ky_max:
                self.pixels[(kx, ky)] = Pixel(kx, ky, (kx+1/2)*(self.lx + self.ox), (ky+1/2)*(self.ly + self.oy), self.z_o, self.lx, self.ly)
                ky += 1
            ky = self.ky_min
            kx += 1
    
    def get_sensor_discrete_resolution(self):
        return self.kx_max - self.kx_min + 1, self.ky_max - self.ky_min + 1

    def get_sensor_continous_resolution(self):
        return self.w, self.h
    
    def get_sensor_area(self):
        return self.w * self.h
    
    def query_point_in_sensor(self, x, y):
        return -self.w/2 <= x <= self.w/2 and -self.h/2 <= y <= self.h/2
    
    def query_point_in_sensor_pixels(self, x, y):
        for pixel in self.pixels.values():
            if pixel.query_point_in_pixel(x, y):
                return True
        return False
    
    def get_sensor_corners(self):
        return ((-self.w/2, -self.h/2, self.z_o),
                (-self.w/2, self.h/2, self.z_o),
                (self.w/2, self.h/2, self.z_o),
                (self.w/2, -self.h/2, self.z_o))