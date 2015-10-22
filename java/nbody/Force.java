
package nbody;


public class Force {
    double x;
    double y;
    double z;

    Force(double _x) {
        x = _x;
        y = _x;
        z = _x;
    }

    Force(double _x, double _y, double _z) {
        x = _x;
        y = _y;
        z = _z;
    }

    public double norm2() {
        return x*x + y*y + z*z;
    }

    public Force dist(Force f2) {
        Force d = new Force(0.);
        d.x = x - f2.x;
        d.y = y - f2.y;
        d.z = z - f2.z;
        return d;
    }
}

