# Compiler and flags
CXX = g++
ROOT_FLAGS = $(shell root-config --cflags --libs)
LD_FLAGS = $(shell root-config --ld)
EXTRA_LIBS = -lXMLIO -lTMVA

# Targets and source files
TARGET_A = a.exe
SOURCE_A = ForTrigSF_MC.C

TARGET_Z = z.exe
SOURCE_Z = DYZllJet.C

# Build and run targets
.PHONY: all run clean

all: $(TARGET_A) $(TARGET_Z)

$(TARGET_A): $(SOURCE_A)
	@echo "[Compiling] $(SOURCE_A)"
	$(CXX) $(LD_FLAGS) $(ROOT_FLAGS) $(EXTRA_LIBS) $(SOURCE_A) -o $(TARGET_A)
	@echo "[usage] ./$(TARGET_A) in.root out.root 2022EE"

$(TARGET_Z): $(SOURCE_Z)
	@echo "[Compiling] $(SOURCE_Z)"
	$(CXX) $(LD_FLAGS) $(ROOT_FLAGS) $(EXTRA_LIBS) $(SOURCE_Z) -o $(TARGET_Z)
	@echo "[usage] ./$(TARGET_Z) in.root out.root 2022EE"

massiverun: $(TARGET_A)
	@if [ -z "$(filelist)" ]; then \
		echo "Error: Set 'filelist' variable to provide the input file list."; \
		exit 1; \
	fi

	@idx=0; \
	for infilename in `cat $(filelist)`; do \
	  oFILE=out_$${idx}.root; \
	  echo "./$(TARGET_A) $$infilename $$oFILE 2022EE"; \
	  ./$(TARGET_A) $$infilename $$oFILE 2022EE > log_$${idx} 2>&1; \
	  sh bkgjob_submitN.sh 5; \
	  idx=$$((idx+1)); \
	done; \
	echo "[AllJobSubmitted]"; \
	wait; \
	echo "[AllJobFinished]"

### usage : make run iFILE=hi.root oFILE=jj.root
run:  $(TARGET_A) 
	./$(TARGET_A) $(iFILE) $(oFILE) 2022EE
clean:
	rm -f $(TARGET_A) $(TARGET_Z) out_*.root log_*
