#!/bin/bash
altozip=$1
if [ ! -f "$altozip" ]; then
    echo "$altozip does not exist."
    exit 1
fi
cd $HOME/escr/in
rm *.xml
cd $HOME/escr/out
rm *.xml


cd $HOME/escr/in
unzip $altozip
retVal=$?
if [ $retVal -ne 0 ]; then
    echo "Cannot unzip"
    exit $retVal
fi
python3 $HOME/ladino-transcript/scripts/escr_content.py \$HOME/escr/in \$HOME/escr/out

rm /mnt/c/Temp/escr.zip
cd $HOME/escr/out
zip /mnt/c/Temp/escr.zip *.xml
