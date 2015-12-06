

#include <stdio.h>
#include <math.h>
#include <stdlib.h>
#include "mtwist.h"

#include "force.h"
#include "particle.h"
#include "tree.h"

struct Particle* randomsystem(const int n){
    mt_seed32(42424242);
    struct Particle* particles;

    particles = (struct Particle *)malloc(n*sizeof(struct Particle));
    for (int i = 0; i < n; ++i)
    {
        particles[i].position.x = mt_ldrand()-.5;
        particles[i].position.y = mt_ldrand()-.5;
        particles[i].position.z = mt_ldrand()-.5;
        particles[i].velocity.x = mt_ldrand()-.5;
        particles[i].velocity.y = mt_ldrand()-.5;
        particles[i].velocity.z = mt_ldrand()-.5;
        particles[i].acceleration.x = 0.;
        particles[i].acceleration.y = 0.;
        particles[i].acceleration.z = 0.;
        particles[i].mass = mt_ldrand();
        // particles[i].mass = 1.;
    }
    printf("Setup done\n");

    for (int i = 0; i < n; ++i)
    {
        for (int j = 0; j < n; ++j)
        {
            if(i!=j){
                calculateForcePP(&particles[i], &particles[j]);
            }
        }
    }

    struct Force acc = {0.,0.,0.};
    for (int i = 0; i < n; ++i)
    {
        acc.x += particles[i].acceleration.x;
        acc.y += particles[i].acceleration.y;
        acc.z += particles[i].acceleration.z;
    }

    printf("%1.16e %1.16e %1.16e\n", acc.x, acc.y, acc.z);

    return particles;
}

struct Particle* randomsystemtree(const int n){
    mt_seed32(42424242);
    struct Particle* particles;

    particles = (struct Particle *)malloc(n*sizeof(struct Particle));
    for (int i = 0; i < n; ++i)
    {
        particles[i].position.x = mt_ldrand()-.5;
        particles[i].position.y = mt_ldrand()-.5;
        particles[i].position.z = mt_ldrand()-.5;
        particles[i].velocity.x = mt_ldrand()-.5;
        particles[i].velocity.y = mt_ldrand()-.5;
        particles[i].velocity.z = mt_ldrand()-.5;
        particles[i].acceleration.x = 0.;
        particles[i].acceleration.y = 0.;
        particles[i].acceleration.z = 0.;
        particles[i].mass = mt_ldrand();
        // particles[i].mass = 1.;
    }

    struct Tree* tree = maketree(particles, n, .3);
    generateMultipole(tree->root);

    int interactions = 0;
    for (int i = 0; i < n; ++i)
    {
        interactions += calculateForcePN(&particles[i], tree->root);
    }
    printf("%d / %d\n", interactions, n*n);

    struct Force acc = {0.,0.,0.};
    for (int i = 0; i < n; ++i)
    {
        acc.x += particles[i].acceleration.x;
        acc.y += particles[i].acceleration.y;
        acc.z += particles[i].acceleration.z;
    }

    printf("%1.16e %1.16e %1.16e\n", acc.x, acc.y, acc.z);
    return particles;
}

int main(){
    //srand(42424242);
    struct Particle* s1;
    struct Particle* s2;
    int n = 1000;
    s1 = randomsystem(n);
    s2 = randomsystemtree(n);

    struct Force dacc;
    double da = 0.;
    for (int i = 0; i < n; ++i)
    {
        // printf("%1.16e %1.16e\n", s1[i].acceleration.x, s2[i].acceleration.x);
        da += sqrt(dist2(s1[i].acceleration, s2[i].acceleration)/abs2(s1[i].acceleration));
        // da += sqrt(abs2(s2[i].acceleration)/abs2(s1[i].acceleration));
    }
    printf("%1.16e\n", da/n);

}




