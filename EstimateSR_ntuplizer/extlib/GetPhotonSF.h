#include<string>
double GetPhotonSF(double pt, double eta, std::string sys){
  double sf;
  if(eta>=-2.5 && eta<-2.0){sf = 1.07222 -0.000434378*pt;
	if(sys=="up"){sf = sf+ 0.029;}
	if(sys=="down"){sf = sf-0.029;}
  }
  if(eta>=-2.0 && eta<-1.566){sf = 1.01246 + 0.000155481*pt;
	if(sys=="up"){sf = sf+ 0.013;}
        if(sys=="down"){sf = sf-0.013;}
  }
  if(eta>=-1.44 && eta<-0.8){sf = 0.993762 -1.1104e-05*pt;
	if(sys=="up"){sf = sf+ 0.017;}
        if(sys=="down"){sf = sf-0.017;}
  }
  if(eta>=-0.8 && eta<0.0){sf = 0.986143 + 0.000130489*pt;
	if(sys=="up"){sf = sf+ 0.027;}
        if(sys=="down"){sf = sf-0.027;}
  }
  if(eta>=0.0 && eta<0.8){sf = 0.991526 + 7.79625e-05*pt;
	if(sys=="up"){sf = sf+ 0.028;}
        if(sys=="down"){sf = sf-0.028;}
  }
  if(eta>=0.8 && eta<1.44){sf = 0.982112 + 0.0001417*pt;
	if(sys=="up"){sf = sf+ 0.018;}
        if(sys=="down"){sf = sf-0.018;}
  }
  if(eta>=1.566 && eta<2.0){sf = 1.00718 + 5.74764e-05*pt;
	if(sys=="up"){sf = sf+ 0.013;}
        if(sys=="down"){sf = sf-0.013;}
  }
  if(eta>=2.0 && eta<=2.5){sf = 1.04898 + 8.68794e-05*pt;
	if(sys=="up"){sf = sf+ 0.029;}
        if(sys=="down"){sf = sf-0.029;}
  }

  return(sf);
}

