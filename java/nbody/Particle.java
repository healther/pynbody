package nbody;

public class Particle 
{
    Force position;
    Force velocity;
    Force acceleration;
    double mass;

    Particle(){
        position = new Force(0., 0., 0.);
        velocity = new Force(0., 0., 0.);
        acceleration = new Force(0., 0., 0.);
        mass = 0.;
    }

    Particle(Force r, Force v, double m) {
        position = r;
        velocity = v;
        acceleration = new Force(0., 0., 0.);
        mass = m;
    }

    public void calcforce(Particle py) {
        Force sep = position.dist(py.position);

        double d2 = sep.norm2();
        d2 = -mass*py.mass/d2/Math.sqrt(d2);
        acceleration.x += d2 * sep.x;
        acceleration.y += d2 * sep.y;
        acceleration.z += d2 * sep.z;        
    }
}




