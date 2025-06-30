OUTPUT_DIR=/afs/cern.ch/user/l/ltsai/eos_storage/condor_storage/$(jobname)

.PHONY: help ## print help by default


check_defined = \
    $(strip $(foreach 1,$1, \
    $(call __check_defined,$1,$(strip $(value 2)))))
__check_defined = \
    $(if $(value $1),, \
    $(error Undefined $1$(if $2, ($2))))

check_shell_var_defined = \
  	$(if $(shell [ -z "$${$1}" ] && echo undefined), \
	$(error Shell variable $1 is undefined), \
	$(info Shell variable $1 is set))

makehisto: ## make histo [jEtaBin=0 or 1][jPtL=30][jPtR=100]
	$(call check_defined, jEtaBin)
	$(call check_defined, jPtL)
	$(call check_defined, jPtR)
	python3 makehisto_Run2022_workingpoint.py $(jEtaBin) $(jPtL) $(jPtR)

#tag = 2022EE
#searchDAS:
#	$(call check_defined, dataset)
#	$(call check_shell_var_defined,X509_USER_PROXY)
#	sh prepare_remoteFileList.sh $(tag) $(dataset)
#submit: | $(OUTPUT_DIR)
#	$(call check_defined, jobname)
#	$(call check_defined, filelist)
#	$(call check_shell_var_defined,X509_USER_PROXY)
#	@echo -e "\n\n[OutputFolder] $(OUTPUT_DIR)"
#	condor_submit submitted_condorjob2.sub -batch-name $(jobname) -a "jobName=$(jobname)" -a "remoteFileList=$(filelist)" -a "output_folder=$(OUTPUT_DIR)"
#
#searchDASfromFile:
#	$(call check_defined, datasetSummary)
#	$(call check_shell_var_defined,X509_USER_PROXY)
#	while read -r tag dataset; do make searchDAS tag="$$tag" dataset="$$dataset"; done < $(datasetSummary)
#submitfromFile: | $(OUTPUT_DIR) 
#	$(call check_defined, datasetSummary)
#	$(call check_shell_var_defined,X509_USER_PROXY)
#	@echo -e "[OutputFolder] $(OUTPUT_DIR)"
#	while read -r jobname dataset; do make searchDAS tag="$$jobname" dataset="$$dataset"; make submit jobname="$$jobname" filelist="remoteFileList_$${jobname}.txt"; done < $(datasetSummary)
#
#checkOutput: 
#	sh check_job_output.sh $(DIR)
#checkOutputfromfile: 
#	while read -r jobname dataset; do echo -e "\n\n[FileList] remoteFileList_$${jobname}.txt ( `wc --lines <remoteFileList_$${jobname}.txt` )"; make checkOutput DIR=$(OUTPUT_DIR)/$$jobname ; done < $(datasetSummary)
#
#checkErrorLog: 
#	$(call check_defined, jobtag)
#	@du -sh condor_logs/job_$(jobtag)*.error | grep K || echo all job accomplished!
#	
#collectErrorFiles: 
#	$(call check_defined, jobtag)
#	$(call check_defined, remoteFileList)
#
#	touch failedjob_$(jobtag).txt; /bin/rm failedjob_$(jobtag).txt
#	make checkErrorLog jobtag=$(jobtag) | grep error > l || { echo "all $(jobtag) job accomplished!"; exit; }
#	while read -r _size_ filename; do sh get_remoterootpath_from_remoteFileList.sh $(remoteFileList) $$filename >> failedjob_$(jobtag).txt; done < l
#
#	@echo "[outputfile] failedjob_$(jobtag).txt"
#	@/bin/rm l

clean: ## clean logs
	/bin/rm condor_logs/*

$(OUTPUT_DIR):
	$(call check_defined, jobname)
	@echo Folder not found: Initialize folder $(OUTPUT_DIR)
	mkdir -p $@

IN_ARGS = [opts]

help:  ## Display this help
	@awk 'BEGIN {FS = ":.*##"; printf "Usage: make \033[32m<command>\033[0m $(IN_ARGS)\n\nCommands:\n\033[36m\033[0m\n"} /^[0-9a-zA-Z_-]+:.*?##/ { printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2 } /^##@/ { printf "\n\033[1m%s\033[0m\n", substr($$0, 5) } ' $(MAKEFILE_LIST)

.DEFAULT_GOAL := help
