module Integrator

using MyParticle
using MyForce
using MyKutta

export test

#const G = 6.67398e-11      # SI
#const G = 1.48811382e-34   # Au/day
const G = 1.                # NBU

function forces{T<:Real}(particles::Vector{Particle{T}})
    N = size(particles, 1)
    out = Array(Particle{T}, N)
    for i = 1:N
        out[i] = Particle(zero(T))
        out[i].position = particles[i].velocity
        out[i].velocity = Force(zero(T))
    end
    for i = 1:N
        pi = particles[i]
        outi = out[i].velocity
        for j = i+1:N
            pj = particles[j]
            outj = out[j].velocity
            d = pj.position - pi.position
            d3 = fnorm2(d)
            d3 = d3*sqrt(d3)
            F = (G / d3) * d
            #pi.acceleration += pj.mass * F
            #pj.acceleration += pi.mass * F
            outi += pj.mass * F
            outj += pi.mass * F
        end
    end
    out
end


function euler{T<:Real}(particles::Vector{Particle{T}}, acc::Vector{Force{T}}, dt::T)
    N = size(particles, 1)
    out = deepcopy(particles)
    for i = 1:N
        pi = particles[i]
        oi = out[i]
        oi.position += dt*pi.velocity
        oi.velocity += dt*acc[i]
        # pi.acceleration = Force(zero(T))
        # oi.acceleration.x = zero(T)
        # oi.acceleration.y = zero(T)
        # oi.acceleration.z = zero(T)
        oi.time += dt
    end
    out
end

function test(N::Integer, tend::Real, dt::Real, tol::Real)
    println("Testrun with $N particles")
    t0 = time()
    T = typeof(tend)
    println("Type of simulation $T")
    particles = Array(Particle{T},N)
    for i = 1:N
        particles[i] = Particle(zero(T))
        pi = particles[i]
        pi.position.x = rand()
        pi.position.y = rand()
        pi.position.z = rand()
        pi.velocity.x = rand()
        pi.velocity.y = rand()
        pi.velocity.z = rand()
        #pi.acceleration = zero(T)
        # pi.acceleration.x = zero(T)
        # pi.acceleration.y = zero(T)
        # pi.acceleration.z = zero(T)
        pi.mass = one(T)
        pi.time = zero(T)
    end
    t1 = time()
    println("Initialisation: $(t1-t0)")

    const nint = iceil(tend/dt)
    ftm = "%08d %1.16e %1.16e %1.16e %1.16e %1.16e %1.16e %1.16e"
    for l = 1:nint
        t2 = time()
        f = open(@sprintf("data/%08d", l-1) * ".dat", "w")
        write(f,"Snapshotnumber" * @sprintf("%08d", l-1) * "\n")
        write(f,"Time: " * @sprintf("%1.16e", (l-1)*dt) * "\n")
        write(f,"Particlenumber: " * @sprintf("%08d", N) * "\n")
        for i = 1:N
            pi = particles[i]
            str = @sprintf("%08d %1.16e %1.16e %1.16e %1.16e %1.16e %1.16e %1.16e", i, pi.mass, pi.position.x, pi.position.y, pi.position.z, pi.velocity.x, pi.velocity.y, pi.velocity.z)
            write(f,str * "\n")
        end
        close(f)
        t3 = time()
        # acc = forces(particles)
        # t3a = time()
        # particles = euler(particles, acc, dt)
        particles = dopri(forces, particles, dt, tol)
        t4 = time()
        @printf("%6d / %6d: last: %1.7e, remaining: %1.7e, writing: %1.7e, calculating: %1.7e \n",
            l, nint, t4-t2, (t4-t2)*(nint-l), t3-t2, t4-t3)
    end
    f = open(@sprintf("data/%08d", nint) * ".dat", "w")
    write(f,"Snapshotnumber" * @sprintf("%08d", nint) * "\n")
    write(f,"Time: " * @sprintf("%1.16e", nint*dt) * "\n")
    write(f,"Particlenumber: " * @sprintf("%08d", N) * "\n")
    for i = 1:N
        pi = particles[i]
        str = @sprintf("%08d %1.16e %1.16e %1.16e %1.16e %1.16e %1.16e %1.16e", i, pi.mass, pi.position.x, pi.position.y, pi.position.z, pi.velocity.x, pi.velocity.y, pi.velocity.z)
        write(f,str * "\n")
    end
    close(f)
    t5 = time()
    println("Total time: $(t5-t0)")
end
end # module