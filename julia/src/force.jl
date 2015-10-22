module MyForce

export Force, norm2

type Force{T<:Real}
    x::T
    y::T
    z::T
end

Force{T<:Real}(x::T) = Force{T}(x, x, x)

convert{T<:Real}(::Type{Force{T}}, f::Force) = Force(convert(T, f.x), convert(T, f.y), convert(T, f.z))


norm2{T<:Real}(f::Force{T}) = f.x*f.x + f.y*f.y + f.z*f.z
norm{T<:Real}(f::Force{T}) = sqrt(f.x*f.x + f.y*f.y + f.z*f.z)

+{T<:Real}(a::Force{T}, b::Force{T}) = Force{T}(a.x+b.x, a.y+b.y, a.z+b.z)
-{T<:Real}(a::Force{T}, b::Force{T}) = Force{T}(a.x-b.x, a.y-b.y, a.z-b.z)
*{T<:Real}(a::Force{T}, b::Force{T}) = a.x*b.x, a.y*b.y, a.z*b.z

*{T<:Real}(a::Force{T}, b::T) = Force{T}(a.x*b, a.y*b, a.z*b)
*{T<:Real}(b::T, a::Force{T}) = a*b
/{T<:Real}(a::Force{T}, b::T) = Force{T}(a.x/b, a.y/b, a.z/b)


end

