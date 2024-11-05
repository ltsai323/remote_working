#for BDTXML in `find . -mindepth 2 -name "*.xml" -type f | sort`;do
for BDTXML in *.xml;do
    cat $BDTXML | grep -v "Spectator" > tmp.xml

    ORGNAME=$(echo $BDTXML | sed "s|.xml|_original.xml|g")

    #echo "mv $BDTXML $ORGNAME"
    mv $BDTXML $ORGNAME

    #echo "mv tmp.xml  $BDTXML"
    mv tmp.xml  $BDTXML

    diff -y -W 200 --suppress-common-lines $ORGNAME $BDTXML 
    echo ""
done
