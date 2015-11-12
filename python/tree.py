
import math
import particle

class Tree:
    def __init__(self, theta = 0.2):
        self.nparticles = 0
        self.maxdepth = 1
        self.theta = theta
        self.root = Node(r=[0.,0.,0.], size=1., theta=self.theta)
        self.particles = []

    def addParticle(self, newpart):
        self.particles.append(newpart)
        self.root.addParticle(newpart)
        self.nparticles += 1

    def calculateForce(self):
        self.root.generateMultipole()
        interactions = 0
        for p in self.particles:
            interactions += self.root.calculateForce(p)
        return interactions

    def calculateFMM(self):
        interactions = 0
        self.root.generateMultipole()
        stack = [(self.root, self.root)]
        while stack:
        # for A,B in stack:
            A, B = stack.pop()
            if A is None and B is None:
                continue
            interactions += 1
            if A.size>B.size:
                for a in filter(None, A.subnodes):
                    stack.append(self._interact(a,B))
            else:
                for b in filter(None, B.subnodes):
                    stack.append(self._interact(A,b))
        self.root.evaluateMultipole()
        return interactions

    def _interact(self, A, B):
        if 1==A.nparticles and 1==B.nparticles:
            # leaf leaf interaction calculate directly
            return(self._P2P(A,B))
        elif 1==A.nparticles:
            # source is leaf
            return(self._L2M(A,B))
        elif 1==B.nparticles:
            # sink is leave
            return(self._M2L(A,B))
        elif self._MAC2(A,B):
            # nodes far away
            return(self._M2M(A,B))
        else:
            return (A, B)

    def _P2P(self, A, B):
        if A is not B:
            B.particle.calculateForce(A.particle)
        return (None, None)

    def _MAC2(self, A, B):
        d2 = sum((ar-br)*(ar-br) for ar, br in zip(A.r, B.r))
        return (A.size+B.size)*(A.size+B.size) < d2 * self.theta

    def _MAC(self, A, B):
        d2 = sum((ar-br)*(ar-br) for ar, br in zip(A.r, B.r))
        return A.size*A.size < d2 * self.theta

    def _M2M(self, A, B):
        B.pseudoparticle.calculateForce(A.pseudoparticle)        
        return (None, None)

    def _L2M(self, A, B):
        if self._MAC(B,A):
            B.pseudoparticle.calculateForce(A.particle)
            return (None, None)
        else:
            return (A,B)  
    
    def _M2L(self, A, B):
        if self._MAC(A,B):
            B.particle.calculateForce(A.pseudoparticle) 
            return(None, None)
        return(A,B)       

class Node:
    def __init__(self, r, size, theta = 0.7):
        self.r = r
        self.size = size
        self.theta = theta
        self.particle = None
        self.pseudoparticle = particle.Particle(r=[0.,0.,0.],v=[0.,0.,0.],m=0.)
        self.nparticles = 0
        #self.particles = []
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
        
        #self.particles.append(newpart)
        self.nparticles += 1
        #self.updatePseudoParticle(newpart)

    def findSubNode(self, part):
        rel = [x<y for (x,y) in zip(self.r, part.r)]
        return sum(rel[i]*2**i for i in range(3))

    def createSubNode(self, idx):
        rel = [idx&1, (idx&2)//2, (idx&4)//4]
        newr = [x-.25*self.size+.5*self.size*y for (x,y) in zip(self.r, rel)]
        if self.subnodes[idx] is None:
            self.subnodes[idx] = Node(newr, self.size/2., theta = self.theta)

    def updatePseudoParticle(self, part):
        self.pseudoparticle.absorbParticle(part)

    def generateMultipole(self):
        self.pseudoparticle = particle.Particle(r=[0.,0.,0.],v=[0.,0.,0.],m=0.)
        if self.nparticles == 0:
            print("error")
        elif self.nparticles == 1:
            self.pseudoparticle.r[:] = self.particle.r
            self.pseudoparticle.v[:] = self.particle.v
            self.pseudoparticle.a[:] = self.particle.a
            self.pseudoparticle.m = self.particle.m
        else:
            for subnode in self.subnodes :
                if subnode is not None:
                    subnode.generateMultipole()
                    for i in range(3):
                        self.pseudoparticle.r[i] += subnode.pseudoparticle.r[i] * subnode.pseudoparticle.m
                        self.pseudoparticle.v[i] += subnode.pseudoparticle.v[i] * subnode.pseudoparticle.m
                        self.pseudoparticle.a[i] += subnode.pseudoparticle.a[i] * subnode.pseudoparticle.m
                    self.pseudoparticle.m += subnode.pseudoparticle.m
            self.pseudoparticle.r = [cm/self.pseudoparticle.m for cm in self.pseudoparticle.r]
            self.pseudoparticle.v = [cm/self.pseudoparticle.m for cm in self.pseudoparticle.v]
            self.pseudoparticle.a = [cm/self.pseudoparticle.m for cm in self.pseudoparticle.a]

    def evaluateMultipole(self):
        for s in filter(None, self.subnodes):
            # push to subnodes
            for i in range(3):
                s.pseudoparticle.a[i] += self.pseudoparticle.a[i]/self.pseudoparticle.m*s.pseudoparticle.m
            s.evaluateMultipole()
        if self.nparticles is 1:
            # push to particle
            for i in range(3):
                self.particle.a[i] += self.pseudoparticle.a[i]

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

