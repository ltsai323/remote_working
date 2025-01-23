#!/usr/bin/env sh
function the_exit() { echo $1; exit 1; }

#`root-config --ld` `root-config --cflags --libs` -lXMLIO -lTMVA ForTrigSF_MC.C -o a.out && echo '[usage] ./a.exe in.root out.root 2022EE'
#`root-config --ld` `root-config --cflags --libs` -lXMLIO -lTMVA ForTrigSF_DYZjet.C -o dyzmumu.exe && echo '[usage] ./dyzmumu.exe in.root out.root 2022EE'
#`root-config --ld` `root-config --cflags --libs` -lXMLIO -lTMVA DYZllJet.C -o z.out && echo '[usage] ./z.exe in.root out.root 2022EE'
# XMLIO deals with error from ld at arm64
#`root-config --ld` `root-config --cflags --libs` -lXMLIO -lTMVA -I./extlib/ -lcorrectionlib -L./extlib/ PatchToxPhoton.C -o b.exe && echo '[usage] ./b.exe in.root out.root'

#`root-config --ld` `root-config --cflags --libs` -lTMVA -I./extlib/ -lcorrectionlib -L./extlib/ EstimateSR.C   -o c.exe




`root-config --ld` `root-config --cflags --libs` -lXMLIO -lTMVA ForTrigSF_DYZjet.C -o main_job.exe && echo '[usage] ./main_job.exe in.root out.root'
