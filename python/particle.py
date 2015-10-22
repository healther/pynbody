
import math



class Particle():
    def __init__(self, 
            r = [0., 0., 0.],
            v = [0., 0., 0.],
            m = 1.):
        self.r = r
        self.v = v
        self.a = [0., 0., 0.]
        self.m = m

    def calcacceleration(self, particle):
        assert(isinstance(particle, Particle))
        assert(particle!=self)
        d = [ri-rj for (ri,rj) in zip(self.r, particle.r)]
        d2 = sum(dd*dd for dd in d)
        a = [-particle.m*dd/d2/math.sqrt(d2) for dd in d]
        for i in range(3):
            self.a[i] += a[i]

    def integrate(self, dt):
        assert(self.a!=[0.,0.,0.])
        for i in range(3):
            self.r[i] += self.v[i] * dt
            self.v[i] += self.a[i] * dt
            self.a[i] = 0.