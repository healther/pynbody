
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

    void calcacceleration(Particle p) {
        Vector3D sep = r-p.r;
        double d2 = sep*sep;
        Vector3D acc = Vector3D(0.,0.,0.);
        for (int i = 0; i < 3; ++i)
        {
            acc[i] = -p.m * sep[i] / d2 / sqrt(d2);
        }
        a += acc;
    }
} ;