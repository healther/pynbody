
#include <iostream>

#include "system.h"

int main(int argc, char const *argv[])
{
    std::cout.precision(17);

    int n = 10000;
    System s(n);
    
    // int interactions = s.run_tree(.8);
    // std::cout << interactions << std::endl;
    s.run();
    for (int i = 0; i < n; ++i)
    {
        //std::cout << s.particles[i].a[0] << "\t" << s.particles[i].a[1] << "\t" << s.particles[i].a[2] << std::endl;
    }
    Vector3D a = Vector3D(0.,0.,0.);
    for (int i = 0; i < n; ++i)
    {
        a += s.particles[i].a;
    }

    std::cout << a[0] << "\t" << a[1] << "\t" << a[2] << std::endl;
    return 0;
}
