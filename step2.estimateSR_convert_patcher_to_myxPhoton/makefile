# Compiler and flags
CXX = $(shell root-config --ld)
ROOT_FLAGS = $(shell root-config --cflags --libs)
LD_FLAGS = $(shell root-config --ldflags)
EXTRA_LIBS = -lTMVA
MYLIB = -I./extlib/ -L./extlib/ -lcorrectionlib

# Targets and source files
TARGET_New = exe.EstimateSR
SOURCE_New = EstimateSR.C

TARGET_Orig = exe.origEstimateSR
SOURCE_Orig = origEstimateSR.C

# Build and run targets
.PHONY: all run clean

all: $(TARGET_New)

$(TARGET_New): $(SOURCE_New)
	@echo "[Compiling] $(SOURCE_New)"
	$(CXX) $(LD_FLAGS) $(ROOT_FLAGS) $(EXTRA_LIBS) $(SOURCE_New) $(MYLIB) -o $(TARGET_New)
	@echo "[usage] ./$(TARGET_New) in.root out.root 2022EE"

$(TARGET_Orig): $(SOURCE_Orig)
	@echo "[Compiling] $(SOURCE_Orig)"
	$(CXX) $(LD_FLAGS) $(ROOT_FLAGS) $(EXTRA_LIBS) $(SOURCE_Orig) $(MYLIB) -o $(TARGET_Orig)
	@echo "[usage] ./$(TARGET_Orig) in.root out.root 2022EE"
hi: HI.C
	$(CXX) $(LD_FLAGS) $(ROOT_FLAGS) $(EXTRA_LIBS) HI.C $(MYLIB) -o a.exe


massiverun: runData runGJets runQCD runGJetsPythiaFlat ## Data and gjet
#massiverun: runData runGJets runQCD

runData: runDataE runDataF runDataG runDataESB runDataFSB runDataGSB ## 6 channel
runDataE: $(TARGET_New) 
	./$(TARGET_New) DataE            > log_DataE 2>&1
runDataF: $(TARGET_New) 
	./$(TARGET_New) DataF            > log_DataF 2>&1
runDataG: $(TARGET_New) 
	./$(TARGET_New) DataG            > log_DataG 2>&1
runDataESB: $(TARGET_New) 
	./$(TARGET_New) DataEsideband    > log_DataEsideband 2>&1
runDataFSB: $(TARGET_New) 
	./$(TARGET_New) DataFsideband    > log_DataFsideband 2>&1
runDataGSB: $(TARGET_New) 
	./$(TARGET_New) DataGsideband    > log_DataGsideband 2>&1



runGJets: runGJets40 runGJets70 runGJets100 runGJets200 runGJets400 runGJets600 ## 6 channel
runGJets40: $(TARGET_New)
	./$(TARGET_New) GJets40  > log_GJets40  2>&1
runGJets70: $(TARGET_New)
	./$(TARGET_New) GJets70  > log_GJets70  2>&1
runGJets100: $(TARGET_New)
	./$(TARGET_New) GJets100 > log_GJets100 2>&1
runGJets200: $(TARGET_New)
	./$(TARGET_New) GJets200 > log_GJets200 2>&1
runGJets400: $(TARGET_New)
	./$(TARGET_New) GJets400 > log_GJets400 2>&1
runGJets600: $(TARGET_New)
	./$(TARGET_New) GJets600 > log_GJets600 2>&1

runGJetsPythiaFlat: $(TARGET_New)
	./$(TARGET_New) GJetsPythiaFlat > log_GJetsPythiaFlat 2>&1


runQCD: runQCD70 runQCD100 runQCD200 runQCD400 runQCD600 runQCD800 runQCD1000 runQCD1200 runQCD1500 runQCD2000 ## 10 channel
runQCD70: $(TARGET_New)
	./$(TARGET_New) QCD70    > log_QCD70  2>&1
runQCD100: $(TARGET_New)
	./$(TARGET_New) QCD100   > log_QCD100 2>&1
runQCD200: $(TARGET_New)
	./$(TARGET_New) QCD200   > log_QCD200 2>&1
runQCD400: $(TARGET_New)
	./$(TARGET_New) QCD400   > log_QCD400 2>&1
runQCD600: $(TARGET_New)
	./$(TARGET_New) QCD600   > log_QCD600 2>&1
runQCD800: $(TARGET_New)
	./$(TARGET_New) QCD800   > log_QCD800 2>&1
runQCD1000: $(TARGET_New)
	./$(TARGET_New) QCD1000  > log_QCD1000 2>&1
