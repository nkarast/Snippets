#
#	Calculate luminosity, pileup, lifetime and levelling times
#	Based on the work of S. Fartoukh
#
#	Author: Nikos Karastathis  ( nkarast <at> cern <dot> ch )
#	Version: 0.2

"""<DOCSTRING MODULE beamCal>
	module : beamCal - Numerical Calculation of machine performance standards based on beam parameters
Author : Nikos Karastathis (nkarast <at> cern <dot> ch)
Version: 0.2
--------------------------------------------------------
This is a collection of functions that numerically calculate the performance standards (luminosity, pileup, levelling time, beam lifetime, etc)
of an accelerator machine (here defaults to HL-LHC), based on beam and machine parameters.

Prerequisites: Scipy Stack i.e. NumPy, SciPy [optionally SymPy, Matplotlib]

Available functions:
--------------------

Module Functions:
		- createRange
		- help

Class: BeamCal
		- setLogFile
		- setLogLevel
		- setBeamProfile
		- setPlotOption
		- setNb0
		- setNpart0
		- setNrj0
		- setEmitnX0
		- setEmitX0
		- setEmitnY0
		- setEmitY0
		- setCircum
		- setFrev0
		- setSig0
		- setHrf400
		- setOmegaCC0
		- setVRF0
		- setVRFx0
		- setVRFy0
		- setLlevel0
		- setAlpha0
		- rho
		- plotProfiles
		- kernel
		- density
		- Rloss
		- mu2D
		- muz
		- mut
		- siglumz
		- siglumt
		- Life
		- TLev
		- Lumi
		- mutot
		- myLumi
		- myMutot
		- myMuz
		- myLumz
		- runLumi_XB
		- runLimi_XBI
		- runLumi_XS
		- runLimi_XSI
		- runMuz_XB
		- runMuz_XBI
		- runMuz_XS
		- runMuz_XSI
		- runLumz_XB
		- runLumz_XBI
		- runLumz_XS
		- runLumz_XSI
		- runXBI
		- runXSI
		- printConfig
"""

####################################################################################################


import numpy as np
from scipy.integrate import quad, dblquad
from logging import *

