
#include <vector>
#include <random>
#include <iostream>
#include <fstream>
#include <string>
#include <sstream>


#include "tree.h"
#include "particle.h"


class System {
public:
    long n;
    std::vector<Particle> particles;

    System() { }

    System(const char * fname) {
        std::ifstream fin(fname);

        std::vector< std::vector<std::string> >   result;
        std::string                line;
        // iterates over all lines in file fname
        while(std::getline(fin,line))
        {
            std::stringstream ss(line);
            std::string item;
            std::vector<std::string> particlestr;
            // splits the line into the single double values
            while (std::getline(ss, item, ' ')) {
                particlestr.push_back(item);
            }
            result.push_back(particlestr);
        }

        for (std::vector< std::vector<std::string> >::iterator line = result.begin()+1; line != result.end(); ++line)
        {
            double m = std::stod((*line)[0].c_str());
            Vector3D r = Vector3D(
                std::stod((*line)[1].c_str()),
                std::stod((*line)[2].c_str()),
                std::stod((*line)[3].c_str())
                );
            Vector3D v = Vector3D(
                std::stod((*line)[4].c_str()),
                std::stod((*line)[5].c_str()),
                std::stod((*line)[6].c_str())
                );
            Vector3D a = Vector3D(
                std::stod((*line)[7].c_str()),
                std::stod((*line)[8].c_str()),
                std::stod((*line)[9].c_str())
                );
            particles.push_back(Particle(m,r,v));
        }
    }

    System(long _n) {
        int seed = 42424242;
        std::mt19937 g1(seed);

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

    int run() {
        int interactions = 0;
        for (std::vector<Particle>::iterator pi = particles.begin(); pi != particles.end(); ++pi)
        {
            for (std::vector<Particle>::iterator pj = particles.begin(); pj != particles.end(); ++pj)
            {
                if(pi!=pj){
                    pi->calculateForce(*pj);
                    interactions++;
                }
            }
        }
        return interactions;
    }

    int run_tree(double theta) {
        Tree t = Tree(theta);
        for (std::vector<Particle>::iterator p = particles.begin(); p != particles.end(); ++p)
        {
            t.addParticle(*p);
        }
        t.generateMultipole();
        int interactions = t.calculateForce();
        return interactions;
    }
} ;

