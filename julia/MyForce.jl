module MyForce

export Force, fnorm2, fnorm

type Force{T<:Real}
    x::T
    y::T
    z::T
end

Force{T<:Real}(x::T) = Force(x, x, x)

fnorm2{T<:Real}(f::Force{T}) = f.x*f.x + f.y*f.y + f.z*f.z
fnorm{T<:Real}(f::Force{T}) = sqrt(f.x*f.x + f.y*f.y + f.z*f.z)

convert{T<:Real}(::Type{Force{T}}, f::Force) = Force(convert(T, f.x), convert(T, f.y), convert(T, f.z))
convert{T<:Real}(::Type{Force{T}}, x::Real) = Force(convert(T, x))

+{T<:Real}(a::Force{T}, b::Force{T}) = Force{T}(a.x+b.x, a.y+b.y, a.z+b.z)
-{T<:Real}(a::Force{T}, b::Force{T}) = Force{T}(a.x-b.x, a.y-b.y, a.z-b.z)
*{T<:Real}(a::Force{T}, b::Force{T}) = a.x*b.x + a.y*b.y + a.z*b.z
.*{T<:Real}(a::Force{T}, b::Force{T}) = a.x*b.x + a.y*b.y + a.z*b.z

*{T<:Real}(a::Force{T}, b::T) = Force{T}(a.x*b, a.y*b, a.z*b)
*{T<:Real}(a::T, b::Force{T}) = b*a
.*{T<:Real}(a::Force{T}, b::T) = Force{T}(a.x*b, a.y*b, a.z*b)
.*{T<:Real}(a::T, b::Force{T}) = b.*a
/{T<:Real}(a::Force{T}, b::T) = Force{T}(a.x/b, a.y/b, a.z/b)

end # module

