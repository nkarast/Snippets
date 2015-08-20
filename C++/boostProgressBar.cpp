#include <boost/progress.hpp>
#include <stdlib.h> // for the sleep function

//! Maximum number the loop can take:
unsigned int nentries = 10000;

//! Create the progressbar
boost::progress_display show_progress(nentries);


for(unsigned int jentry = 0; jentry<nentries; jentry++){
	//! do some stuff then show the progress bar
	sleep(2000); // sleep is in msec


	++show_progress;

	}// for event