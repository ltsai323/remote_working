if [ -d "barrel_photon" ]; then
    cd barrel_photon
else
    mkdir barrel_photon
    cd barrel_photon
    ln -s ../dataMCcomp_barrelPhoton.root dataMCcomp.root
fi

python3 ../visualize.py
