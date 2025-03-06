class Ray:
    def __init__(self, x, y, z, dx, dy, dz):
        self.x = x
        self.y = y
        self.z = z
        self.dx = dx / (dx**2 + dy**2 + dz**2)**0.5
        self.dy = dy / (dx**2 + dy**2 + dz**2)**0.5
        self.dz = dz / (dx**2 + dy**2 + dz**2)**0.5