class BeamCal:
	####################################################################################################
	#
	#	EXECUTION OPTIONS
	#
	####################################################################################################
	def __init__(self):
		self.plotSample				= False
		self.beamProfile			= "gauss" #"flat" # "cos2"
		self.logfile				= None
		self.loglevel				= DEBUG

		#imports based on options
		if self.plotSample:
			import matplotlib.pyplot as plt
		if (self.beamProfile != "gauss") or self.plotSample:
			from sympy.functions.special.delta_functions import Heaviside
			from sympy.functions.special.gamma_functions import gamma
		basicConfig(format='%(asctime)s %(levelname)s : %(message)s', filename=self.logfile, level=self.loglevel)


	####################################################################################################
	#
	#	CONSTANT AND DEFAULT PARAMETERS
	#
	####################################################################################################
		self.Clight 				= 299792458. 				# speed of light [m/s]
		self.Qe 					= 1.60217733e-19  			# electron charge [C]
		self.sigprotoninelas 		= 0.085  					# inelastic hadron cross section [barn]
		self.sigtotproton 			= 0.111   					# inelastic hadron cross section [barn]
		self.Mproton 				= 0.93827231  				# proton mass [GeV]

	####################################################################################################
	#
	#	CURRENT SETUP PARAMETERS : NOMINAL SCENARIO AT 5e34
	#							   SNAPSHOT AT THE BEGGINING AND END OF THE COAST
	#
	####################################################################################################
		self.Nb0 			= 2736. #2556 - LHC  				# number of collision at IP1 and IP5
		self.Npart0 		= 1.25e11 							# bunch charge at begining of coast
		self.Nrj0 			= 7000. #6500. - LHC				# collision energy [GeV]
		self.gamma0 		= self.Nrj0/self.Mproton			# relativisitc factor
		self.emitX0  		= 2.5e-06/self.gamma0 				# r.m.s. horizontal physical emittance in collision
		self.emitY0  		= 2.5e-06/self.gamma0 				# r.m.s. vertical physical emittance in collision
		self.circum			= 26658.8832						# ring circumference [m]
		self.sigz0			= 0.081 							# default r.m.s. bunch length [m]
		self.frev0 			= self.Clight/self.circum 			# LHC revolution frequency at flat top
		self.hrf400 		= 35640. 							# LHC harmonic number for 400 Mhz
		self.omegaCC0 		= self.hrf400*self.frev0/self.Clight*2.*np.pi 		# default omega/c for 400 MHz crab-cavities
		self.VRF0 			= 11.4 								# reference CC voltage for full crabbing at 590 murad crossing angle
		self.VRFx0 			= 6.8 # 0. # LHC no CC				# CC voltage [MV] in crossing plane for 2 CCs
		self.VRFy0 			= 0.0 								# default CC voltage [MV] in parallel plane
		self.Llevel0 		= 5. 								# Default Level luminosity [10**34]
		self.alpha0 		= 590.e-06 							# Default full crossing angle
		self.bx0 			= 0.15  							# default H beta*
		self.by0 			= 0.15   							# default V beta*
		self.sepx0 			= 0 								# Default H separation in units of sigma
		self.sepy0 			= 0


	####################################################################################################
	#
	#	ACCESSOR FUNCTIONS
	#
	####################################################################################################
	def setLogfile(self, nlogfile):
		info("[Logfile] %s --> %s" %(self.logfile,nlogfile))
		self.logfile = nlogfile

	def getLogfile(self):
		return self.logfile

	def setLogLevel(self, level):
		info("[Loglevel] %s --> %s" % (self.loglevel, level))
		self.loglevel = level

	def getLogLevel(self):
		return self.loglevel

	def setBeamProfile(self, nbeamProfile):
		info("[Beam Profile] %s --> %s" % (self.beamProfile,nbeamProfile))
		self.beamProfile = nbeamProfile

	def getBeamProfile(self):
		return self.beamProfile

	def setPlotOption(self, nbool):
		info("[Plot Option] %s --> %s" % (self.plotSample,nbool))
		self.plotSample=nbool

	def setNb0(self, nNb0):
		info("[Nb0] %s --> %s" % (self.Nb0,nNb0))
		self.Nb0 = nNb0

	def getNb0(self):
		return self.Nb0

	def setNpart0(self, nNpart0):
		info("[Npart0] %.15f --> %.15f" % (self.Npart0,nNpart0))
		self.Npart0 = nNpart0

	def getNpart0(self):
		return self.Npart0

	def setNrj0(self, nNrj0):
		info("[Nrj0] %s --> %s (gamma: %s --> %s)" % (self.Nrj0,nNrj0, self.gamma0, nNrj0/self.Mproton))
		self.Nrj0 = nNrj0

	def getNrj0(self):
		return self.Nrj0

	def setEmitnX0(self, nemitnX0):
		info("[emitnX0] %s --> %s (Physical: %s --> %s)" % (self.emitX0*self.gamma0,nemitnX0, self.emitX0, nemitnX0/self.gamma0))
		self.emitX0 = nemitnX0/self.gamma0

	def getEmitnX0(self):
		return self.emitX0*self.gamma0

	def getEmitX0(self):
		return self.emitX0

	def setEmitnY0(self, nemitnY0):
		info("[emitnY0] %s --> %s (Physical: %s --> %s)" % (self.emitY0*self.gamma0,nemitnY0, self.emitY0, nemitnY0/self.gamma0))
		self.emitY0 = nemitnY0/self.gamma0

	def getEmitnY0(self):
		return self.emitY0*self.gamma0

	def getEmitY0(self):
		return self.emitY0

	def setCircum(self, ncircum):
		info("[circum] %s --> %s (Revolution Frequency at Flat Top: %s --> %s)"% (self.circum, ncircum, self.frev0, self.Clight/ncircum))
		self.circum = ncircum

	def getCircum(self):
		return self.circum

	def setFrev0(self, nfrev0):
		info("Force [frev0] %s --> %s" % (self.frev0, nfrev0))
		self.frev0 = nfrev0

	def getFrev0(self):
		return self.frev0

	def setSigz0(self, nsigz0):
		info("[sig0] %s --> %s"% (self.sigz0, nsigz0))
		self.sigz0 = nsigz0

	def getSigz0(self):
		return self.sigz0

	def setHrf400(self, nhrf400):
		info("[hrf400] %s --> %s (omegaCC0: %s --> %s)" % (self.hrf400, nhrf400, self.omegaCC0, nhrf400*self.frev0/self.Clight*2.*np.pi))
		self.hrf400 = nhrf400

	def getHrf400(self):
		return self.hrf400

	def setOmegaCC0(self, nomegacc0):
		info("Force [omegaCC0] %s --> %s" % (self.omegaCC0, nomegacc0))
		self.omegaCC0 = nomegacc0

	def getOmegaCC0(self):
		return self.omegaCC0

	def setVRF0(self, nVRF0):
		info("[VRF] %s --> %s" %(self.VRF0, nVRF0))
		self.VRF0 = nVRF0

	def getVRF0(self):
		return self.VRF0

	def setVRFx0(self, nVRFx0):
		info("[VRFx] %s --> %s" %(self.VRFx0, nVRFx0))
		self.VRFx0 = nVRFx0

	def getVRFx0(self):
		return self.VRFx0

	def setVRFy0(self, nVRFy0):
		info("[VRFy] %s --> %s" %(self.VRFy0, nVRFy0))
		self.VRFy0 = nVRFy0

	def getVRFy0(self):
		return self.VRFy0

	def setLlevel0(self, nLlevel):
		info("[Llevel] %s --> %s" %(self.Llevel0, nLlevel))
		self.Llevel0 = nLlevel

	def getLlevel0(self):
		return self.Llevel0

	def setAlpha0(self, nalpha0):
		info("[alpha] %s --> %s" % (self.alpha0, nalpha0))
		self.alpha0 = nalpha0

	def getAlpha0(self):
		return self.alpha0



	####################################################################################################
	#
	#	FUNCTIONS
	#
	####################################################################################################

	# - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - -
	def rho(self, z,sigz):
		'''
		Typical longutudinal bunch distributions as a function of z [m], normalized to 1 and centered at 0.0 with a given r.m.s. of sigz [m]
		Input   : z, sigz
		Returns : The value taken from the beam profile for the specific combination of z and sigz
		'''
		if self.beamProfile == "gauss":
			return 1./np.sqrt(2.*np.pi)/sigz*np.exp(-(z*z)/2/(sigz*sigz))
		elif self.beamProfile == "cos2":
			return 1./(np.sqrt(3)*np.pi*sigz/np.sqrt(np.pi*np.pi -6))*(np.cos(np.pi*z/(2*np.sqrt(3)*np.pi*sigz/np.sqrt(np.pi*np.pi -6))))**2*Heaviside(1-np.fabs(z)/(np.sqrt(3)*np.pi*sigz/np.sqrt(np.pi*np.pi -6)))
		elif self.beamProfile == "flat":
			return 2**(5./4.)*np.sqrt(np.pi)/gamma(1./4.)**2/sigz*np.exp(-1./2.*(z/(gamma(1./4.)*sigz/np.sqrt(2.*np.pi)))**4)

	# - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - -
	def plotProfiles(self, z=np.linspace(-0.20,0.20,80,endpoint=True) , sigz=None ,currBeamProfile=None):
		'''
		Make a sample plot of the longitudinal bunch distributions available in the code
		Input : z: np.linspace for plotting
				sigz : bunchlength
				currbeamprofile: the current beam profile to reset it before exiting
		Returns: A plot with the 3 different distributions.
		'''
		if sigz is None:
			sigz = self.sigz0
		if currBeamProfile is None:
			currBeamProfile = self.beamProfile

		beamProfile = "gauss"
		gauss = [rho(zi,sigz) for zi in z]
		beamProfile = "cos2"
		cos2  = [rho(zi,sigz) for zi in z]
		beamProfile = "flat"
		flat  = [rho(zi,sigz) for zi in z]
		# restore the current profile
		beamProfile = currBeamProfile
		fig, ax = plt.figure()
		ax.plot(z, gauss, 'k-',  lw=3, label="Gauss")
		ax.plot(z, cos2,  'k--', lw=3, label="Cos2")
		ax.plot(z, gauss, 'r-',  lw=3, label="Flat")
		ax.legend(loc='best')
		plt.show()


	# - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - -
	def kernel(self, z, t, bx, by, alpha, dx, dy, VRFx, VRFy, omegaCCx, omegaCCy, emitnx, emitny):
		'''
		Kernel function
		'''
		return 1/np.sqrt(1 + (z/bx)**2)/np.sqrt(1 + (z/by)**2)*np.exp(-((dx*np.sqrt(bx*emitnx) + alpha*z - self.alpha0/omegaCCx/self.VRF0*(VRFx*np.cos(omegaCCx*t)*np.sin(omegaCCx*z)))/(2*np.sqrt(bx*emitnx))/np.sqrt(1 + (z/bx)**2))**2)*np.exp(-((dy*np.sqrt(by*emitny) + VRFy/self.VRF0*self.alpha0/omegaCCy*np.sin(omegaCCy*t)*np.cos(omegaCCy*z))/(2*np.sqrt(by*emitny))/np.sqrt(1 + (z/by)**2))**2)


	# - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - -
	def density(self, z, t, bx, by, alpha, dx, dy, VRFx, VRFy, omegaCCx, omegaCCy, sigz, emitnx, emitny):
		'''
		Non-normalized 2D pileup density -- Depends on rho function return value and beam profile
		'''
		return 2*self.kernel(z, t, bx, by, alpha, dx, dy, VRFx, VRFy, omegaCCx, omegaCCy, emitnx, emitny)*self.rho(z - t, sigz)*self.rho(z + t, sigz)


	# - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - -
	def Rloss(self, bx, by, alpha, dx, dy, VRFx, VRFy, omegaCCx, omegaCCy, sigz, emitnx, emitny):
		'''
		Generalized Loss factor - the double integral of density for z, t in the range of (-inf,inf)
		'''
		return dblquad(lambda mt, mz: self.density(mz, mt, bx, by, alpha, dx, dy, VRFx, VRFy, omegaCCx, omegaCCy, sigz, emitnx, emitny), -np.inf, np.inf, lambda x: -np.inf, lambda x: np.inf)[0]


	# - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - -
	def mu2D(self, z, t, bx, by, alpha, dx, dy, VRFx, VRFy, omegaCCx, omegaCCy, sigz, emitnx, emitny, mutot, lossfactor):
		'''
		Normalized 2D pileup density evt/mm/ps vs z[m] and t[ns]
		WARNING : mutot is a function of lumi!
		Inputs:  mutot      = total pileup for given luminosity
				 lossfactor = Rloss return value
		'''
		return mutot*self.density(z, self.Clight*t*1.e-09, bx, by, alpha, dx, dy, VRFx, VRFy, omegaCCx, omegaCCy, sigz, emitnx, emitny)/lossfactor*self.Clight*1.e-15


	# - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - -
	def muz(self, z, bx, by, alpha, dx, dy, VRFx, VRFy, omegaCCx, omegaCCy, sigz, emitnx, emitny, mutot, lossfactor):
		'''
		Normalized line pileup density [evt/mm] vs z [m]
		'''
		def intergrand(t, z, bx, by, alpha, dx, dy, VRFx, VRFy, omegaCCx, omegaCCy, sigz, emitnx, emitny):
			return self.density(z, t, bx, by, alpha, dx, dy, VRFx, VRFy, omegaCCx, omegaCCy, sigz, emitnx, emitny)

		return 1.0e-03*mutot/lossfactor*quad(intergrand, -np.inf, np.inf, args=(z, bx, by, alpha, dx, dy, VRFx, VRFy, omegaCCx, omegaCCy, sigz, emitnx, emitny))[0] # remember all quads return (value, abs_error)


	# - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - -
	def mut(self, t, bx, by, alpha, dx, dy, VRFx, VRFy, omegaCCx, omegaCCy, sigz, emitnx, emitny, mutot, lossfactor):
		'''
		Normalized time pileup density [evt/ps] vs. time [ns]
		'''
		def intergrand(z, t, bx, by, alpha, dx, dy, VRFx, VRFy, omegaCCx, omegaCCy, sigz, emitnx, emitny):
			return self.density(z, self.Clight*t*1.e-09, bx, by, alpha, dx, dy, VRFx, VRFy, omegaCCx, omegaCCy, sigz, emitnx, emitny)
		return self.Clight*1.e-12*mutot/lossfactor*quad(intergrand, -np.inf, np.inf, args=(t, bx, by, alpha, dx, dy, VRFx, VRFy, omegaCCx, omegaCCy, sigz, emitnx, emitny, mutot, lossfactor))[0]


	# - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - -
	def siglumz(self, bx, by, alpha, dx, dy, VRFx, VRFy, omegaCCx, omegaCCy, sigz, emitnx, emitny):
		'''
		R.M.S. luminous region [cm]
		'''
		return 100.*np.sqrt(dblquad(lambda mt, mz: self.density(mz, mt, bx, by, alpha, dx, dy, VRFx, VRFy, omegaCCx, omegaCCy, sigz, emitnx, emitny)*mz*mz, -np.inf, np.inf, lambda x: -np.inf, lambda x: np.inf)[0]/self.Rloss(bx, by, alpha, dx, dy, VRFx, VRFy, omegaCCx, omegaCCy, sigz, emitnx, emitny))


	# - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - -
	def siglumt(self, bx, by, alpha, dx, dy, VRFx, VRFy, omegaCCx, omegaCCy, sigz, emitnx, emitny):
		'''
		R.M.S. Collision time [ps]
		'''
		return 1.e12/self.Clight*np.sqrt(dblquad(lambda mt, mz: self.density(mz, mt, bx, by, alpha, dx, dy, VRFx, VRFy, omegaCCx, omegaCCy, sigz, emitnx, emitny)*mt*mt, -np.inf, np.inf, lambda x: -np.inf, lambda x: np.inf)[0]/self.Rloss(bx, by, alpha, dx, dy, VRFx, VRFy, omegaCCx, omegaCCy, sigz, emitnx, emitny))


	# - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - -
	def Tlife(self, Nb, Npart, Llevel):
		'''
		Beam lifetime [h]
		'''
		return Nb*Npart/2./(self.sigtotproton*1.e-24)/(Llevel*1.e34)/3600.


	# - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - -
	def TLev(self, Llevel, frev, Nb, Npart, bx, by, alpha, dx, dy, VRFx, VRFy, omegaCCx, omegaCCy, sigz, emitnx, emitny):
		'''
		Levelling time [h]
		'''
		return  (1. - np.sqrt(Llevel/self.Lumi(frev, Nb, Npart, bx, by, alpha, dx, dy, VRFx, VRFy, omegaCCx, omegaCCy, sigz, emitnx, emitny)))*self.Tlife(Nb, Npart, Llevel)


	# - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - -
	def Lumi(self, frev, Nb, Npart, bx, by, alpha, dx, dy, VRFx, VRFy, omegaCCx, omegaCCy, sigz, emitnx, emitny):
		'''
		Luminosity [10^34 Hz/cm^2]
		'''
		return (self.Rloss(bx, by, alpha, dx, dy, VRFx, VRFy, omegaCCx, omegaCCy, sigz, emitnx, emitny)*1./4./np.pi/np.sqrt(bx*by)/np.sqrt(emitnx*emitny)*frev*Nb*Npart**2)/1e38


	# - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - -
	def myLumi(self, bstar, halfX, sep):
		'''
		Helper function to calculate lumi for the parameters : beta*, halfX and vertical separation
		'''
		return self.Lumi(self.frev0, self.Nb0, self.Npart0, bstar, bstar, 2.e-06*halfX, 0., sep, np.min(np.array([self.VRFx0, halfX/295.*self.VRF0])), 0., self.omegaCC0, self.omegaCC0, self.sigz0, self.emitX0, self.emitY0)


	# - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - -
	def mutot(self, frev, Nb, Npart, bx, by, alpha, dx, dy, VRFx, VRFy, omegaCCx, omegaCCy, sigz, emitnx, emitny):
		'''
		Total pileup for given configuration
		'''
		return (self.Lumi(frev, Nb, Npart, bx, by, alpha, dx, dy, VRFx, VRFy, omegaCCx, omegaCCy, sigz, emitnx, emitny)*1.0e34*self.sigprotoninelas*1.0e-24)/(self.Nb0*self.frev0)


	# - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - -
	def myMutot(self, bstar, halfX, sep):
		'''
		User friendly function : Total pileup for current settings of b*, crossing and vertical separation
		'''
		return (self.myLumi(bstar, halfX, sep)*1.0e34*self.sigprotoninelas*1.0e-24)/(self.Nb0*self.frev0)


	# - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - -
	def myMuz(self, bstar, halfX, sep):
		'''
		User friendly function: Line density for z=0m and changing the mutot with the current luminosity
		'''
		return self.muz(0.0, bstar, bstar, 2.0e-6*halfX, 0.0, sep,  np.min(np.array([self.VRFx0, halfX/295.*self.VRF0])), 0.0, self.omegaCC0, self.omegaCC0, self.sigz0, self.emitX0, self.emitY0, self.myMutot(bstar, halfX, sep), self.Rloss(bstar, bstar, 2.0e-6*halfX, 0.0, sep, np.min(np.array([self.VRFx0, halfX/295.*self.VRF0])), 0.0, self.omegaCC0, self.omegaCC0, self.sigz0, self.emitX0, self.emitY0))


	# - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - -
	def myLumz(self, bstar, halfX, sep):
		'''
		User friendly function: Luminous region for current settings of b*, crossing and vertical separation
		'''
		return self.siglumz(bstar, bstar, 2.0e-06*halfX, 0.0, sep, np.min(np.array([self.VRFx0, halfX/295.*self.VRF0])), 0.0, self.omegaCC0, self.omegaCC0, self.sigz0, self.emitX0, self.emitY0)


	# - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - -
	def runLumi_XB(self, b,x, Npart, emitnx, emitny, s=0.0, outputFileName=None):
		'''
		Calculates the luminosity in units of 10**34 [Hz/cm/cm] for a scan on beta* and crossing for a GIVEN intensity
		Input : b: np.array with the beta* values to scan in [m]  (Example: 0.20 m)
				x: np.array with the half-crossing values to scan in [urad] (Example: 120.0 urad)
				Npart: Bunch intensity [particles] (Example: 2.2e11 particles)
				emitx: Normalized emittance in the horizontal plane in [rad*m] (Example: 2.5e-06 rad m)
				emitx: Normalized emittance in the vertical plane in [rad*m] (Example: 2.5e-06 rad m)
				s: Vertical separation in [/sigma] (Example: 0.2 \sigma)
				outputFileName: Filename to store the return value as tabulated data

		Output: Returns an numpy array filled with three item tuples in the form of (beta* [cm], crossing [um], luminosity [10^34])
		'''

		# Checks if input matches the object parameters, if not change it
		if Npart != self.Npart0:
			self.setNpart0(Npart)
		if emitnx is None:
			emitnx = self.getEmitnX0()
		if (emitnx is not None) and (emitnx != self.getEmitnX0()):
			self.setEmitnX0(emitnx)
		if emitny is None:
			emitny = self.getEmitnY0()
		if (emitny is not None) and (emitny != self.getEmitnY0()):
			self.setEmitnY0(emitny)

		debug("Running XB input values = I=%s, enx=%s,eny=%s" % (Npart, emitnx, emitny))
		info("Running Luminosity Calculation for I=%s, enx=%s,eny=%s | b*=[%s:%s], x=[%s:%s]" % (self.getNpart0(), self.getEmitnX0(), self.getEmitnY0(), np.min(b), np.max(b), np.min(x), np.max(x)))

		lumi = []
		for mb in b:
			for mx in x:
				mlumi = self.myLumi(mb, mx, s)
				lumi.append((mb*100., mx, mlumi))
				debug("(%s\t%s\t%s)"% (mb*100., mx, mlumi))

		if outputFileName is not None:
			np.savetxt(outputFileName, lumi, '%i\t%i\t%.6f')
		return np.array(lumi)


	# - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - -
	def runLumi_XBI(self, b, x, Npart, emitnx, emitny, s=0.0, savefile=False, outputFilePattern="lumi_XBI_I"):
		'''
		Drive routine for the XBI (crossing, beta*, intensity) scans.
		Input:	b: np.array with the beta* values to scan in [m]  (Example: 0.20 m)
				x: np.array with the half-crossing values to scan in [urad] (Example: 120.0 urad)
				Npart: np.array with the bunch intensities to scan [particles] (Example: 2.2e11 particles)
				emitx: np.array with the normalized emittance in the horizontal plane in [rad*m] (Example: 2.5e-06 rad m)
				emitx: np.array with the normalized emittance in the vertical plane in [rad*m] (Example: 2.5e-06 rad m)
				s: Vertical separation in [/sigma] (Example: 0.2 \sigma)
				savefile: Boolean that determines if the lumi results will be stored in a tabulated text file
				outputFilePattern: Part of the filename to be stored. The routine will fill the intensity value and the suffix.
		'''
		# if len(Npart) > 1:
		# 	debug("Running for multiple intensities... [%s]" % Npart)
		if len(emitnx) != len(emitny):
			critical("# runLumi_XBI: Different size input for emittances!")
			raise ValueError("Different size input for emittances")
		elif len(emitnx) > 1:
			if len(emitnx) != len(Npart):
				critical("# runLumi_XBI: Mismatch in the length of intensities and emittances")
				raise ValueError("Mismatch in the length of intensities and emittances")
			else:
				warn("# runLumi_XBI: Hopefully you have ordered your intensities and emittances properly, my dear user...")
				for Np, ex, ey in zip(Npart, emitnx, emitny):
					info("Running Lumi XBI for I=%s, enx=%s, eny=%s and b=[%s:%s], x=[%s:%s]" % (Npart, emitnx, emitny, np.min(b), np.max(b), np.min(x), np.max(x)))
					if savefile:
						mfilename = outputFilePattern+str(Np/(1.0e11))+".txt"
						self.runLumi_XB(b,x, Np, ex, ey, s=s, outputFileName=mfilename)
					else:
						self.runLumi_XB(b,x, Np, ex, ey, s=s, outputFileName=None)


	# - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - -
	def runLumi_XS(self, s,x, Npart, emitnx, emitny, b=0.20, outputFileName=None):
		'''
		Calculates the luminosity in units of 10**34 [Hz/cm/cm] for a scan on separation and crossing for a GIVEN intensity & emittance
		Input : s: np.array with the separation values to scan in [\sigma]  (Example: 0.20 \sigma)
				x: np.array with the half-crossing values to scan in [urad] (Example: 120.0 urad)
				Npart: Bunch intensity [particles] (Example: 2.2e11 particles)
				emitx: Normalized emittance in the horizontal plane in [rad*m] (Example: 2.5e-06 rad m)
				emitx: Normalized emittance in the vertical plane in [rad*m] (Example: 2.5e-06 rad m)
				b: Beta* value [m] (Example: 0.20 m)

		Output: Returns an numpy array filled with three item tuples in the form of (separation [\sigma] crossing [um], luminosity [10^34])
		'''
		#pass
		# Check if input matches the object parameters, if not change it

		if Npart != self.Npart0:
			self.setNpart0(Npart)
		if emitnx is None:
			emitnx = self.getEmitnX0()
		if (emitnx is not None) and (emitnx != self.getEmitnX0()):
			self.setEmitnX0(emitnx)
		if emitny is None:
			emitny = self.getEmitnY0()
		if (emitny is not None) and (emitny != self.getEmitnY0()):
			self.setEmitnY0(emitny)

		debug("Running XB input values = I=%s, enx=%s,eny=%s" % (Npart, emitnx, emitny))
		info("Running Luminosity Calculation for I=%s, enx=%s,eny=%s | s=[%s:%s], x=[%s:%s]" % (self.getNpart0(), self.getEmitnX0(), self.getEmitnY0(), np.min(s), np.max(s), np.min(x), np.max(x)))

		lumi = []
		for ms in s:
			for mx in x:
				mlumi = self.myLumi(b, mx, ms)
				lumi.append((ms, mx, mlumi))
				debug("(%s\t%s\t%s)"% (ms, mx, mlumi))

		if outputFileName is not None:
			np.savetxt(outputFileName, lumi, '%.3f\t%i\t%.6f')
		return np.array(lumi)


	# - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - -
	def runLumi_XSI(self, s, x, Npart, emitnx, emitny, b=0.20, savefile=False, outputFilePattern="lumi_XSI_I"):
		'''
		Drive routine for the XSI (crossing, separation, intensity) scans.
		Input:	s: np.array with the separation values to scan in [\sigma]  (Example: 0.20 \sigma)
				x: np.array with the half-crossing values to scan in [urad] (Example: 120.0 urad)
				Npart: np.array with the bunch intensities to scan [particles] (Example: 2.2e11 particles)
				emitx: np.array with the normalized emittance in the horizontal plane in [rad*m] (Example: 2.5e-06 rad m)
				emitx: np.array with the normalized emittance in the vertical plane in [rad*m] (Example: 2.5e-06 rad m)
				b: Beta* value [m] (Example: 0.20 m)
				savefile: Boolean that determines if the lumi results will be stored in a tabulated text file
				outputFilePattern: Part of the filename to be stored. The routine will fill the intensity value and the suffix.
		'''

		if len(Npart) > 1:
			debug("Running for multiple intensities... [%s]" % Npart)
			if len(emitnx) != len(emitny):
				critical("# runLumi_XSI: Different size input for emittances!")
				raise ValueError("Different size input for emittances")
			elif len(emitnx) > 1:
				if len(emitnx) != len(Npart):
					critical("# runLumi_XSI: Mismatch in the length of intensities and emittances")
					raise ValueError("Mismatch in the length of intensities and emittances")
				else:
					warn("# runLumi_XSI: Hopefully you have ordered your intensities and emittances properly, my dear user...")
					for Np, ex, ey in zip(Npart, emitnx, emitny):
						info("Running Lumi XSI for I=%s, enx=%s, eny=%s and s=[%s:%s], x=[%s:%s]" % (Npart, emitnx, emitny, np.min(s), np.max(s), np.min(x), np.max(x)))
						if savefile:
							mfilename = outputFilePattern+str(Np/(1.0e11))+".txt"
							self.runLumi_XS(s,x, Np, ex, ey, b=b, outputFileName=mfilename)
						else:
							self.runLumi_XS(s,x, Np, ex, ey, b=b, outputFileName=None)


	# - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - -
	def runMuz_XB(self, b,x, Npart, emitnx, emitny, s=0.0, outputFileName=None):
		'''
		Calculates the line pileup density for z=0 in units of [evt/mm] vs z [m] for a scan on beta* and crossing for a GIVEN intensity
		Input : b: np.array with the beta* values to scan in [m]  (Example: 0.20 m)
				x: np.array with the half-crossing values to scan in [urad] (Example: 120.0 urad)
				Npart: Bunch intensity [particles] (Example: 2.2e11 particles)
				emitx: Normalized emittance in the horizontal plane in [rad*m] (Example: 2.5e-06 rad m)
				emitx: Normalized emittance in the vertical plane in [rad*m] (Example: 2.5e-06 rad m)
				s: Vertical separation in [/sigma] (Example: 0.2 \sigma)
				outputFileName: Filename to store the return value as tabulated data

		Output: Returns an numpy array filled with three item tuples in the form of (beta* [cm], crossing [um], line pileup [evt/mm])
		'''

		# Checks if input matches the object parameters, if not change it
		if Npart != self.Npart0:
			self.setNpart0(Npart)
		if emitnx is None:
			emitnx = self.getEmitnX0()
		if (emitnx is not None) and (emitnx != self.getEmitnX0()):
			self.setEmitnX0(emitnx)
		if emitny is None:
			emitny = self.getEmitnY0()
		if (emitny is not None) and (emitny != self.getEmitnY0()):
			self.setEmitnY0(emitny)

		debug("Running XB input values = I=%s, enx=%s,eny=%s" % (Npart, emitnx, emitny))
		info("Running Line Pileup Density Calculation for I=%s, enx=%s,eny=%s | b*=[%s:%s], x=[%s:%s]" % (self.getNpart0(), self.getEmitnX0(), self.getEmitnY0(), np.min(b), np.max(b), np.min(x), np.max(x)))

		pz = []
		for mb in b:
			for mx in x:
				mpz = self.myMuz(mb, mx, s)
				pz.append((mb*100., mx, mpz))
				debug("(%s\t%s\t%s)"% (mb*100., mx, mpz))

		if outputFileName is not None:
			np.savetxt(outputFileName, pz, '%i\t%i\t%.6f')
		return np.array(pz)


	# - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - -
	def runMuz_XBI(self, b, x, Npart, emitnx, emitny, s=0.0, savefile=False, outputFilePattern="muz_XBI_I"):
		'''
		Drive routine for the XBI (crossing, beta*, intensity) scans.
		Input:	b: np.array with the beta* values to scan in [m]  (Example: 0.20 m)
				x: np.array with the half-crossing values to scan in [urad] (Example: 120.0 urad)
				Npart: np.array with the bunch intensities to scan [particles] (Example: 2.2e11 particles)
				emitx: np.array with the normalized emittance in the horizontal plane in [rad*m] (Example: 2.5e-06 rad m)
				emitx: np.array with the normalized emittance in the vertical plane in [rad*m] (Example: 2.5e-06 rad m)
				s: Vertical separation in [/sigma] (Example: 0.2 \sigma)
				savefile: Boolean that determines if the lumi results will be stored in a tabulated text file
				outputFilePattern: Part of the filename to be stored. The routine will fill the intensity value and the suffix.
		'''
		if len(Npart) > 1:
			debug("Running for multiple intensities... [%s]" % Npart)
			if len(emitnx) != len(emitny):
				critical("# runMuz_XBI: Different size input for emittances!")
				raise ValueError("Different size input for emittances")
			elif len(emitnx) > 1:
				if len(emitnx) != len(Npart):
					critical("# runMuz_XBI: Mismatch in the length of intensities and emittances")
					raise ValueError("Mismatch in the length of intensities and emittances")
				else:
					warn("# runMuz_XBI: Hopefully you have ordered your intensities and emittances properly, my dear user...")
					for Np, ex, ey in zip(Npart, emitnx, emitny):
						info("Running Line Pileup Density XBI for I=%s, enx=%s, eny=%s and b=[%s:%s], x=[%s:%s]" % (Npart, emitnx, emitny, np.min(b), np.max(b), np.min(x), np.max(x)))
						if savefile:
							mfilename = outputFilePattern+str(Np/(1.0e11))+".txt"
							self.runMuz_XB(b,x, Np, ex, ey, s=s, outputFileName=mfilename)
						else:
							self.runMuz_XB(b,x, Np, ex, ey, s=s, outputFileName=None)


	# - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - -
	def runMuz_XS(self, s,x, Npart, emitnx, emitny, b=0.20, outputFileName=None):
		'''
		Calculates the line pileup density for z=0 in units of [evt/mm] vs z [m] for a scan on beta* and crossing for a GIVEN intensity
		Input : b: np.array with the beta* values to scan in [m]  (Example: 0.20 m)
				x: np.array with the half-crossing values to scan in [urad] (Example: 120.0 urad)
				Npart: Bunch intensity [particles] (Example: 2.2e11 particles)
				emitx: Normalized emittance in the horizontal plane in [rad*m] (Example: 2.5e-06 rad m)
				emitx: Normalized emittance in the vertical plane in [rad*m] (Example: 2.5e-06 rad m)
				s: Vertical separation in [/sigma] (Example: 0.2 \sigma)
				outputFileName: Filename to store the return value as tabulated data

		Output: Returns an numpy array filled with three item tuples in the form of (beta* [cm], crossing [um], line pileup [evt/mm])
		'''

		# Checks if input matches the object parameters, if not change it
		if Npart != self.Npart0:
			self.setNpart0(Npart)
		if emitnx is None:
			emitnx = self.getEmitnX0()
		if (emitnx is not None) and (emitnx != self.getEmitnX0()):
			self.setEmitnX0(emitnx)
		if emitny is None:
			emitny = self.getEmitnY0()
		if (emitny is not None) and (emitny != self.getEmitnY0()):
			self.setEmitnY0(emitny)

		debug("Running XB input values = I=%s, enx=%s,eny=%s" % (Npart, emitnx, emitny))
		info("Running Line Pileup Density Calculation for I=%s, enx=%s,eny=%s | s=[%s:%s], x=[%s:%s]" % (self.getNpart0(), self.getEmitnX0(), self.getEmitnY0(), np.min(s), np.max(s), np.min(x), np.max(x)))

		pz = []
		for ms in s:
			for mx in x:
				mpz = self.myMuz(b, mx, ms)
				pz.append((ms, mx, mpz))
				debug("(%s\t%s\t%s)"% (ms, mx, mpz))

		if outputFileName is not None:
			np.savetxt(outputFileName, pz, '%.3f\t%i\t%.6f')
		return np.array(pz)


	# - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - -
	def runMuz_XSI(self, s, x, Npart, emitnx, emitny, b=0.20, savefile=False, outputFilePattern="muz_XSI_I"):
		'''
		Drive routine for the XBI (crossing, beta*, intensity) scans.
		Input:	b: np.array with the beta* values to scan in [m]  (Example: 0.20 m)
				x: np.array with the half-crossing values to scan in [urad] (Example: 120.0 urad)
				Npart: np.array with the bunch intensities to scan [particles] (Example: 2.2e11 particles)
				emitx: np.array with the normalized emittance in the horizontal plane in [rad*m] (Example: 2.5e-06 rad m)
				emitx: np.array with the normalized emittance in the vertical plane in [rad*m] (Example: 2.5e-06 rad m)
				s: Vertical separation in [/sigma] (Example: 0.2 \sigma)
				savefile: Boolean that determines if the lumi results will be stored in a tabulated text file
				outputFilePattern: Part of the filename to be stored. The routine will fill the intensity value and the suffix.
		'''
		if len(Npart) > 1:
			debug("Running for multiple intensities... [%s]" % Npart)
			if len(emitnx) != len(emitny):
				critical("# runMuz_XSI: Different size input for emittances!")
				raise ValueError("Different size input for emittances")
			elif len(emitnx) > 1:
				if len(emitnx) != len(Npart):
					critical("# runMuz_XSI: Mismatch in the length of intensities and emittances")
					raise ValueError("Mismatch in the length of intensities and emittances")
				else:
					warn("# runMuz_XSI: Hopefully you have ordered your intensities and emittances properly, my dear user...")
					for Np, ex, ey in zip(Npart, emitnx, emitny):
						info("Running Line Pileup Density XSI for I=%s, enx=%s, eny=%s and s=[%s:%s], x=[%s:%s]" % (Npart, emitnx, emitny, np.min(s), np.max(s), np.min(x), np.max(x)))
						if savefile:
							mfilename = outputFilePattern+str(Np/(1.0e11))+".txt"
							self.runMuz_XS(s,x, Np, ex, ey, b=b, outputFileName=mfilename)
						else:
							self.runMuz_XS(s,x, Np, ex, ey, b=b, outputFileName=None)


	# - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - -
	def runLumz_XB(self, b,x, Npart, emitnx, emitny, s=0.0, outputFileName=None):
		'''
		Calculates the line pileup density for z=0 in units of [evt/mm] vs z [m] for a scan on beta* and crossing for a GIVEN intensity
		Input : b: np.array with the beta* values to scan in [m]  (Example: 0.20 m)
				x: np.array with the half-crossing values to scan in [urad] (Example: 120.0 urad)
				Npart: Bunch intensity [particles] (Example: 2.2e11 particles)
				emitx: Normalized emittance in the horizontal plane in [rad*m] (Example: 2.5e-06 rad m)
				emitx: Normalized emittance in the vertical plane in [rad*m] (Example: 2.5e-06 rad m)
				s: Vertical separation in [/sigma] (Example: 0.2 \sigma)
				outputFileName: Filename to store the return value as tabulated data

		Output: Returns an numpy array filled with three item tuples in the form of (beta* [cm], crossing [um], luminous region [cm])
		'''

		# Checks if input matches the object parameters, if not change it
		if Npart != self.Npart0:
			self.setNpart0(Npart)
		if emitnx is None:
			emitnx = self.getEmitnX0()
		if (emitnx is not None) and (emitnx != self.getEmitnX0()):
			self.setEmitnX0(emitnx)
		if emitny is None:
			emitny = self.getEmitnY0()
		if (emitny is not None) and (emitny != self.getEmitnY0()):
			self.setEmitnY0(emitny)

		debug("Running XB input values = I=%s, enx=%s,eny=%s" % (Npart, emitnx, emitny))
		info("Running Luminous Region Calculation for I=%s, enx=%s,eny=%s | b*=[%s:%s], x=[%s:%s]" % (self.getNpart0(), self.getEmitnX0(), self.getEmitnY0(), np.min(b), np.max(b), np.min(x), np.max(x)))

		pz = []
		for mb in b:
			for mx in x:
				mpz = self.myLumz(mb, mx, s)
				pz.append((mb*100., mx, mpz))
				debug("(%s\t%s\t%s)"% (mb*100., mx, mpz))

		if outputFileName is not None:
			np.savetxt(outputFileName, pz, '%i\t%i\t%.6f')
		return np.array(pz)


	# - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - -
	def runLumz_XBI(self, b, x, Npart, emitnx, emitny, s=0.0, savefile=False, outputFilePattern="lumz_XBI_I"):
		'''
		Drive routine for the XBI (crossing, beta*, intensity) scans.
		Input:	b: np.array with the beta* values to scan in [m]  (Example: 0.20 m)
				x: np.array with the half-crossing values to scan in [urad] (Example: 120.0 urad)
				Npart: np.array with the bunch intensities to scan [particles] (Example: 2.2e11 particles)
				emitx: np.array with the normalized emittance in the horizontal plane in [rad*m] (Example: 2.5e-06 rad m)
				emitx: np.array with the normalized emittance in the vertical plane in [rad*m] (Example: 2.5e-06 rad m)
				s: Vertical separation in [/sigma] (Example: 0.2 \sigma)
				savefile: Boolean that determines if the lumi results will be stored in a tabulated text file
				outputFilePattern: Part of the filename to be stored. The routine will fill the intensity value and the suffix.
		'''
		if len(Npart) > 1:
			debug("Running for multiple intensities... [%s]" % Npart)
			if len(emitnx) != len(emitny):
				critical("# runMuz_XBI: Different size input for emittances!")
				raise ValueError("Different size input for emittances")
			elif len(emitnx) > 1:
				if len(emitnx) != len(Npart):
					critical("# runMuz_XBI: Mismatch in the length of intensities and emittances")
					raise ValueError("Mismatch in the length of intensities and emittances")
				else:
					warn("# runMuz_XBI: Hopefully you have ordered your intensities and emittances properly, my dear user...")
					for Np, ex, ey in zip(Npart, emitnx, emitny):
						info("Running Line Pileup Density XBI for I=%s, enx=%s, eny=%s and b=[%s:%s], x=[%s:%s]" % (Npart, emitnx, emitny, np.min(b), np.max(b), np.min(x), np.max(x)))
						if savefile:
							mfilename = outputFilePattern+str(Np/(1.0e11))+".txt"
							self.runLumz_XB(b,x, Np, ex, ey, s=s, outputFileName=mfilename)
						else:
							self.runLumz_XB(b,x, Np, ex, ey, s=s, outputFileName=None)


	# - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - -
	def runLumz_XS(self, s,x, Npart, emitnx, emitny, b=0.20, outputFileName=None):
		'''
		Calculates the line pileup density for z=0 in units of [evt/mm] vs z [m] for a scan on beta* and crossing for a GIVEN intensity
		Input : b: np.array with the beta* values to scan in [m]  (Example: 0.20 m)
				x: np.array with the half-crossing values to scan in [urad] (Example: 120.0 urad)
				Npart: Bunch intensity [particles] (Example: 2.2e11 particles)
				emitx: Normalized emittance in the horizontal plane in [rad*m] (Example: 2.5e-06 rad m)
				emitx: Normalized emittance in the vertical plane in [rad*m] (Example: 2.5e-06 rad m)
				s: Vertical separation in [/sigma] (Example: 0.2 \sigma)
				outputFileName: Filename to store the return value as tabulated data

		Output: Returns an numpy array filled with three item tuples in the form of (beta* [cm], crossing [um], line pileup [evt/mm])
		'''

		# Checks if input matches the object parameters, if not change it
		if Npart != self.Npart0:
			self.setNpart0(Npart)
		if emitnx is None:
			emitnx = self.getEmitnX0()
		if (emitnx is not None) and (emitnx != self.getEmitnX0()):
			self.setEmitnX0(emitnx)
		if emitny is None:
			emitny = self.getEmitnY0()
		if (emitny is not None) and (emitny != self.getEmitnY0()):
			self.setEmitnY0(emitny)

		debug("Running XB input values = I=%s, enx=%s,eny=%s" % (Npart, emitnx, emitny))
		info("Running Line Pileup Density Calculation for I=%s, enx=%s,eny=%s | s=[%s:%s], x=[%s:%s]" % (self.getNpart0(), self.getEmitnX0(), self.getEmitnY0(), np.min(s), np.max(s), np.min(x), np.max(x)))

		pz = []
		for ms in s:
			for mx in x:
				mpz = self.myLumz(b, mx, ms)
				pz.append((ms, mx, mpz))
				debug("(%s\t%s\t%s)"% (ms, mx, mpz))

		if (outputFileName is not None):
			np.savetxt(outputFileName, pz, '%.3f\t%i\t%.6f')
		return np.array(pz)


	# - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - -
	def runLumz_XSI(self, s, x, Npart, emitnx, emitny, b=0.20, savefile=False, outputFilePattern="lumz_XSI_I"):
		'''
		Drive routine for the XBI (crossing, beta*, intensity) scans.
		Input:	b: np.array with the beta* values to scan in [m]  (Example: 0.20 m)
				x: np.array with the half-crossing values to scan in [urad] (Example: 120.0 urad)
				Npart: np.array with the bunch intensities to scan [particles] (Example: 2.2e11 particles)
				emitx: np.array with the normalized emittance in the horizontal plane in [rad*m] (Example: 2.5e-06 rad m)
				emitx: np.array with the normalized emittance in the vertical plane in [rad*m] (Example: 2.5e-06 rad m)
				s: Vertical separation in [/sigma] (Example: 0.2 \sigma)
				savefile: Boolean that determines if the lumi results will be stored in a tabulated text file
				outputFilePattern: Part of the filename to be stored. The routine will fill the intensity value and the suffix.
		'''
		if len(Npart) > 1:
			debug("Running for multiple intensities... [%s]" % Npart)
			if len(emitnx) != len(emitny):
				critical("# runLumz_XSI: Different size input for emittances!")
				raise ValueError("Different size input for emittances")
			elif len(emitnx) > 1:
				if len(emitnx) != len(Npart):
					critical("# runLumz_XSI: Mismatch in the length of intensities and emittances")
					raise ValueError("Mismatch in the length of intensities and emittances")
				else:
					warn("# runLumz_XSI: Hopefully you have ordered your intensities and emittances properly, my dear user...")
					for Np, ex, ey in zip(Npart, emitnx, emitny):
						info("Running Luminous region XSI for I=%s, enx=%s, eny=%s and s=[%s:%s], x=[%s:%s]" % (Npart, emitnx, emitny, np.min(s), np.max(s), np.min(x), np.max(x)))
						if savefile:
							mfilename = outputFilePattern+str(Np/(1.0e11))+".txt"
							self.runLumz_XS(s,x, Np, ex, ey, b=b, outputFileName=mfilename)
						else:
							self.runLumz_XS(s,x, Np, ex, ey, b=b, outputFileName=None)


	# - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - -
	def runXBI(self, b, x, Npart, emitnx, emitny, s=0.0, savefile=False):
		'''
		Drive routine to produce all the txt files for the XBI scan
		'''
		info("Running BeamCal for XBI : b*=[%s:%s], x=[%s:%s]"%(np.min(b), np.max(b), np.min(x), np.max(x)))
		# self.runLumi_XBI(b, x, Npart, emitnx, emitny, s=s, savefile=savefile)
		self.runMuz_XBI(b, x, Npart, emitnx, emitny, s=s, savefile=savefile)
		self.runLumz_XBI(b, x, Npart, emitnx, emitny, s=s, savefile=savefile)


	# - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - -
	def runXSI(self, s, x, Npart, emitnx, emitny, b=0.20, savefile=False):
		'''
		Drive routine to produce all the txt files for the XSI scan
		'''
		info("Running BeamCal for XSI : b*=[%s:%s], x=[%s:%s]"%(np.min(b), np.max(b), np.min(x), np.max(x)))
		self.runLumi_XSI(s,x,Npart, emitnx, emitny, b=b, savefile=savefile)
		self.runMuz_XSI(s,x,Npart, emitnx, emitny, b=b, savefile=savefile)
		self.runLumz_XSI(s,x,Npart, emitnx, emitny, b=b, savefile=savefile)


	# - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - -
	def printConfig(self):
		print '''
####################################################################################################
#
#	OPTIONS
#
####################################################################################################
beamProfile 			= %s 	# Longutudinal bunch distributions as a function of z [m]
plotSample 			= %s 	# Plot sample distributions
logfile 			= %s 		# Logfile name
loglevel 			= %s 		# Loglevel - Write only output of level higher than
						# 0: Not Set, 10: DEBUG, 20: INFO, 30: WARNING, 40: ERROR, 50: CRITICAL

####################################################################################################
#
#	CONSTANT AND DEFAULT PARAMETERS
#
####################################################################################################

Clight 				= %s  	# speed of light [m/s]
Qe 				= %s  # electron charge [C]
sigprotoninelas 		= %s  	# inelastic hadron cross section [barn]
sigtotproton 			= %s   	# inelastic hadron cross section [barn]
Mproton 			= %s  	# proton mass [GeV]

####################################################################################################
#
#	CURRENT SETUP PARAMETERS : NOMINAL SCENARIO AT 5e34
#				  SNAPSHOT AT THE BEGGINING AND END OF THE COAST
#
####################################################################################################
Nb0 				= %s	# number of collision at IP1 and IP5
Npart0 				= %s 	# bunch charge at begining of coast
Nrj0 				= %s 	# collision energy [GeV]
gamma0 				= %s	# relativisitc factor
emitX0  			= %s # r.m.s. horizontal physical emittance in collision
emitY0  			= %s # r.m.s. vertical physical emittance in collision
circum 				= %s 	# ring circumference [m]
sigz0				= %s 	# default r.m.s. bunch length [m]
frev0 				= %s	# LHC revolution frequency at flat top
hrf400 				= %s 	# LHC harmonic number for 400 Mhz
omegaCC0 			= %s 	# default omega/c for 400 MHz crab-cavities
VRF0 				= %s 		# reference CC voltage for full crabbing at 590 murad crossing angle
VRFx0 				= %s 		# CC voltage [MV] in crossing plane for 2 CCs
VRFy0 				= %s 		# default CC voltage [MV] in parallel plane
Llevel0 			= %s 		# Default Level luminosity [10**34]
alpha0 				= %s 	# Default full crossing angle

		'''%(self.beamProfile, self.plotSample, self.logfile, self.loglevel, self.Clight,self.Qe, self.sigprotoninelas, self.sigtotproton, self.Mproton, self.Nb0, self.Npart0, self.Nrj0, self.gamma0, self.emitX0, self.emitY0,self.circum, self.sigz0,self.frev0,self.hrf400,self.omegaCC0,self.VRF0,self.VRFx0,self.VRFy0,self.Llevel0,self.alpha0)

