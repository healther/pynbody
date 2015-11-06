
import time
import random

import tree
import particle

class System():
    def __init__(self, n=100, seed=42424242):
        self.n = n
        self.seed = seed
        random.seed(self.seed)

        self.particles = []
        for _ in range(self.n):
            self.particles.append(
                    particle.Particle(
                        r = [random.random()-.5,
                            random.random()-.5,
                            random.random()-.5
                            ],
                        v = [random.random()-.5,
                            random.random()-.5,
                            random.random()-.5
                            ],
                        m = 1. #random.random()
                        )
                )

    def run(self):
        for px in self.particles:
            for py in self.particles:
                if px!=py:
                    px.calculateForce(py)
        print(len(self.particles)*(len(self.particles)-1))

    def run_tree(self, theta=0.2):
        self.t = tree.Tree(theta=theta)
        for p in self.particles:
            self.t.addParticle(p)

        print(self.t.calculateForce())
        #for p in self.particles:
        #    print(p.a)

    def check(self):
        f = [0.,0.,0.]
        for p in self.particles:
            for i in range(3):
                f[i] += p.a[i]
        print(f)
        return f

def compare(n=100, theta=.5):
    s1 = System(n=n)
    s1.run()
    s1.check()
    s2 = System(n=n)
    s2.run_tree(theta=theta)
    s2.check()
    daaverage = 0.
    for s1p, s2p in zip(s1.particles, s2.particles):
        da = [a1-a2 for a1,a2 in zip(s1p.a, s2p.a)]
        da2 = sum(d*d for d in da)
        a2 = sum(d*d for d in s1p.a)
        daaverage += da2/a2
    print(daaverage/len(s1.particles))
    return s1,s2

if __name__ == '__main__':
    n = 10
    t0 = time.time()
    s1 = System(n=n)
    s1.run()
    s1.check()
    t1 = time.time()
    print("BruteForce n={} in: {} seconds".format(n, t1-t0))
    t2 = time.time()
    s2 = System(n=n)
    s2.run_tree()
    s2.check()
    t3 = time.time()
    print("BruteForce n={} in: {} seconds".format(n, t3-t2))
    daaverage = 0.
    das = []
    for s1p, s2p in zip(s1.particles, s2.particles):
        da = [a1-a2 for a1,a2 in zip(s1p.a, s2p.a)]
        da2 = sum(d*d for d in da)
        a2 = sum(d*d for d in s1p.a)
        print(da2/a2)
        das.append(da2/a2)
        daaverage += da2/a2
    print(daaverage/len(s1.particles))