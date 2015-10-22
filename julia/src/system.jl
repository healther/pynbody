include("force.jl")
include("particle.jl")

module MySystem

using MyParticle
using MyForce

srand(42424242)

type System
    n::Int64
    particles::Array{MyParticle.Particle, 1}

    function System(n::Int64)
        particles = MyParticle.Particle[]
        for i in [1:n]
            r = MyForce.Force(rand()-.5, rand()-.5, rand()-.5)
            v = MyForce.Force(rand()-.5, rand()-.5, rand()-.5)
            a = MyForce.Force(0.,0.,0.)
            m = rand()
            p = MyParticle.Particle(0.)
            p.position = r
            p.velocity = v
            p.acceleration = a
            p.mass = m
            push!(particles, p)
        end
    end
end

end # module


function run!(particles)
    for px in particles
        for py in particles
            if px!=py
                MyParticle.calcacceleration!(px,py)
            end
        end
    end
end


#s = MySystem.System(1000)
n = 10000
particles = MyParticle.Particle[]
for i in 1:n
    r = MyForce.Force(rand()-.5, rand()-.5, rand()-.5)
    v = MyForce.Force(rand()-.5, rand()-.5, rand()-.5)
    a = MyForce.Force(0.,0.,0.)
    m = rand()
    p = MyParticle.Particle(0.)
    p.position = r
    p.velocity = v
    p.acceleration = a
    p.mass = m
    push!(particles, p)
end

run!(particles)

f = MyForce.Force(0.)
for p in particles
    f+=p.acceleration
end
println(f)

