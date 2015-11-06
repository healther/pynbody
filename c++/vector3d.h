#ifndef H_VECTOR3D
#define H_VECTOR3D

class Vector3D
{
    public:
    
        double   x;
        double   y;
        double   z;
        
        Vector3D() {}
        
        Vector3D(double r, double s, double t)
        {
            x = r;
            y = s;
            z = t;
        }
        
        Vector3D& Set(double r, double s, double t)
        {
            x = r;
            y = s;
            z = t;
            return (*this);
        }
        
        double& operator [](long k)
        {
            return ((&x)[k]);
        }
        
        const double& operator [](long k) const
        {
            return ((&x)[k]);
        }
        
        Vector3D& operator +=(const Vector3D& v)
        {
            x += v.x;
            y += v.y;
            z += v.z;
            return (*this);
        }
        
        Vector3D& operator -=(const Vector3D& v)
        {
            x -= v.x;
            y -= v.y;
            z -= v.z;
            return (*this);
        }
        
        Vector3D& operator *=(double t)
        {
            x *= t;
            y *= t;
            z *= t;
            return (*this);
        }
        
        Vector3D& operator /=(double t)
        {
            double f = 1.0F / t;
            x *= f;
            y *= f;
            z *= f;
            return (*this);
        }
        
        Vector3D& operator %=(const Vector3D& v)
        {
            // cross product
            double       r, s;
            
            r = y * v.z - z * v.y;
            s = z * v.x - x * v.z;
            z = x * v.y - y * v.x;
            x = r;
            y = s;
            
            return (*this);
        }
        
        Vector3D& operator &=(const Vector3D& v)
        {
            x *= v.x;
            y *= v.y;
            z *= v.z;
            return (*this);
        }
        
        Vector3D operator -(void) const
        {
            return (Vector3D(-x, -y, -z));
        }
        
        Vector3D operator +(const Vector3D& v) const
        {
            return (Vector3D(x + v.x, y + v.y, z + v.z));
        }
        
        Vector3D operator -(const Vector3D& v) const
        {
            return (Vector3D(x - v.x, y - v.y, z - v.z));
        }
        
        Vector3D operator *(double t) const
        {
            return (Vector3D(x * t, y * t, z * t));
        }
        
        Vector3D operator /(double t) const
        {
            double f = 1.0F / t;
            return (Vector3D(x * f, y * f, z * f));
        }
        
        double operator *(const Vector3D& v) const
        {
            return (x * v.x + y * v.y + z * v.z);
        }
        
        Vector3D operator %(const Vector3D& v) const
        {
            return (Vector3D(y * v.z - z * v.y, z * v.x - x * v.z,
                    x * v.y - y * v.x));
        }
        
        Vector3D operator &(const Vector3D& v) const
        {
            return (Vector3D(x * v.x, y * v.y, z * v.z));
        }
        
        bool operator ==(const Vector3D& v) const
        {
            return ((x == v.x) && (y == v.y) && (z == v.z));
        }
        
        bool operator !=(const Vector3D& v) const
        {
            return ((x != v.x) || (y != v.y) || (z != v.z));
        }
        
        Vector3D& Normalize(void)
        {
            return (*this /= sqrtf(x * x + y * y + z * z));
        }
        
};


#endif


