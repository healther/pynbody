module MyKutta

export dopri

using MyParticle
using MyForce

function runge{T<:Real}(f::Function, y::Any, h::T, a::Array{T}, b::Array{T}, c::Array{T})
    s = size(c, 1)
    k = Array(typeof(y), s)
    yn = deepcopy(y)
    for i = 1:s
        yn = y
        t = c[i]*h
        for j = 1:i-1
            yn += a[i,j].*k[j]
        end
        k[i] = f(yn)*h
    end
    if size(b)[1]==2
        out = Array(typeof(y), 2)
        out[1]=y
        out[2]=y
        for i =1:s
            out[1] += b[1,i].*k[i]
            out[2] += b[2,i].*k[i]
        end
        return out
    else 
        yn = y
        for i =1:s
            yn += b[i].*k[i]
        end
        return yn
    end
end

function dopri{T<:Real}(f::Function, y::Any, h::T, tol::T)
    n = size(y,1)
    dt = 0.
    a = [0. 0. 0. 0. 0. 0. 0.;
        1./5. 0. 0. 0. 0. 0. 0.;
        3./40. 9./40. 0. 0. 0. 0. 0.;
        44./45. -56./15. 32./9. 0. 0. 0. 0.;
        19372./6561. -25360./2187. 64448./6561. -212./729. 0. 0. 0.;
        9017./3168. -355./33. 46732./5247. 49./176. -5103./18656. 0. 0.;
        35./384. 0. 500./1113. 125./192. -2187./6784. 11./84. 0.]
    b = [5179./57600. 0. 7571./16695. 393./640. -92097./339200. 187./2100. 1./40.;
        35./384. 0. 500./1113. 125./192. -2187./6784. 11./84. 0.]
    c = [0. .2 .3 .8 8./9. 1. 1.]

    hh = copy(h)
    out = Array(typeof(y), 2)
    iter = 0
    while true
        #h = hh-dt
        out = runge(f, y, h, a, b, c)
        res = zero(T)
        for i = 1:n
            res += pnorm2(out[1][i]-out[2][i])
        end
        if res<tol
            dt += h
        else
            h /= 2.
        end
        if dt>=hh 
            break
        end
        iter += 1
    end
    println(iter, "  ", dt)
    out[2]
end

end # module