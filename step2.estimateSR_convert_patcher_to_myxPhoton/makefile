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

all: $(TARGET_New) $(TARGET_Orig)

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


massiverun: $(TARGET_New)
	./$(TARGET_New) DataE            > log_DataE 2>&1 & \
	./$(TARGET_New) DataF            > log_DataF 2>&1 & \
	./$(TARGET_New) DataG            > log_DataG 2>&1 & \
	./$(TARGET_New) DataEsideband    > log_DataEsideband 2>&1 & \
	./$(TARGET_New) DataFsideband    > log_DataFsideband 2>&1 & \
	./$(TARGET_New) DataGsideband    > log_DataGsideband 2>&1 & \
	./$(TARGET_New) GJets40  > log_GJets40  2>&1 & \
	./$(TARGET_New) GJets70  > log_GJets70  2>&1 & \
	./$(TARGET_New) GJets100 > log_GJets100 2>&1 & \
	./$(TARGET_New) GJets200 > log_GJets200 2>&1 & \
	./$(TARGET_New) GJets400 > log_GJets400 2>&1 & \
	./$(TARGET_New) GJets600 > log_GJets600 2>&1 & \
	./$(TARGET_New) QCD70    > log_QCD70  2>&1 & \
	./$(TARGET_New) QCD100   > log_QCD100 2>&1 & \
	./$(TARGET_New) QCD200   > log_QCD200 2>&1 & \
	./$(TARGET_New) QCD400   > log_QCD400 2>&1 & \
	./$(TARGET_New) QCD600   > log_QCD600 2>&1 & \
	./$(TARGET_New) QCD800   > log_QCD800 2>&1 & \
	./$(TARGET_New) QCD1000  > log_QCD1000 2>&1 & \
	./$(TARGET_New) QCD1200  > log_QCD1200 2>&1 & \
	./$(TARGET_New) QCD1500  > log_QCD1500 2>&1 & \
	./$(TARGET_New) QCD2000  > log_QCD2000 2>&1 & \
	wait
	
test: $(TARGET_New)
	@echo "[QCD test sample]"
	./$(TARGET_New) test1
	@echo "[sig test sample]"
	./$(TARGET_New) test2
	@echo "[data test sample]"
	./$(TARGET_New) test3
run: $(TARGET_New)
	@echo "[DirectRun]"
	time ./$(TARGET_New) $(runtype) | tee log_$(runtype)
	echo "[DirectRun] Finished"
	


clean:
	rm -f $(TARGET_New) $(TARGET_Orig) out_*.root log_*


##  Usage:
##  	make all
##  	make test # run test sample
##  	make massiverun
##    make run runtype=QCD70
