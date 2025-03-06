from Pixel import Pixel
from Sensor import Sensor
from Aperture import Aperture
from Objective import Lens, Propagation, PropagationLens, Objective
import numpy as np
import math

class Camera:
    def __init__(self, w, h, lx, ly, ox, oy, z_o, z_a, d, z_s, objective):
        self.z_o = z_o
        self.z_s = z_s
        self.z_a = z_a
        self.sensor = Sensor(w, h, z_o, lx, ly, ox, oy)
        self.aperture = Aperture(z_a, d)
        self.objective = objective
        self.z_e = self.objective.total_propagation()
        self.ABCD = self.objective.get_rtm()
        self.A = self.ABCD[0, 0]
        self.B = self.ABCD[0, 1]
        self.C = self.ABCD[1, 0]
        self.D = self.ABCD[1, 1]

    def query_sensor_ray_valid(self, ray):
        if not self.sensor.query_point_in_sensor(ray.x, ray.y):
            return False
        
        intersection_x = ray.x + ray.dx*(self.sensor.z_o - ray.z)/ray.dz
        intersection_y = ray.y + ray.dy*(self.sensor.z_o - ray.z)/ray.dz

        if not self.aperture.query_point_in_aperture(intersection_x, intersection_y):
            return False
        
        return True

    def query_sensor_pixel_ray_valid(self, ray):
        for pixel in self.sensor.pixels:
            if not pixel.query_point_in_pixel(ray.x, ray.y):
                return False
        
        intersection_x = ray.x + ray.dx*(self.sensor.z_o - ray.z)/ray.dz
        intersection_y = ray.y + ray.dy*(self.sensor.z_o - ray.z)/ray.dz

        if not self.aperture.query_point_in_aperture(intersection_x, intersection_y):
            return False
        
        return True
    
    def trace_ray_from_ray(self, sensor_pixel_ray):
        outgoing_ray_x = self.A*sensor_pixel_ray.x + self.A*(self.z_s - sensor_pixel_ray.z)*sensor_pixel_ray.dx/sensor_pixel_ray.dz + self.B*sensor_pixel_ray.dx/(1-self.dy**2)**0.5
        outgoing_ray_y = self.A*sensor_pixel_ray.y + self.A*(self.z_s - sensor_pixel_ray.z)*sensor_pixel_ray.dy/sensor_pixel_ray.dz + self.B*sensor_pixel_ray.dy/(1-self.dx**2)**0.5
        outgoing_ray_z = self.z_e
        outgoing_ray_dx = self.C*sensor_pixel_ray.x + self.C*(self.z_s - sensor_pixel_ray.z)*sensor_pixel_ray.dx/sensor_pixel_ray.dz + self.D*sensor_pixel_ray.dx/(1-self.dy**2)**0.5
        outgoing_ray_dy = self.C*sensor_pixel_ray.x + self.C*(self.z_s - sensor_pixel_ray.z)*sensor_pixel_ray.dx/sensor_pixel_ray.dz + self.D*sensor_pixel_ray.dx/(1-self.dy**2)**0.5
        outgoing_ray_dz = (1-outgoing_ray_dx**2-outgoing_ray_dy**2)**0.5
    
    def trace_ray_from_sensor_pixel_and_aperture_points(self, o_x, o_y, a_x, a_y):
        K = (1 - (self.z_s - self.z_o)/(self.z_a - self.z_o))

        outgoing_ray_x = o_x*(self.A*(1-K) - self.B) + a_x*(self.A*K + self.B)
        outgoing_ray_y = o_y*(self.A*(1-K) - self.B) + a_y*(self.A*K + self.B)
        outgoing_ray_z = self.z_e
        outgoing_ray_dx = o_x*(self.C*(1-K) - self.D) + a_x*(self.C*K + self.D)
        outgoing_ray_dy = o_y*(self.C*(1-K) - self.D) + a_y*(self.C*K + self.D)
        outgoing_ray_dz = (1-outgoing_ray_dx**2-outgoing_ray_dy**2)**0.5