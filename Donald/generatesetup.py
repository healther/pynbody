
import numpy as np
import yaml
import sys


def generatesetup(enum=0):
    '''Units are kg, km, and km/s if not specified otherwise'''
    data = np.zeros((4,7))
    data[0] = [5.97237E24, 0., 0., 0., 0., 0., 0.]  # earth
    if enum is 0:
        angles = [0., 120., 240.]
    elif enum is 1:
        angles = [0., 60., 120.]
    sep = 384400
    vabs = sep*2*np.pi/27.3217/24./60./60.
    for i,deg in enumerate(angles):
        r = [np.sin(deg*np.pi/180.)*sep, np.cos(deg*np.pi/180.)*sep, 0.]
        v = [np.cos(deg*np.pi/180.)*vabs, -np.sin(deg*np.pi/180.)*vabs, 0.]
        if enum is 3 and i is not 1:
            data[i+1, 0] = 7.35E22 / 30.
        else:
            data[i+1, 0] = 7.35E22
        data[i+1, 1:4] = r
        data[i+1, 4:7] = v


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

def writeinitfile(enum=0):
    data = generatesetup(enum=enum)
    outdata, transl = translatetonbu(data)
    np.savetxt('data.inp', outdata)

    with open('transl.dat', 'w') as f:
        yaml.dump(transl, f)

if __name__ == '__main__':
    if len(sys.argv)==1:
        writeinitfile()
    elif len(sys.argv)==2:
        writeinitfile(enum=int(sys.argv[1]))


