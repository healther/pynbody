
#include <iostream>
#include <ctime>

#include "system.h"

int main(int argc, char const *argv[])
{
    std::cout.precision(17);

    int n = 10000;
    // System s1("../test.data");
    std::clock_t begin = std::clock();
    System s1(n);
    int interactions_brute = s1.run();
    std::clock_t end = std::clock();
    double elapsed_secs = double(end - begin) / CLOCKS_PER_SEC;
    std::cout << elapsed_secs << std::endl;


    // System s2("../test.data");
    std::clock_t begin2 = std::clock();
    System s2(n);
    int interactions_tree = s2.run_tree(.7);
    std::clock_t end2 = std::clock();
    double elapsed_secs2 = double(end2 - begin2) / CLOCKS_PER_SEC;
    std::cout << elapsed_secs2 << std::endl;

    std::cout << interactions_brute << " " << interactions_tree << std::endl;
    for (int i = 0; i < n; ++i)
    {
    //    std::cout << s1.particles[i].a[0]-s2.particles[i].a[0] << "\t" << s1.particles[i].a[1]-s2.particles[i].a[1] << "\t" << s1.particles[i].a[2]-s2.particles[i].a[2] << std::endl;
    }
    Vector3D da = Vector3D(0.,0.,0.);
    double daaver = 0.;
    for (int i = 0; i < n; ++i)
    {
        da = s1.particles[i].a - s2.particles[i].a;
        daaver += (da*da) / (s1.particles[i].a*s1.particles[i].a) / (double)n;
    }

    std::cout << daaver << std::endl;
    return 0;
}