#####################################################################################################################################################
#
#									M O D U L E   F U N C T I O N S   O U T S I D E   C L A S S
#
#####################################################################################################################################################
# - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - -
def createRange(start, stop, step):
	'''
	User friendly function to make step-incremented array within the start/stop limits
	'''
	return np.arange(start, stop+(step/2.0), step)


# - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - - * - -
def help():
		print '''
module : beamCal - Numerical Calculation of machine performance standards based on beam parameters
Author : Nikos Karastathis (nkarast <at> cern <dot> ch)
Version: 0.2
--------------------------------------------------------
This is a collection of functions that numerically calculate the performance standards (luminosity, pileup, levelling time, beam lifetime, etc)
of an accelerator machine (here defaults to HL-LHC), based on beam and machine parameters.

Prerequisites: Scipy Stack i.e. NumPy, SciPy [optionally SymPy, Matplotlib]

Available functions:
--------------------

Module Functions:
		- createRange
		- help

Class: BeamCal
		- setLogFile
		- setLogLevel
		- setBeamProfile
		- setPlotOption
		- setNb0
		- setNpart0
		- setNrj0
		- setEmitnX0
		- setEmitX0
		- setEmitnY0
		- setEmitY0
		- setCircum
		- setFrev0
		- setSig0
		- setHrf400
		- setOmegaCC0
		- setVRF0
		- setVRFx0
		- setVRFy0
		- setLlevel0
		- setAlpha0
		- rho
		- plotProfiles
		- kernel
		- density
		- Rloss
		- mu2D
		- muz
		- mut
		- siglumz
		- siglumt
		- Life
		- TLev
		- Lumi
		- mutot
		- myLumi
		- myMutot
		- myMuz
		- myLumz
		- runLumi_XB
		- runLimi_XBI
		- runLumi_XS
		- runLimi_XSI
		- runMuz_XB
		- runMuz_XBI
		- runMuz_XS
		- runMuz_XSI
		- runLumz_XB
		- runLumz_XBI
		- runLumz_XS
		- runLumz_XSI
		- runXBI
		- runXSI
		- printConfig




		'''



#####################################################################################################################################################
#####################################################################################################################################################
#####################################################################################################################################################

if __name__ == '__main__':

	### Example :
    x = BeamCal()
    
    myB = np.array([0.15])
    myB_2 = createRange(0.20, 1., 0.10)
    myB = np.append(myB, myB_2).ravel()
    print 'B: ', myB
    myX = createRange(120., 345., 15.)
    print 'X: ', myX

    mNpart	= np.array([1.3e11])
    memitnx = np.array([2.5e-6])
    memitny = np.array([2.5e-6])
    x.runLumi_XB(myB,myX, 1.6e11, 2.5e-06, 2.5e-06, s=0.0, outputFileName='lumi_XBI_I1.6.txt')