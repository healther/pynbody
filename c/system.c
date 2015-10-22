

#include <stdio.h>
#include <math.h>
#include <stdlib.h>
#include "mtwist.h"

struct Force
{
    double x;
    double y;
    double z;
};

struct Particle
{
    struct Force position;
    struct Force velocity;
    struct Force acceleration;
    double mass;
};

struct Force dist(struct Force px, struct Force py){
    struct Force d;
    d.x = px.x-py.x;
    d.y = px.y-py.y;
    d.z = px.z-py.z;
    return d;
}

double abs2(struct Force f){
    return f.x*f.x + f.y*f.y + f.z*f.z;
}

void calcforce(struct Particle* px, struct Particle py){
    struct Force sep = dist(px->position,py.position);
    double d2 = abs2(sep);
    d2 = -px->mass*py.mass/d2/sqrt(d2);
    px->acceleration.x += d2*sep.x;
    px->acceleration.y += d2*sep.y;
    px->acceleration.z += d2*sep.z;
}

int main(){
    //srand(42424242);
    mt_seed();
    int n = 10000;
    struct Particle particles[n];
    struct Force acc = {0.,0.,0.};

    for (int i = 0; i < n; ++i)
    {
        // particles[i].position.x = (double)rand() / (double)RAND_MAX ;
        // particles[i].position.y = (double)rand() / (double)RAND_MAX ;
        // particles[i].position.z = (double)rand() / (double)RAND_MAX ;
        // particles[i].velocity.x = (double)rand() / (double)RAND_MAX ;
        // particles[i].velocity.y = (double)rand() / (double)RAND_MAX ;
        // particles[i].velocity.z = (double)rand() / (double)RAND_MAX ;
        // particles[i].acceleration.x = 0.;
        // particles[i].acceleration.y = 0.;
        // particles[i].acceleration.z = 0.;
        particles[i].position.x = mt_ldrand()-.5;
        particles[i].position.y = mt_ldrand()-.5;
        particles[i].position.z = mt_ldrand()-.5;
        particles[i].velocity.x = mt_ldrand()-.5;
        particles[i].velocity.y = mt_ldrand()-.5;
        particles[i].velocity.z = mt_ldrand()-.5;
        particles[i].acceleration.x = 0.;
        particles[i].acceleration.y = 0.;
        particles[i].acceleration.z = 0.;
        particles[i].mass = mt_ldrand() ;
    }

    for (int i = 0; i < n; ++i)
    {
        for (int j = 0; j < n; ++j)
        {
            if(i!=j){
                calcforce(&particles[i], particles[j]);
            }
        }
    }

    for (int i = 0; i < n; ++i)
    {
        acc.x += particles[i].acceleration.x;
        acc.y += particles[i].acceleration.y;
        acc.z += particles[i].acceleration.z;
    }

    printf("%1.16e %1.16e %1.16e\n", acc.x, acc.y, acc.z);
}




