using PyPlot
using Distributions

# Create a 3D isonormal distribution

sig = [1., 1., 0.03]

dist = MvNormal(sig)

# Sample the distribution

data = rand(dist, 100000)

# Now split data into x,y,z
x = data[1,:];
y = data[2,:];
z = data[3,:];

Qx = 64.31
Qy = 59.32





# # Plot the Distribution

figure()
scatter3D(x,y,z, c="green", alpha=0.3)
xlabel("X")
ylabel("Y")
zlabel("Z")
xlim(-5,5)
ylim(-5,5)
zlim(-5,5)





#
#
# immutable myBunch
#   sig::Vector{Float64}
#   N::Int64
# #   x::Vector{Float64}
# #   y::Vector{Float64}
# #   z::Vector{Float64}
#
#
#
#   # function makeBunch(sig, N)
#   #   println("$sig")
#   #   # d = MvNormal(sig)
#   #   # data = rand(d, N)
#   #   # x = data[1,:]
#   #   # y = data[2,:]
#   #   # z = data[3,:]
#   # end
#
# end
workspace()
#
# d = myBunch([1.,1.,1.], 1000)
