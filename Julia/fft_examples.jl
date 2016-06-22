using PyPlot

## Define my data as a step function

x = [abs(x)<=1 ? 1 : 0 for x in -5:0.1:5]


## Get the FFT of the data
f = fft(x)

## Shift the result to make the zero-frequency component
F = fftshift(f)

## Plot the data the fft and the fft-shifted
plt[:figure]()
plt[:plot](x, "g-", label="Data")
plt[:plot](f, "b:", label="F=F{Data}")
plt[:plot](F, "r--", label="F_{shift}{Data}")
plt[:tight_layout]()
plt[:legend]()



## Now look at the inverse
##
## I can get back my data by inverse-shifting and inverse-Fourriering...

y = ifft(ifftshift(F))

plt[:figure]()
plt[:plot](x, label="Initial Data")
plt[:plot](y, "r--", label="Inverse Fourier Data")
plt[:tight_layout]()
plt[:legend]()




###########################################################
#########                                      ############
######### The same Snippet in Python would be: ############
#########                                      ############
###########################################################
#
#     ../Python/fft_example.py
#

# import matplotlib.pyplot as plt
# import numpy as np


# ## Define your data array x
# x = [1 if np.abs(t)<=1 else 0 for t in np.arange(-5,5,0.1)]

# ## Get the FFT of your data
# f = np.fft.fft(x)

# ## Shift the fft so that the zero frequency is at the center of the spectrum
# F = np.fft.fftshift(f)

# ## Now make the plots of the data, the fft and the fft-shifted
# plt.figure()
# plt.plot(x, "g-", label="Data")
# plt.plot(f, "b:", label="F=F{Data}")
# plt.plot(F, "r--", label="F_{shift}{Data}")
# plt.tight_layout()
# plt.legend()
# plt.show()


# ## Look at the inverse
# ##
# ## I can get back my data by inverse-shifting and inverse-Fourriering...

# y = np.fft.ifft(np.fft.ifftshift(F))

# plot.figure()
# plt.plot(x, label="Initial Data")
# plt.plot(y, "r--", label="Inverse Fourier Data")
# plt.tight_layout()
# plt.legend()
# plt.show()


