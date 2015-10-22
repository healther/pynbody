
import random

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
                        m = random.random()
                        )
                )

    def run(self):
        for px in self.particles:
            for py in self.particles:
                if px!=py:
                    px.calcacceleration(py)


if __name__ == '__main__':
    s = System(n=10000)
    s.run()
    f = [0.,0.,0.]
    for p in s.particles:
        for i in range(3):
            f[i] += p.a[i]*p.m
    print(f)