double GetTriggerSF(double pt, double eta, std::string sys){
  double sf;
  if(eta>=-2.5 && eta<-2.0){
    if(pt>=210 && pt < 230){sf = 0.98; if(sys=="up"){sf = sf+0.02;} if(sys=="down"){sf = sf-0.05;}}
    if(pt>=230 && pt < 250){sf = 0.97; if(sys=="up"){sf = sf+0.03;} if(sys=="down"){sf = sf-0.03;}}
    if(pt>=250 && pt < 300){sf = 0.97; if(sys=="up"){sf = sf+0.03;} if(sys=="down"){sf = sf-0.04;}}
    if(pt>=300 && pt < 400){sf = 0.97; if(sys=="up"){sf = sf+0.03;} if(sys=="down"){sf = sf-0.03;}}
    if(pt>=400 && pt < 500){sf = 0.99; if(sys=="up"){sf = sf+0.01;} if(sys=="down"){sf = sf-0.01;}}
    if(pt>=500 && pt < 700){sf = 0.97; if(sys=="up"){sf = sf+0.03;} if(sys=="down"){sf = sf-0.03;}}
    else{sf = 0.97; if(sys=="up"){sf = sf+0.03;} if(sys=="down"){sf = sf-0.03;}}
  }
  if(eta>=-2.0 && eta<-1.566){
    if(pt>=210 && pt < 230){sf = 0.97; if(sys=="up"){sf = sf+0.02;} if(sys=="down"){sf = sf-0.02;}}
    if(pt>=230 && pt < 250){sf = 1.0; if(sys=="up"){sf = sf+0.0;} if(sys=="down"){sf = sf-0.01;}}
    if(pt>=250 && pt < 300){sf = 0.99; if(sys=="up"){sf = sf+0.01;} if(sys=="down"){sf = sf-0.02;}}
    if(pt>=300 && pt < 400){sf = 0.98; if(sys=="up"){sf = sf+0.02;} if(sys=="down"){sf = sf-0.02;}}
    if(pt>=400 && pt < 500){sf = 0.99; if(sys=="up"){sf = sf+0.01;} if(sys=="down"){sf = sf-0.01;}}
    if(pt>=500 && pt < 700){sf = 1.0; if(sys=="up"){sf = sf+0.0;} if(sys=="down"){sf = sf-0.01;}}
    else{sf = 1.0; if(sys=="up"){sf = sf+0.0;} if(sys=="down"){sf = sf-0.01;}}
  }
  if(eta>=-1.44 && eta<-0.8){
    if(pt>=210 && pt < 230){sf = 0.98; if(sys=="up"){sf = sf+0.01;} if(sys=="down"){sf = sf-0.01;}}
    if(pt>=230 && pt < 250){sf = 0.98; if(sys=="up"){sf = sf+0.02;} if(sys=="down"){sf = sf-0.02;}}
    if(pt>=250 && pt < 300){sf = 1.0; if(sys=="up"){sf = sf+0.0;} if(sys=="down"){sf = sf-0.01;}}
    if(pt>=300 && pt < 400){sf = 0.99; if(sys=="up"){sf = sf+0.004;} if(sys=="down"){sf = sf-0.004;}}
    if(pt>=400 && pt < 500){sf = 0.98; if(sys=="up"){sf = sf+0.02;} if(sys=="down"){sf = sf-0.02;}}
    if(pt>=500 && pt < 700){sf = 0.99; if(sys=="up"){sf = sf+0.01;} if(sys=="down"){sf = sf-0.01;}}
    else{sf = 0.98; if(sys=="up"){sf = sf+0.02;} if(sys=="down"){sf = sf-0.02;}}
  }
  if(eta>=-0.8 && eta<0.0){
    if(pt>=210 && pt < 230){sf = 0.96; if(sys=="up"){sf = sf+0.02;} if(sys=="down"){sf = sf-0.02;}}
    if(pt>=230 && pt < 250){sf = 0.99; if(sys=="up"){sf = sf+0.01;} if(sys=="down"){sf = sf-0.01;}}
    if(pt>=250 && pt < 300){sf = 0.99; if(sys=="up"){sf = sf+0.01;} if(sys=="down"){sf = sf-0.01;}}
    if(pt>=300 && pt < 400){sf = 0.99; if(sys=="up"){sf = sf+0.01;} if(sys=="down"){sf = sf-0.01;}}
    if(pt>=400 && pt < 500){sf = 0.99; if(sys=="up"){sf = sf+0.01;} if(sys=="down"){sf = sf-0.01;}}
    if(pt>=500 && pt < 700){sf = 0.99; if(sys=="up"){sf = sf+0.01;} if(sys=="down"){sf = sf-0.01;}}
    else{sf = 0.99; if(sys=="up"){sf = sf+0.01;} if(sys=="down"){sf = sf-0.01;}}
  }
  if(eta>=0.0 && eta<0.8){
    if(pt>=210 && pt < 230){sf = 0.96; if(sys=="up"){sf = sf+0.03;} if(sys=="down"){sf = sf-0.03;}}
    if(pt>=230 && pt < 250){sf = 0.98; if(sys=="up"){sf = sf+0.02;} if(sys=="down"){sf = sf-0.02;}}
    if(pt>=250 && pt < 300){sf = 1.0; if(sys=="up"){sf = sf+0.0;} if(sys=="down"){sf = sf-0.01;}}
    if(pt>=300 && pt < 400){sf = 0.99; if(sys=="up"){sf = sf+0.01;} if(sys=="down"){sf = sf-0.01;}}
    if(pt>=400 && pt < 500){sf = 0.97; if(sys=="up"){sf = sf+0.02;} if(sys=="down"){sf = sf-0.02;}}
    if(pt>=500 && pt < 700){sf = 0.98; if(sys=="up"){sf = sf+0.01;} if(sys=="down"){sf = sf-0.01;}}
    else{sf = 0.99; if(sys=="up"){sf = sf+0.01;} if(sys=="down"){sf = sf-0.01;}}
  }
  if(eta>=0.8 && eta<1.44){
    if(pt>=210 && pt < 230){sf = 0.98; if(sys=="up"){sf = sf+0.01;} if(sys=="down"){sf = sf-0.01;}}
    if(pt>=230 && pt < 250){sf = 0.99; if(sys=="up"){sf = sf+0.01;} if(sys=="down"){sf = sf-0.01;}}
    if(pt>=250 && pt < 300){sf = 0.99; if(sys=="up"){sf = sf+0.01;} if(sys=="down"){sf = sf-0.01;}}
    if(pt>=300 && pt < 400){sf = 0.99; if(sys=="up"){sf = sf+0.01;} if(sys=="down"){sf = sf-0.01;}}
    if(pt>=400 && pt < 500){sf = 0.99; if(sys=="up"){sf = sf+0.01;} if(sys=="down"){sf = sf-0.01;}}
    if(pt>=500 && pt < 700){sf = 0.99; if(sys=="up"){sf = sf+0.01;} if(sys=="down"){sf = sf-0.01;}}
    else{sf = 0.99; if(sys=="up"){sf = sf+0.01;} if(sys=="down"){sf = sf-0.01;}}
  }
  if(eta>=1.566 && eta<2.0){
    if(pt>=210 && pt < 230){sf = 0.96; if(sys=="up"){sf = sf+0.02;} if(sys=="down"){sf = sf-0.02;}}
    if(pt>=230 && pt < 250){sf = 0.98; if(sys=="up"){sf = sf+0.01;} if(sys=="down"){sf = sf-0.02;}}
    if(pt>=250 && pt < 300){sf = 0.98; if(sys=="up"){sf = sf+0.02;} if(sys=="down"){sf = sf-0.03;}}
    if(pt>=300 && pt < 400){sf = 0.99; if(sys=="up"){sf = sf+0.01;} if(sys=="down"){sf = sf-0.01;}}
    if(pt>=400 && pt < 500){sf = 0.98; if(sys=="up"){sf = sf+0.01;} if(sys=="down"){sf = sf-0.02;}}
    if(pt>=500 && pt < 700){sf = 0.99; if(sys=="up"){sf = sf+0.01;} if(sys=="down"){sf = sf-0.01;}}
    else{sf = 0.98; if(sys=="up"){sf = sf+0.02;} if(sys=="down"){sf = sf-0.04;}}
  }
  if(eta>=2.0 && eta<=2.5){
    if(pt>=210 && pt < 230){sf = 0.92; if(sys=="up"){sf = sf+0.05;} if(sys=="down"){sf = sf-0.05;}}
    if(pt>=230 && pt < 250){sf = 0.97; if(sys=="up"){sf = sf+0.02;} if(sys=="down"){sf = sf-0.03;}}
    if(pt>=250 && pt < 300){sf = 0.96; if(sys=="up"){sf = sf+0.04;} if(sys=="down"){sf = sf-0.04;}}
    if(pt>=300 && pt < 400){sf = 0.95; if(sys=="up"){sf = sf+0.01;} if(sys=="down"){sf = sf-0.01;}}
    if(pt>=400 && pt < 500){sf = 0.96; if(sys=="up"){sf = sf+0.04;} if(sys=="down"){sf = sf-0.04;}}
    if(pt>=500 && pt < 700){sf = 0.98; if(sys=="up"){sf = sf+0.02;} if(sys=="down"){sf = sf-0.03;}}
    else{sf = 1.0; if(sys=="up"){sf = sf+0.0;} if(sys=="down"){sf = sf-0.05;}}
  }
return(sf);
}
