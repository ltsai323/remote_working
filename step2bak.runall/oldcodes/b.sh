pPtRange=("$@")

for (( idx=0; idx<${#pPtRange[@]}; idx++)); do
    pPtR=${pPtRange[$idx]}
    echo $pPtR
done
