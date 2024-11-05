#!/usr/bin/env sh
#`root-config --ld` `root-config --cflags --libs` -lXMLIO -lTMVA ForTrigSF_MC.C -o a.exe && echo '[usage] ./a.exe in.root out.root isMC[1/0]'
# XMLIO deals with error from ld at arm64
#`root-config --ld` `root-config --cflags --libs` -lXMLIO -lTMVA -I./extlib/ -lcorrectionlib -L./extlib/ PatchToxPhoton.C -o b.exe && echo '[usage] ./b.exe in.root out.root'

`root-config --ld` `root-config --cflags --libs` -lTMVA -I./extlib/ -lcorrectionlib -L./extlib/ EstimateSR.C   -o c.exe
