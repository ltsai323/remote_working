#export LD_LIBRARY_PATH=$LD_LIBRARAY_PATH:$PWD/extlib/
function the_exit() { echo $1; exit; }
if [ "$1" == "test" ]; then
  echo 'exec test samples'
  ./ttt.out test1 || the_exit "failed to execute gjet test sample"
  ./ttt.out test2 || the_exit "failed to execute qcd test sample"
  ./ttt.out test3 || the_exit "failed to execute data sample"
  exit
fi
echo 'exec massive product'
./a.out DataE            > log_DataE 2>&1 &
./a.out DataF            > log_DataF 2>&1 &
./a.out DataG            > log_DataG 2>&1 &
./a.out DataEsideband    > log_DataEsideband 2>&1 &
./a.out DataFsideband    > log_DataFsideband 2>&1 &
./a.out DataGsideband    > log_DataGsideband 2>&1 &
./a.out GJets40  > log_GJets40  2>&1 &
./a.out GJets70  > log_GJets70  2>&1 &
./a.out GJets100 > log_GJets100 2>&1 &
./a.out GJets200 > log_GJets200 2>&1 &
./a.out GJets400 > log_GJets400 2>&1 &
./a.out GJets600 > log_GJets600 2>&1 &
./a.out QCD70    > log_QCD70  2>&1 &
./a.out QCD100   > log_QCD100 2>&1 &
./a.out QCD200   > log_QCD200 2>&1 &
./a.out QCD400   > log_QCD400 2>&1 &
./a.out QCD600   > log_QCD600 2>&1 &
./a.out QCD800   > log_QCD800 2>&1 &
./a.out QCD1000  > log_QCD1000 2>&1 &
./a.out QCD1200  > log_QCD1200 2>&1 &
./a.out QCD1500  > log_QCD1500 2>&1 &
./a.out QCD2000  > log_QCD2000 2>&1 &
wait
