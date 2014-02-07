from __future__ import print_function, division

import numpy as np
import pycuda.autoinit
import pycuda.driver as drv
from pycuda import gpuarray

from pycuda.compiler import SourceModule


advance_kernel = """
__global__ advance(const __restrict__ double * r_old, const __restrict__ double * v_old, const __restrict__ double * mass, double * r_new, double * v_new, int number_of_particles){
    int tx = threadIdx.x + blockDim.x * blockIdx.x;
    
    if(tx>=n) return;
    
    int particle_id = tx;
    double particle_x = r_old[particle_id];
    double particle_y = r_old[particle_id + number_of_particles];
    double particle_z = r_old[particle_id + 2*number_of_particles];
    double particle_vx = r_old[particle_id];
    double particle_vy = r_old[particle_id + number_of_particles];
    double particle_vz = r_old[particle_id + 2*number_of_particles];
    double particle_mass = mass[particle_id];
    
    double distance = 0.;
    double acceleration_vx = 0.;
    double acceleration_vy = 0.;
    double acceleration_vz = 0.;
    
    for(int i=0; i<number_of_particles; ++i){
        if(i!=particle_id){
            distance = sprt( 
                (particle_x-r_old[i])*(particle_x-r_old[i]) 
                    +
                (particle_y-r_old[i + number_of_particles])*(particle_x-r_old[i  + number_of_particles]) 
                    +
                (particle_z-r_old[i + 2*number_of_particles])*(particle_x-r_old[i + 2*number_of_particles]) 
                    );

            acceleration_x += mass[i] * (r_old[i] - particle_x) / distance**3;
            acceleration_y += mass[i] * (r_old[i + number_of_particles] - particle_x) / distance**3;
            acceleration_z += mass[i] * (r_old[i + 2*number_of_particles] - particle_x) / distance**3;
        
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
    number_of_particles = np.int32(number_of_particles)
    gpu_rs, gpu_vs = [gpu_r], [gpu_v]
    
    for i in xrange(stores-1):
        gpu_rs.append(gpuarray.empty_like(gpu_r))
        gpu_vs.append(gpuarray.empty_like(gpu_v))
        
    advance = SourceModule(advance_kernel).get_function("advance")
    advance.prepare([np.intp, np.intp, np.intp, np.intp, np.intp, np.int32])
    
    block_size = (32,0,0)
    grid_size = (int(number_of_particles/32), 0, 0)
    
    advance.prepared_call(block_size, grid_size ,gpu_r[0], gpu_v[0], gpu_mass, gpu_r[1], gpu_v[1], number_of_particles)

    old, new = 1, 2
    for i in xrange(steps):
        r = rs_gpu[old].get_async()
        v = vs_gpu[old].get_async()
        advance.prepared_call_async(block_size, grid_size ,gpu_rs[old], gpu_vs[old], gpu_mass, gpu_rs[new], gpu_vs[new], number_of_particles)
        
        np.write("step{i:4}_r".format(i*stepsize)+".dat", r)
        np.write("step{i:4}_v".format(i*stepsize)+".dat", r)
        
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


    