
#include <iostream>
#include <ctime>

#include "system.h"

int main(int argc, char const *argv[])
{
    std::cout.precision(17);

    int n = 5;
    System s1("../test.data");
    std::clock_t begin = std::clock();
    // System s1(n);
    int interactions_brute = s1.run();
    std::clock_t end = std::clock();
    double elapsed_secs = double(end - begin) / CLOCKS_PER_SEC;
    std::cout << elapsed_secs << std::endl;


    System s2("../test.data");
    std::clock_t begin2 = std::clock();
    // System s2(n);
    int interactions_tree = s2.run_tree(.7);
    std::clock_t end2 = std::clock();
    double elapsed_secs2 = double(end2 - begin2) / CLOCKS_PER_SEC;
    std::cout << elapsed_secs2 << std::endl;

    System s3("../test.data");
    std::clock_t begin3 = std::clock();
    // System s3(n);
    int interactions_fmm = s3.run_fmm(.7);
    std::clock_t end3 = std::clock();
    double elapsed_secs3 = double(end3 - begin3) / CLOCKS_PER_SEC;
    std::cout << elapsed_secs3 << std::endl;

    std::cout << interactions_brute << " " << interactions_tree << " " << interactions_fmm << std::endl;
    for (int i = 0; i < n; ++i)
    {
       // std::cout << s1.particles[i].a[0]-s3.particles[i].a[0] << "\t" << s1.particles[i].a[1]-s3.particles[i].a[1] << "\t" << s1.particles[i].a[2]-s3.particles[i].a[2] << std::endl;
       std::cout <<  s3.particles[i].a[0] << "\t" <<  s3.particles[i].a[1] << "\t" <<  s3.particles[i].a[2] << std::endl;
    }
    Vector3D da = Vector3D(0.,0.,0.);
    double daaver = 0.;
    double daaver2 = 0.;
    for (int i = 0; i < n; ++i)
    {
        da = s1.particles[i].a - s2.particles[i].a;
        daaver += (da*da) / (s1.particles[i].a*s1.particles[i].a) / (double)n;
        da = s1.particles[i].a - s3.particles[i].a;
        daaver2 += (da*da) / (s1.particles[i].a*s1.particles[i].a) / (double)n;
    }

    std::cout << daaver << std::endl;
    std::cout << daaver2 << std::endl;
    return 0;
}
