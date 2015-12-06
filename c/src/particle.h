#ifndef PARTICLE_H
#define PARTICLE_H

#include <math.h>
#include "force.h"


struct Particle
{
    struct Force position;
    struct Force velocity;
    struct Force acceleration;
    double mass;
};

void calculateForcePP(struct Particle* px, const struct Particle* py){
    struct Force sep = dist(px->position,py->position);
    double d2 = abs2(sep);
    d2 = -px->mass*py->mass/d2/sqrt(d2);
    px->acceleration.x += d2*sep.x;
    px->acceleration.y += d2*sep.y;
    px->acceleration.z += d2*sep.z;
}

void setzero(struct Particle* px){
    px->position.x = 0.;
    px->position.y = 0.;
    px->position.z = 0.;
    px->velocity.x = 0.;
    px->velocity.y = 0.;
    px->velocity.z = 0.;
    px->acceleration.x = 0.;
    px->acceleration.y = 0.;
    px->acceleration.z = 0.;
    px->mass = 0.;
}

void setpart(struct Particle* px, const struct Particle* py){
    px->position.x = py->position.x;
    px->position.y = py->position.y;
    px->position.z = py->position.z;
    px->velocity.x = py->velocity.x;
    px->velocity.y = py->velocity.y;
    px->velocity.z = py->velocity.z;
    px->acceleration.x = py->acceleration.x;
    px->acceleration.y = py->acceleration.y;
    px->acceleration.z = py->acceleration.z;
    px->mass = py->mass;
}

void absorbpart(struct Particle* px, const struct Particle* py){
    double invmass = 1./(px->mass + py->mass);
    // double invmass = 1.;
    px->position.x = invmass*(px->mass*px->position.x+py->mass*py->position.x);
    px->position.y = invmass*(px->mass*px->position.y+py->mass*py->position.y);
    px->position.z = invmass*(px->mass*px->position.z+py->mass*py->position.z);
    px->velocity.x = invmass*(px->mass*px->velocity.x+py->mass*py->velocity.x);
    px->velocity.y = invmass*(px->mass*px->velocity.y+py->mass*py->velocity.y);
    px->velocity.z = invmass*(px->mass*px->velocity.z+py->mass*py->velocity.z);
    px->acceleration.x = invmass*(px->mass*px->acceleration.x+py->mass*py->acceleration.x);
    px->acceleration.y = invmass*(px->mass*px->acceleration.y+py->mass*py->acceleration.y);
    px->acceleration.z = invmass*(px->mass*px->acceleration.z+py->mass*py->acceleration.z);
    px->mass = px->mass + py->mass;
}

void reducepart(struct Particle* px){
    px->position.x /= px->mass;
    px->position.y /= px->mass;
    px->position.z /= px->mass;
    px->velocity.x /= px->mass;
    px->velocity.y /= px->mass;
    px->velocity.z /= px->mass;
    px->acceleration.x /= px->mass;
    px->acceleration.y /= px->mass;
    px->acceleration.z /= px->mass;
}

#endif /* PARTICLE_H */