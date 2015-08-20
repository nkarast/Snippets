evgenConfig.description = "MG5 gg H->WW->lvlv, CP Mixing DF decay"
evgenConfig.keywords = ["Higgs","WW", "CPMixing", "emu/mue"]
evgenConfig.inputfilecheck = 'Spin0CPMixed'

#include ( "MC12JobOptions/Pythia_AUET2B_CTEQ6L1_Common.py" )
include("MC12JobOptions/Pythia_Perugia2011C_Common.py")
evgenConfig.generators += [ "MadGraph" ]
## ... Tauola
include ( "MC12JobOptions/Pythia_Tauola.py" )
## ... Photos
include ( "MC12JobOptions/Pythia_Photos.py" )

topAlg.Pythia.PythiaCommand += [ "pyinit user madgraph",
                                "pyinit pylisti -1","pyinit pylistf 1","pyinit dumpr 1 2",
                                "pyinit user lhef",
                                ]

