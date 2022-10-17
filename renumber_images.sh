cd /mnt/c/Users/yuda/Pictures/AnyPDFtoJPG/MeamLoez-Izmir-Devarim-1868

for f in *.jpg ; do
    echo $f
    tmp1=${f##*_}
    tmp2=${tmp1%%.jpg}
    printf -v num "%03d" $tmp2
    nam=${f%%_*}
    name=${nam}"_"${num}".jpg"
    if [ "$f" != "$name" ]; then
        echo mv $f $name
        mv "$f" "$name"
    fi
done