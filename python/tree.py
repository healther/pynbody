
import math
import particle

class Tree:
    def __init__(self, theta = 0.2):
        self.nparticles = 0
        self.theta = theta
        self.root = Node(r=[0.,0.,0.], size=1., theta=self.theta)
        self.particles = []

    def addParticle(self, newpart):
        self.particles.append(newpart)
        self.root.addParticle(newpart)
        self.nparticles += 1

    def calculateForce(self):
        #self.root.generateMultipole()
        interactions = 0
        for p in self.particles:
            interactions += self.root.calculateForce(p)
        return interactions


class Node:
    def __init__(self, r, size, theta = 0.7):
        self.r = r
        self.size = size
        self.theta = theta
        self.particle = None
        self.pseudoparticle = particle.Particle(r=[0.,0.,0.],v=[0.,0.,0.],m=0.)
        self.nparticles = 0
        self.particles = []
        self.subnodes = 8*[None]

    def addParticle(self, newpart):
        if self.nparticles is 0:
            self.particle = newpart
        elif self.nparticles is 1:
            idx = self.findSubNode(self.particle)
            self.createSubNode(idx)
            self.subnodes[idx].addParticle(self.particle)
            self.particle = None

            idx = self.findSubNode(newpart)
            self.createSubNode(idx)
            self.subnodes[idx].addParticle(newpart)
        else:
            idx = self.findSubNode(newpart)
            self.createSubNode(idx)
            self.subnodes[idx].addParticle(newpart)
        
        self.particles.append(newpart)
        self.nparticles += 1
        self.updatePseudoParticle(newpart)

    def findSubNode(self, part):
        rel = [x<y for (x,y) in zip(self.r, part.r)]
        return sum(rel[i]*2**i for i in range(3))

    def createSubNode(self, idx):
        rel = [idx&1, idx&2, idx&4]
        newr = [x-.25*self.size+.5*self.size*y for (x,y) in zip(self.r, rel)]
        if self.subnodes[idx] is None:
            self.subnodes[idx] = Node(newr, self.size/2., theta = self.theta)

    def updatePseudoParticle(self, part):
        self.pseudoparticle.absorbParticle(part)

    def generateMultipole(self):
        if self.nparticles == 0:
            print("error")
            self.pseudoparticle.r[:] = [0.,0.,0.]
            self.pseudoparticle.v[:] = [0.,0.,0.]
            self.pseudoparticle.a[:] = [0.,0.,0.]
            self.pseudoparticle.m = 0.
        elif self.nparticles == 1:
            self.pseudoparticle.r[:] = self.particles[0].r
            self.pseudoparticle.v[:] = self.particles[0].v
            self.pseudoparticle.a[:] = self.particles[0].a
            self.pseudoparticle.m = self.particles[0].m
        else:
            self.pseudoparticle.r[:] = [0.,0.,0.]
            self.pseudoparticle.v[:] = [0.,0.,0.]
            self.pseudoparticle.a[:] = [0.,0.,0.]
            self.pseudoparticle.m = 0.
            for subnode in self.subnodes :
                if subnode is not None:
                    subnode.generateMultipole()
                    for i in range(3):
                        self.pseudoparticle.r[i] += subnode.pseudoparticle.r[i]
                        self.pseudoparticle.v[i] += subnode.pseudoparticle.v[i]
                        self.pseudoparticle.a[i] += subnode.pseudoparticle.a[i]
                    self.pseudoparticle.m += subnode.pseudoparticle.m
            self.pseudoparticle.r = [cm/self.pseudoparticle.m for cm in self.pseudoparticle.r]

    def calculateForce(self, part):
        d = [ri-rj for (ri,rj) in zip(part.r, self.pseudoparticle.r)]
        # d = [ri-rj for (ri,rj) in zip(part.r, self.r)]
        d2 = sum(dd*dd for dd in d)
        

        if self.size**2 < self.theta**2*d2 or 1==self.nparticles:
            if d2<1E-15:
                # self interaction
                return 0
            else:
                part.calculateForce(self.pseudoparticle)
                return 1

        else:
            interactions = 0
            for subnode in self.subnodes:
                if subnode is not None:
                    interactions += subnode.calculateForce(part)
            return interactions

