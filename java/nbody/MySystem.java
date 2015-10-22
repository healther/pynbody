
package nbody;

public class MySystem 
{
    public static void main (String[] args)
    {
        int n = 10000;
        Particle particles [] = new Particle[n];

        

        for (int i = 0; i<n; ++i) {
            Force position = new Force(Math.random(), Math.random(), Math.random());
            Force velocity = new Force(Math.random(), Math.random(), Math.random());
            double mass = Math.random();
            particles[i] = new Particle(position, velocity, mass);
        }

        for (int i=0; i<n; ++i) {
            for (int j=0; j<n; ++j) {
                if (i!=j) {
                    particles[i].calcforce(particles[j]);
                }
            }
        }

        Force f = new Force(0.,0.,0.);
        for (int i=0; i<n; ++i) {
            f.x += particles[i].acceleration.x;
            f.y += particles[i].acceleration.y;
            f.z += particles[i].acceleration.z;
        }

        System.out.format("%1.17e %1.17e %1.17e\n", f.x, f.y, f.z);
    }
}


