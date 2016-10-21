using PyPlot
using SymPy

#
#   Assume motion in 2D under the force:
#       Fx = -m*(w1)^2 * x , Fy = -m*(w2)^2 * y
#
#   The solutions are : x(t) = A*cos(w1*t) , y(t) = A*sin(w2*t)
#
#   The solutios for the following conditions are:
#   x(0)= A, y(0)=0, x'(0)=0, y'(0)=w2*A

x  = Float64[]
y  = Float64[]
z  = Float64[]
vx = Float64[]
vy = Float64[]
vz = Float64[]

println(typeof(x))

## Asume that the frequencies are given by the user:
#w1, w2 = input("The frequencies w1, w2 [separated by comma] : ")

# x(0) = 5
# x'(0) = 0

#X, Y, Z, A, B, C, D, T = sp.Symbols("X Y A B C D T")



w1 = 3.
w2 = 5.
w3 = 7.

## Also the total time and time step
#tf, dt = input("Total simulation time (tf) and time step (dt) [separated by comma] : ")
tf = 10.
dt = 0.1

## Print out the confiurations:
println("Frequencies (w1, w2, w3) = ($w1, $w2, $w3)")
println("Time and time step (tf, dt) = ($tf, $dt)")


# Time loop
t = 0.0:dt:tf
println(t)

for mtime in t
    push!(x, cos(w1*mtime))
    push!(y, sin(w2*mtime))
    push!(vx, -w1*sin(w1*mtime))
    push!(vy, w2*cos(w2*mtime))
end





fig = figure(figsize=(10,10))
subplot(221)
plot(t,x, "r--", label="x")
plot(t,y, "b-", label="y")
xlabel("Time")
ylabel("X,Y")
plt[:legend]()

subplot(222)
plot(t,vx, "r--", label="Vx")
plot(t,vy, "b-", label="Vy")
xlabel("Time")
ylabel("Vx,Vy")
plt[:legend]()

subplot(223)
plot(x,vx, "r--", label="Phase Space (X)")
xlabel("X")
ylabel("Vx")
plt[:legend]()

subplot(224)
plot(y,vy, "r--", label="Phase Space (Y)")
xlabel("Y")
ylabel("Vy")
plt[:legend]()
fig[:canvas][:draw]()
