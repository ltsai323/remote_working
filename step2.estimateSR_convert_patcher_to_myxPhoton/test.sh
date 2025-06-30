#!/usr/bin/env sh
refFOLDER=../testref/
newFOLDER=./



function the_exit() { echo $1; exit 1; }

function checkEVT() {
  rootFILE=$1
  logFILE=$2
root $rootFILE > $logFILE <<EOF
std::cout << "entries : " << tree->GetEntries() << std::endl;
std::cout << "Entry 1" <<std::endl;
tree->Show(1)
std::cout << "Entry 3" <<std::endl;
tree->Show(3)
std::cout << "Entry 30" <<std::endl;
tree->Show(30)
std::cout << "Entry 300" <<std::endl;
tree->Show(300)
EOF
}
function compare_file() {
  fileNAME=$1
  echo -e "\n\n\n[CompareFile] on file '$fileNAME'"
  
  newfile=$newFOLDER/$fileNAME
  reffile=$refFOLDER/$fileNAME
  if [ ! -f "$newfile" ]; then the_exit "[FileNotFound] new file '$newfile' does not exist"; fi
  if [ ! -f "$reffile" ]; then the_exit "[FileNotFound] ref file '$reffile' does not exist"; fi

  checkEVT $newfile log_new_$fileNAME
  checkEVT $reffile log_ref_$fileNAME
  echo -e "\n[COMP] diff log_new_$fileNAME log_ref_$fileNAME"
  diff log_new_$fileNAME log_ref_$fileNAME
}


fDATA=mytesting_data.root
fFAKE=mytesting_qcdmadgraph.root
fSIGN=mytesting_gjetmadgraph.root
compare_file $fDATA
compare_file $fFAKE
compare_file $fSIGN
