cat cogg_wofs_2018_diff_cleaned.txt | awk -F "/" \
    '{  print"datacube-alchemist addtoqueue time in [" $3 "-" $4 "-" $5 ", "  $3 "-" $4 "-" $5 "]  region_code=""\x27""\x22" $1$2  "\x22\x27" "   #  " $1 "/" $2"/" $3"/" $4"/" $5}' > fill_wofs_gaps_2018.sh

# "\x27\x22" "121060"  "\x22\x27"
# "datacube-alchemist addtoqueue time in [2017-01-01, 2017-01-01]  region_code="

# Getting the id files - wofs
# cat wofs2-2016.txt  | awk -F "/" '{print$7 "/" $8"/" $9"/" $10"/" $11}' | sort > wofs2-2016-id.txt

# Getting the id files - coggs
#cat c2cogged-all-no-fill-5astrix-2018.txt  | awk -F "/" '{print$5"/" $6"/" $7 "/" $8"/" $9}' | sort > c2cogged-2018-id.txt
