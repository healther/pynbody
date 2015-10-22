
#include <vector>
#include <random>

#include "particle.h"

int seed = 42424242;
std::mt19937 g1(seed);

class System {
public:
    long n;
    std::vector<Particle> particles;

    System() { }

    System(long _n) {
        n = _n;
        for (int i = 0; i < n; ++i)
        {
            double m = (double)g1()/(double)g1.max();
            Vector3D r = Vector3D(
                    (double)g1()/(double)g1.max() - .5,
                    (double)g1()/(double)g1.max() - .5,
                    (double)g1()/(double)g1.max() - .5);
            Vector3D v = Vector3D(
                    (double)g1()/(double)g1.max() - .5,
                    (double)g1()/(double)g1.max() - .5,
                    (double)g1()/(double)g1.max() - .5);
            particles.push_back(Particle(m,r,v));
        }
    }

    void run() {
        for (std::vector<Particle>::iterator pi = particles.begin(); pi != particles.end(); ++pi)
        {
            for (std::vector<Particle>::iterator pj = particles.begin(); pj != particles.end(); ++pj)
            {
                if(pi!=pj){
                    pi->calcacceleration(*pj);
                }
            }
        }
    }
} ;

