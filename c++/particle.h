
#include "vector3d.h"

class Particle {
public:
    double m;
    Vector3D r, v, a;

    Particle() {}

    Particle(double _m, Vector3D _r, Vector3D _v){
        m = _m;
        r = _r;
        v = _v;
        a = Vector3D(0.,0.,0.);
    }

    void calcforce(Particle p) {
        Vector3D sep = r-p.r;
        double d2 = sep*sep;
        d2 = -p.m*m / d2 / sqrt(d2);
        for (int i = 0; i < 3; ++i)
        {
            a[i] += d2 * sep[i] ;
        }
    }
} ;