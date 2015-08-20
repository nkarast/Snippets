#	Snippet to demonstrate the progress bar
#
import time  #! for the sleep func
#
from progressbar import *


# initialise the progress bar
progress = ProgressBar()

# Then loop over something and look at the progress bar growing
for i in progress(range(80)):
  time.sleep(0.01)



####
####	Or more impressive ...
####

def ETAbar():
    widgets = ['Test: ', Percentage(), ' ', Bar(marker=RotatingMarker()),
               ' ', ETA(), ' ', FileTransferSpeed()]
    pbar = ProgressBar(widgets=widgets, maxval=10000000).start()
    for i in range(1000000):
        # do something
        pbar.update(10*i+1)
    pbar.finish()



ETAbar()