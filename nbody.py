from __future__ import print_function, division

import numpy as np
import pycuda.autoinit
import pycuda.driver as drv
from pycuda import gpuarray

from pycuda.compiler import SourceModule


advance_kernel = """
#include <math.h>

#define timestep .01

__global__ void advance(const double * __restrict__ r_old, const double * __restrict__ v_old, const double * __restrict__ mass, double * __restrict__ r_new, double * __restrict__ v_new, const int number_of_particles){
    const int tx = threadIdx.x + blockDim.x * blockIdx.x;
    
    if(tx>=number_of_particles) return;
    
    const int particle_id = tx;
    const double particle_x = r_old[particle_id];
    const double particle_y = r_old[particle_id + number_of_particles];
    const double particle_z = r_old[particle_id + 2*number_of_particles];
    const double particle_vx = r_old[particle_id];
    const double particle_vy = r_old[particle_id + number_of_particles];
    const double particle_vz = r_old[particle_id + 2*number_of_particles];
    const double particle_mass = mass[particle_id];
    
    double distance = 0.;
    double acceleration_x = 0.;
    double acceleration_y = 0.;
    double acceleration_z = 0.;
    
    for(int i=0; i<number_of_particles; ++i){
        if(i!=particle_id){
            distance = (particle_x-r_old[i]) * (particle_x-r_old[i]);
            distance += (particle_y-r_old[i+number_of_particles]) * (particle_x-r_old[i+number_of_particles]) ;
            distance += (particle_z-r_old[i+2*number_of_particles]) * (particle_x-r_old[i+2*number_of_particles]) ;
            distance = sqrt(distance);
            acceleration_x += mass[i] * (r_old[i] - particle_x) / pow(distance,3);
            acceleration_y += mass[i] * (r_old[i + number_of_particles] - particle_x) / pow(distance,3);
            acceleration_z += mass[i] * (r_old[i + 2*number_of_particles] - particle_x) / pow(distance,3);
        
        }
        
        r_new[particle_id] = particle_vx * timestep;
        r_new[particle_id + number_of_particles] = particle_vy * timestep;
        r_new[particle_id + 2 * number_of_particles] = particle_vz * timestep;
        
        v_new[particle_id] = acceleration_x * timestep;
        v_new[particle_id + number_of_particles] = acceleration_y * timestep;
        v_new[particle_id + 2 * number_of_particles] = acceleration_z * timestep;
    }
}
"""

def integrate(stepsize = .01, stores = 5, steps=10000, number_of_particles=2**10):
    gpu_r, gpu_v, gpu_mass = create_particles(number_of_particles)
    number_of_particles = np.int64(number_of_particles)
    gpu_rs, gpu_vs = [gpu_r], [gpu_v]
    
    for i in xrange(stores-1):
        gpu_rs.append(gpuarray.empty_like(gpu_r))
        gpu_vs.append(gpuarray.empty_like(gpu_v))
        
    advance = SourceModule(advance_kernel).get_function("advance")
    advance.prepare([np.intp, np.intp, np.intp, np.intp, np.intp, np.int32])
    stream = drv.Stream()
    block_size = (32,1,1)
    grid_size = (int(number_of_particles/32), 1)
    
    advance.prepared_call(grid_size, block_size ,gpu_rs[0].gpudata, gpu_vs[0].gpudata, gpu_mass.gpudata, gpu_rs[1].gpudata, gpu_vs[1].gpudata, number_of_particles)

    old, new = 1, 2
    for i in xrange(steps):
        r = gpu_rs[old].get_async()
        v = gpu_vs[old].get_async()
        advance.prepared_async_call(grid_size, block_size, stream, gpu_rs[old].gpudata, gpu_vs[old].gpudata, gpu_mass.gpudata, gpu_rs[new].gpudata, gpu_vs[new].gpudata, number_of_particles)
        
        np.save("step{:3.5}_r".format(i*stepsize)+".dat", r)
        np.save("step{:3.5}_v".format(i*stepsize)+".dat", r)
        
        old, new = new, (new+1)%stores

def create_particles(n):
    numberofparticles = n
    
    r = np.random.rand(3*n)
    v = np.random.rand(3*n)
    mass = np.random.rand(n)
    
    gpu_r = gpuarray.to_gpu(r)
    gpu_v = gpuarray.to_gpu(v)
    gpu_mass = gpuarray.to_gpu(mass)
    
    return gpu_r, gpu_v, gpu_mass


    
