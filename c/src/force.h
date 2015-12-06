#ifndef FORCE_H
#define FORCE_H

struct Force
{
    double x;
    double y;
    double z;
};

struct Force dist(const struct Force px, const struct Force py){
    struct Force d;
    d.x = px.x-py.x;
    d.y = px.y-py.y;
    d.z = px.z-py.z;
    return d;
}

double dist2(const struct Force px, const struct Force py){
    double d2 = 0.;
    d2 += (px.x-py.x)*(px.x-py.x);
    d2 += (px.y-py.y)*(px.y-py.y);
    d2 += (px.z-py.z)*(px.z-py.z);
    return d2;
}

double abs2(const struct Force f){
    return f.x*f.x + f.y*f.y + f.z*f.z;
}


#endif /* FORCE_H */

