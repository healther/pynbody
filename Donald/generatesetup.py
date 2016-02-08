
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

import numpy as np
from scipy.optimize import fsolve
import yaml
import sys
import time
import subprocess
import glob
import os
import shutil
import errno
import datetime


def generatesetup(enum_angles=0, enum_mass = 0, enum_stable = 0, enum_gmoon = 0):
    '''Units are kg, km, and km/s if not specified otherwise

    enum_angles     sets the configuration (0 for 120 deg seperation, 1 for 60 deg seperation
    enum_mass       sets the mass ration of the moons (0 for equal, 1 for 1:30)
    enum_stable     sets the stability (0 for right velocity, 1 for v=1.01*v
    enum_gmoon      sets the goldmoon (0 for not, 1 at 500km distance, 2 at L2-point)
        '''
    if enum_gmoon is 0:
        data = np.zeros((4,10))
    else:
        data = np.zeros((5,10))
        data[-1] = [1.01E18, 0., 0., 0., 0., 0., 0., 0., 0., 0.]  # gold moon
        # note that the inclusion of the goldmoon changes the timescaling slightly
        # change is small since m_gmoon ~ 1E-4 m_moon ~ 1E-2 m_earth but non-zero

    data[0] = [5.97237E24, 0., 0., 0., 0., 0., 0., 0., 0., 0.]  # earth
    if enum_angles is 0:
        angles = [0., 120., 240.]
    elif enum_angles is 1:
        angles = [0., 60., 120.]
    sep = 384400                            # orbital distance of the moons
    vabs = sep*2*np.pi/27.3217/24./60./60.  # orbital speed of the moons
    for i,deg in enumerate(angles):
        r = [np.sin(deg*np.pi/180.)*sep, np.cos(deg*np.pi/180.)*sep, 0.]
        v = [np.cos(deg*np.pi/180.)*vabs, -np.sin(deg*np.pi/180.)*vabs, 0.]
        if enum_mass is 0 and i is not 1:
            data[i+1, 0] = 7.35E22 / 30.    # reduced mass moon
        else:
            data[i+1, 0] = 7.35E22          # moon mass

        data[i+1, 1:4] = r
        data[i+1, 4:7] = v
        if enum_stable is 1 and i is 0:
            data[i+1, 4:7] *= 1.01
        data[i+1, 7:10] = [0., 0., 0.]

        if enum_gmoon is not 0 and i is 1:
            if enum_gmoon is 2:
                def l2(x):
                    return data[0,0]/sep**2+x*(data[0,0]+data[i+1,0])/sep**3 - data[0,0]/(sep+x)**2 - data[i+1,0]/x**2
                gmoon_dist = fsolve(l2, .16*sep)      # gold moon at L2
            elif enum_gmoon is 1:
                gmoon_dist = 500        # distance between mass rich moon and gmoon
            else:
                raise NotImplementedError('only L2 and fixed distance are implemented for the gold moon')
            data[-1, 1:4] = r
            data[-1, 4:7] = v
            data[-1, 1:4] *= (sep+gmoon_dist)/sep
            data[-1, 4:7] *= (sep+gmoon_dist)/sep


    # COM correction
    rmean = (data[:,0:1]*data[:,1:4]).sum(axis=0)/data[:,0].sum()
    vmean = (data[:,0:1]*data[:,4:7]).sum(axis=0)/data[:,0].sum()

    data[:,1:4] -= rmean
    data[:,4:7] -= vmean

    return data

### GRAV = 6.67408E-11  # [m^3 kg^-1 s^-2]
GRAV = 6.67408E-20  # [km^3 kg^-1 s^-2]

def translatetonbu(data):
    '''Assumes (mass, pos, velocity) rows in data'''
    mnbu = data[:,0].sum()
    outdata = np.array(data)
    outdata[:,0] /= mnbu

    rnbu_inv = 0.
    for d1 in data:
        for d2 in data:
            if (d1!=d2).any():
                rnbu_inv += d1[0]*d2[0]/np.linalg.norm(d1[1:4]-d2[1:4])
    rnbu_inv = rnbu_inv / mnbu / mnbu
    rnbu = 1./rnbu_inv
    outdata[:,1:4] *= rnbu_inv

    vnbu = np.sqrt(GRAV*mnbu*rnbu_inv)
    outdata[:,4:7] /= vnbu

    tnbu = rnbu/vnbu

    return outdata, {'mnbu': float(mnbu), 'rnbu': float(rnbu), 'vnbu': float(vnbu), 'tnbu': float(tnbu)}

def translatefromnbu(data, mnbu, rnbu, vnbu):
    outdata = np.array(data)
    outdata[:,0] *= mnbu
    outdata[:,1:4] *= rnbu
    outdata[:,4:7] *= vnbudata.con

    return outdata

def writeinitfile(enum_angles=0, enum_mass = 0, enum_stable = 0, enum_gmoon = 0):
    data = generatesetup(enum_angles=enum_angles, enum_mass = enum_mass, enum_stable = enum_stable, enum_gmoon = enum_gmoon)
    outdata, transl = translatetonbu(data)

    with open('data.inp', 'w') as f:
        f.write('0000\n')
        f.write('{:06d}\n'.format(outdata.shape[0]))
        f.write('{:.16E}\n'.format(0.))
        for i, d in enumerate(outdata):
            f.write('{:06d}\t{:.16E}\t{:.16E}\t{:.16E}\t{:.16E}\t{:.16E}\t{:.16E}\t{:.16E}\n'.format(
                i, d[0], d[1], d[2], d[3], d[4], d[5], d[6]
                ))

    # np.savetxt('data.inp', outdata)

    with open('transl.dat', 'w') as f:
        yaml.dump(transl, f)

