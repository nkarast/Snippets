##
##	Script to manipulate MATLAB data structures
##


## Start by importing the scipy io module:
import scipy.io as sio


## Then use the loadmat/savemat/whosmat functions

data = sio.loadmat("/Users/nkarast/Temp/mainbunch_000000.mat", squeeze_me=True, struct_as_record=False)

print data
print data['particles'].ParticleIdNumber[0]

