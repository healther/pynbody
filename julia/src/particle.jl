module MyParticle

include("force.jl")
using MyForce
export Particle, calcacceleration!

type Particle{T<:Real}
    position::Force{T}
    velocity::Force{T}
    acceleration::Force{T}
    #jerk::Force{T}
    #energy::T
    mass::T
    #time::T
end

Particle{T<:Real}(x::T) = Particle{T}(Force(x), Force(x), Force(x), x)

convert{T<:Real}(::Type{Particle{T}}, f::Particle) = Particle{T}(convert(T, f.position), convert(T, f.velocity), convert(T, f.acceleration), convert(T, f.mass))


function calcacceleration!{T<:Real}(px::Particle{T}, py::Particle{T})
    sep::Force{T} = px.position::Force{T}-py.position::Force{T}
    d2::Float64 = norm2(sep)
    px.acceleration -= px.mass*py.mass/d2/sqrt(d2)*sep
end

end # module

