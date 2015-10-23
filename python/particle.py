
import math



class Particle():
    def __init__(self, 
            r = [0., 0., 0.],
            v = [0., 0., 0.],
            m = 0.):
        self.r = r
        self.v = v
        self.a = [0., 0., 0.]
        self.m = m

    def absorbParticle(self, part):
        self.r[:] = [(ri*self.m + rj*part.m)/(self.m+part.m) for ri, rj in zip(self.r, part.r)] 
        self.v[:] = [(vi*self.m + vj*part.m)/(self.m+part.m) for vi, vj in zip(self.v, part.v)] 
        self.a[:] = [(ai*self.m + aj*part.m)/(self.m+part.m) for ai, aj in zip(self.a, part.a)] 
        self.m = self.m + part.m

    def calculateForce(self, particle):
        assert(isinstance(particle, Particle))
        assert(particle!=self)
        d = [ri-rj for (ri,rj) in zip(self.r, particle.r)]
        d2 = sum(dd*dd for dd in d)
        if d2<1E-14:
            return
        a = [-particle.m*self.m*dd/d2/math.sqrt(d2) for dd in d]
        for i in range(3):
            self.a[i] += a[i]

    def integrate(self, dt):
        assert(self.a!=[0.,0.,0.])
        for i in range(3):
            self.r[i] += self.v[i] * dt
            self.v[i] += self.a[i] * dt
            self.a[i] = 0.