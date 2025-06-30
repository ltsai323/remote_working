if [ -d "endcap_photon" ]; then
    cd endcap_photon
else
    mkdir endcap_photon
    cd endcap_photon
    ln -s ../dataMCcomp_endcapPhoton.root dataMCcomp.root
fi

python3 ../visualize.py
