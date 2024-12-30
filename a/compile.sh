if [ "$1" == "test" ]; then
  echo 'test compilation'
  #g++ `root-config --cflags --libs` -lTMVA -I./extlib/ -lcorrectionlib -L./extlib/ EstimateSR.C -o ttt.out && echo ./ttt.out TAG
  g++ `root-config --cflags --libs` -lTMVA -I./extlib/ -lcorrectionlib -L./extlib/ origEstimateSR.C -o ttt.out && echo ./ttt.out TAG
  exit
fi
echo 'normal compilation'
g++ `root-config --cflags --libs` -lTMVA -I./extlib/ -lcorrectionlib -L./extlib/ EstimateSR.C -o a.out && echo ./a.out TAG
#g++ `root-config --cflags --libs` -lTMVA -I./extlib/ -lcorrectionlib -L./extlib/ eee.C -o ttt.out && echo ./ttt.out TAG
