#ifndef H_PARTICLE
#define H_PARTICLE


#include "vector3d.h"

class Particle {
public:
    double m;
    Vector3D r, v, a;

    Particle() {}

    Particle(double const _m, Vector3D const _r, Vector3D const _v){
        m = _m;
        r = _r;
        v = _v;
        a = Vector3D(0.,0.,0.);
    }

    void calculateForce(Particle const & p) {
        // Vector3D sep = r-p.r;
        // double d2 = sep*sep;
        double d2 = (r-p.r)*(r-p.r);
        if (d2<1E-15)
        {
            std::cout << "fail" << std::endl;
            return ;
        }
        d2 = -p.m*m / d2 / sqrt(d2);
        for (int i = 0; i < 3; ++i)
        {
            a[i] += d2 * (r[i]-p.r[i]) ;
        }
    }
} ;


#endif
