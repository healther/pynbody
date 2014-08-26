module MyParticle

using MyForce

export Particle, pnorm2, pnorm

type Particle{T<:Real}
    position::Force{T}
    velocity::Force{T}
    #acceleration::Force{T}
    #jerk::Force{T}
    #energy::T
    mass::T
    time::T
end

Particle{T<:Real}(x::T) = Particle(Force(x), Force(x), x, x)

pnorm{T<:Real}(a::Particle{T}) = fnorm(a.position) + fnorm(a.velocity)
pnorm2{T<:Real}(a::Particle{T}) = fnorm2(a.position) + fnorm2(a.velocity)


+{T<:Real}(a::Particle{T}, b::Particle{T}) = Particle{T}(a.position+b.position, 
        a.velocity+b.velocity, 
        a.mass,
        a.time)
-{T<:Real}(a::Particle{T}, b::Particle{T}) = Particle{T}(a.position-b.position, 
        a.velocity-b.velocity, 
        a.mass,
        a.time)

*{T<:Real}(a::Particle{T}, b::Particle{T}) = a.position*b.position + a.velocity*b.velocity
.*{T<:Real}(a::Particle{T}, b::Particle{T}) = a.position.*b.position + a.velocity.*b.velocity
*{T<:Real}(a::Particle{T}, b::T) = Particle{T}(a.position*b, 
        a.velocity*b, 
        a.mass,
        a.time)
*{T<:Real}(a::T, b::Particle{T}) = b*a
.*{T<:Real}(a::Particle{T}, b::T) = Particle{T}(a.position*b, 
        a.velocity*b, 
        a.mass,
        a.time)
.*{T<:Real}(a::T, b::Particle{T}) = b.*a
/{T<:Real}(a::Particle{T}, b::T) = Particle{T}(a.position/b, 
        a.velocity/b, 
        a.mass,
        a.time)

end # module