runQCD1200: $(TARGET_New)
	./$(TARGET_New) QCD1200  > log_QCD1200 2>&1
runQCD1500: $(TARGET_New)
	./$(TARGET_New) QCD1500  > log_QCD1500 2>&1
runQCD2000: $(TARGET_New)
	./$(TARGET_New) QCD2000  > log_QCD2000 2>&1
	
test: $(TARGET_New)
	./$(TARGET_New) test1; echo gjet mdagraph tested
	./$(TARGET_New) test2; echo QCD madgraph tested
	#./$(TARGET_New) test3
	##@echo "[QCD test sample]"
	#./$(TARGET_New) test1
	##@echo "[sig test sample]"
	#./$(TARGET_New) test2
	##@echo "[data test sample]"
	#./$(TARGET_New) test3
run: $(TARGET_New)
	@echo "[DirectRun]"
	time ./$(TARGET_New) $(runtype) | tee log_$(runtype)
	echo "[DirectRun] Finished"
	


clean: ## clean up log files and output files
	rm -f $(TARGET_New) $(TARGET_Orig) out_*.root log_* outfile_* aabark 

timeSTAMP=$$(date "+%Y%m%d_%H%M")
oDIR=/afs/cern.ch/user/l/ltsai/eos_storage/condor_summary/2022EE_GJet/
mergemassiverun: mergeGJetMadgraph mergeGJetMadgraphAll mergeQCD mergeQCDall mergedatasideband mergedatasignalregion mergeGJetPythiaFlat ## merge all output files from stage2 to new folder [oDIR=/afs/cern.ch/user/l/ltsai/eos_storage/condor_summary/2022EE_GJet/]
	collect_dir=stage2_$(timeSTAMP); mkdir $$collect_dir; mv stage2*.root $$collect_dir; mv $$collect_dir $(oDIR)/; echo "[OutputFolder] $(oDIR)/$$collect_dir"
mergeGJetPythiaFlat:
	cp outfile_GJetPythiaFlat.root stage2_GJetMCGJeyPythiaFlat.root
mergeGJetMadgraph:
	hadd stage2_GJetMCGJetMadgraph.root     \
		outfile_GmJets_200To400.root \
		outfile_GmJets_400To600.root \
		outfile_GmJets_600_inf.root
mergeGJetMadgraphAll:
	hadd stage2_GJetMCGJetMadgraph.all.root \
		outfile_GmJets_100To200.root \
		outfile_GmJets_200To400.root \
		outfile_GmJets_400To600.root \
		outfile_GmJets_40To70.root \
		outfile_GmJets_600_inf.root \
		outfile_GmJets_70To100.root
mergeQCD:
	hadd stage2_QCDMadgraph.root \
		outfile_QCD_400To600.root \
		outfile_QCD_600To800.root \
		outfile_QCD_800To1000.root \
		outfile_QCD_1000To1200.root \
		outfile_QCD_1200To1500.root \
		outfile_QCD_1500To2000.root \
		outfile_QCD_2000.root
mergeQCDall:
	hadd stage2_QCDMadgraph.all.root \
		outfile_QCD_70To100.root \
		outfile_QCD_100To200.root \
		outfile_QCD_200To400.root \
		outfile_QCD_400To600.root \
		outfile_QCD_600To800.root \
		outfile_QCD_800To1000.root \
		outfile_QCD_1000To1200.root \
		outfile_QCD_1200To1500.root \
		outfile_QCD_1500To2000.root \
		outfile_QCD_2000.root
mergedatasideband:
	hadd stage2_GJetDataSignalRegion.root \
		outfile_dataE_signalregion.root \
		outfile_dataF_signalregion.root \
		outfile_dataG_signalregion.root
mergedatasignalregion:
	hadd stage2_GJetDataDataSideband.root \
		outfile_dataE_sideband.root \
		outfile_dataF_sideband.root \
		outfile_dataG_sideband.root

	
##  Usage:
##  	make all
##  	make test # run test sample
##  	make massiverun
##    make run runtype=QCD70

##@ Utility
IN_ARGS = 
help:  ## Display this help
	@awk 'BEGIN {FS = ":.*##"; printf "Usage: make \033[32m<command>\033[0m $(IN_ARGS)\n\nCommands:\n\033[36m\033[0m\n"} /^[a-zA-Z0-9_-]+:.*?##/ { printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2 } /^##@/ { printf "\n\033[1m%s\033[0m\n", substr($$0, 5) } ' $(MAKEFILE_LIST)
