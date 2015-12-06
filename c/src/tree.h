#ifndef TREE_H
#define TREE_H

#include "particle.h"
#include "force.h"

struct Node{
    int nparticles;
    double size;
    double theta;
    struct Force center;

    struct Tree* parenttree;
    struct Particle pseudoparticle;
    struct Node* subnodes[8];
    struct Particle* particle;
};

struct Tree
{
    int nparticles;
    int nnodes, nnodes_used;
    double theta;

    struct Node* root;
    struct Particle* particles;
    struct Node* nodes;
};



void config_subnode(struct Node* subnode, 
        const struct Node* node, const int i)
{
    subnode->nparticles = 0;
    subnode->size = node->size/2.;
    subnode->theta = node->theta;
    subnode->center.x = node->center.x - subnode->size/2. + (i&1)*subnode->size,
    subnode->center.y = node->center.y - subnode->size/2. + (i&2)*subnode->size,
    subnode->center.z = node->center.z - subnode->size/2. + (i&4)*subnode->size,

    subnode->parenttree = node->parenttree;
    subnode->pseudoparticle.position.x = 0.;
    subnode->pseudoparticle.position.y = 0.;
    subnode->pseudoparticle.position.z = 0.;
    subnode->pseudoparticle.velocity.x = 0.;
    subnode->pseudoparticle.velocity.y = 0.;
    subnode->pseudoparticle.velocity.z = 0.;
    subnode->pseudoparticle.acceleration.x = 0.;
    subnode->pseudoparticle.acceleration.y = 0.;
    subnode->pseudoparticle.acceleration.z = 0.;
    subnode->pseudoparticle.mass = 0.;
    for (int i = 0; i < 8; ++i)
    {
        subnode->subnodes[i] = NULL;
    }
    subnode->particle = NULL;
}

int findsubnode(const struct Node* node, 
        const struct Particle* part)
{
    int idx = 0;
    idx += 1 * (node->center.x < part->position.x);
    idx += 2 * (node->center.y < part->position.y);
    idx += 4 * (node->center.z < part->position.z);
    
    return idx;
}

struct Node* nextnode(struct Tree* tree)
{
    if (tree->nnodes_used < tree->nnodes-1){
        tree->nnodes_used += 1;     
        return &(tree->nodes[tree->nnodes_used]);
    }
    return NULL;
}

void addparticle(struct Node* node, 
        struct Particle* newpart)
{
    node->nparticles++;
    if (1==node->nparticles)
    {
        node->particle = newpart;
        return;
    } else if (2==node->nparticles)
    {
        int i = findsubnode(node, node->particle);
        node->subnodes[i] = nextnode(node->parenttree);
        config_subnode(node->subnodes[i], node, i);
        addparticle(node->subnodes[i], node->particle);
        node->particle = NULL;
    } 
    int i = findsubnode(node, newpart);
    if (node->subnodes[i]==NULL) {
        node->subnodes[i] = nextnode(node->parenttree);
        config_subnode(node->subnodes[i], node, i);
    }
    addparticle(node->subnodes[i], newpart);
}

struct Tree* maketree(struct Particle* particles, 
    int nparticles, const double theta){
    struct Tree* tree = malloc(sizeof(struct Tree));
    tree->nparticles = nparticles;
    tree->particles = particles;
    tree->theta = theta;
    
    // prepare 8*log2(nparticles) nodes
    int nexpected_nodes = 0;
    while (nparticles >>= 1) ++nexpected_nodes;
    nexpected_nodes += 10;
    tree->nnodes = tree->nparticles*nexpected_nodes;
    tree->nodes = malloc(tree->nnodes*sizeof(struct Node));
    
    tree->nnodes_used = 0;
    // config root node
    tree->nodes[0].nparticles = 0;
    tree->nodes[0].size = 1.;
    tree->nodes[0].theta = theta;
    tree->nodes[0].center.x = 0.;
    tree->nodes[0].center.y = 0.;
    tree->nodes[0].center.z = 0.;
    tree->nodes[0].parenttree = tree;
    tree->nodes[0].pseudoparticle.position.x = 0.;
    tree->nodes[0].pseudoparticle.position.y = 0.;
    tree->nodes[0].pseudoparticle.position.z = 0.;
    tree->nodes[0].pseudoparticle.velocity.x = 0.;
    tree->nodes[0].pseudoparticle.velocity.y = 0.;
    tree->nodes[0].pseudoparticle.velocity.z = 0.;
    tree->nodes[0].pseudoparticle.acceleration.x = 0.;
    tree->nodes[0].pseudoparticle.acceleration.y = 0.;
    tree->nodes[0].pseudoparticle.acceleration.z = 0.;
    tree->nodes[0].pseudoparticle.mass = 0.;;
    for (int i = 0; i < 8; ++i)
    {
        tree->nodes[0].subnodes[i] = NULL;
    }
    tree->nodes[0].particle = NULL;

    tree->root = &(tree->nodes[0]);

    for (int i = 0; i < tree->nparticles; ++i)
    {
        addparticle(tree->root, &(tree->particles[i]));
    }
    printf("%d / %d\n", tree->nnodes, tree->nnodes_used);

    return tree;
}

void generateMultipole(struct Node* node)
{
    if (0==node->nparticles){
        printf("This should not have happened\n");
        exit(1);
        setzero(&node->pseudoparticle);
    } else if (1==node->nparticles){
        setpart(&node->pseudoparticle, node->particle);
    } else {
        setzero(&node->pseudoparticle);
        for (int i = 0; i < 8; ++i)
        {
            if (node->subnodes[i]!=NULL) {
                generateMultipole(node->subnodes[i]);
                absorbpart(&node->pseudoparticle, &node->subnodes[i]->pseudoparticle);
            }
        }
        // reducepart(&node->pseudoparticle);
    }
}

int calculateForcePN(struct Particle* part, struct Node* node)
{
    double d2 = dist2(part->position, node->pseudoparticle.position);
    // double d2 = dist2(part->position, node->center);

    if (0 == node->nparticles || (d2<1E-14))
    {   // empty or self interaction will be ignored
        return 0;
    } else if (1 == node->nparticles)
    {   // single particle needs to be evaluated
        calculateForcePP(part, &node->pseudoparticle);
        return 1;
    } else if ( (node->size*node->size) < ((node->theta*node->theta) * d2))
    {   // node small enough, yiippii
        calculateForcePP(part, &node->pseudoparticle);
        return 1;
    } else 
    {   // walking down the tree
        int interactions = 0;
        for (int i = 0; i < 8; i++)
        {
            if (node->subnodes[i]!=NULL)
                interactions += calculateForcePN(part, node->subnodes[i]);
        }
        return interactions;
    }
}


#endif /* TREE_H */