def writecfgfile(tend, outputperiod):
    with open('transl.dat', 'r') as f:
        transl = yaml.load(f)
    tphysdisk = transl['tnbu']/24/60/60
    tdisk = 1.
    while (tphysdisk>outputperiod):
        tphysdisk /= 2.
        tdisk /= 2.
    with open('phi-CPU4.cfg', 'w') as f:
        f.write('{}\t{}\t{}\t{}\t{}\tdata.inp'.format(0., tend, tdisk, 0.125, 0.05))

def plot(folder):
    d = np.loadtxt(folder+os.sep+'data.inp', skiprows=3)
    if d.shape[0] is 4:
        rx = [[], [], [], []]
        ry = [[], [], [], []]
    elif d.shape[0] is 5:
        rx = [[], [], [], [], []]
        ry = [[], [], [], [], []]
    else:
        raise NotImplementedError("Unknown number of particles")
    datafiles = glob.iglob(os.path.join(folder, "*.dat"))
    for f in datafiles:
        if f.endswith('transl.dat') or f.endswith('contr.dat'):
            continue
        d = np.loadtxt(f, skiprows=3)
        for j in range(d.shape[0]):
            rx[j].append(d[j,2])
            ry[j].append(d[j,3])
    r = np.array([rx,ry]).T

    with PdfPages(folder+os.sep+'plot.pdf') as pdf:
        fig = plt.figure()
        ax = fig.add_subplot(111)
        for i in range(d.shape[0]):
            ax.plot(r[:,i,0], r[:,i,1], 'x', label=str(i))
        ax.set_xlabel('x [nbu]')
        ax.set_ylabel('y [nbu]')
        ax.set_title('Trajectories')
        plt.savefig(pdf, format='pdf')
        metadata = pdf.infodict()
        metadata['Author'] = 'Andreas Baumbach'
        metadata['Subject'] = 'Trajectories of 3 moon system in Entenhausen'

def main(outputperiod = 1.):
    '''Executes all simulations

    outputperiod  float    maximum number of days between two writeouts
    Requires the phi-simulator executable (cpu-4th) in the same folder and creates subfolders for each simulation run. Recommend turn off of the automatic timestep selection.
    Each folder contains the outputfiles of the phi-simulator, one per writeouttime-step
    '''
    simulations = [ (0, 0, 0, 0),      # 120 deg seperation, equal mass
                    (1, 0, 0, 0),      # 60 deg seperation, equal mass
                    (1, 1, 0, 0),      # 60 deg seperation, 1:30 mass
                    (0, 0, 1, 0),      # 120 deg seperation, equal mass, 1% increased momentum of one moon
                    (1, 1, 1, 0),      # 60 deg seperation, 1:30 mass, 1% increased momentum of one light moon
                    (1, 1, 0, 1),      # 60 deg seperation, 1:30 mass, including gold moon at 500 km
                    (1, 1, 0, 2),      # 60 deg seperation, 1:30 mass, including gold moon at L2
                     ]

    t0 = time.time()
    for i,s in enumerate(simulations):
        i += 1
        t1 = time.time()
        print("{} Generating simulation {} of {}".format(datetime.datetime.now(), i, len(simulations)))
        writeinitfile(enum_angles=s[0], enum_mass=s[1], enum_stable=s[2], enum_gmoon=s[3])
        writecfgfile(tend=3., outputperiod=outputperiod)
        print("{} Starting simulation {} of {}".format(datetime.datetime.now(), i, len(simulations)))
        stdout = subprocess.check_output(['./cpu-4th'], stderr=subprocess.STDOUT)
        print("{} Simulation done, cleaning up".format(datetime.datetime.now()))
        with open('output', 'wb') as f:
            f.write(stdout)
        folder = 'sim{:04d}'.format(i)
        try:
            shutil.rmtree(folder)
        except FileNotFoundError as e:
            pass
        try:
            os.makedirs(folder)
        except OSError as e:
            if e.errno != errno.EEXIST:
                raise
        datafiles = glob.iglob(os.path.join('.', "*.dat"))
        for dfile in datafiles:
            if os.path.isfile(dfile):
                shutil.move(dfile, folder)
        shutil.move('data.inp', folder)
        shutil.move('phi-CPU4.cfg', folder)
        shutil.copy('cpu-4th', folder)
        plot(folder)
        t2 = time.time()
        print("{} Completed simulation {} of {} in {} seconds\n".format(datetime.datetime.now(), i, len(simulations), t2-t1))
    print("____________________________")
    print("{} Finished {} simulations in {} seconds".format(datetime.datetime.now(), len(simulations), t2-t0))

if __name__ == '__main__':
    if len(sys.argv)==1:
        writeinitfile()
    elif len(sys.argv)==2:
        main(outputperiod = float(sys.argv[1]))
    elif len(sys.argv)==4:
        writeinitfile(enum_angles=int(sys.argv[1]), enum_mass=int(sys.argv[2]), enum_stable=int(sys.argv[3]))
    elif len(sys.argv)==5:
        writeinitfile(enum_angles=int(sys.argv[1]), enum_mass=int(sys.argv[2]), enum_stable=int(sys.argv[3]), enum_gmoon=int(sys.argv[4]))


