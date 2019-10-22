diff wofs2-small-id.txt wofs2-small2-id.txt | \
    grep \< | awk -F " " '{print$2}' | awk -F "/" \
    '{  print"datacube-alchemist addtoqueue time in [" $3 "-" $4 "-" $5 ", "  $3 "-" $4 "-" $5 "]  region_code=""\x27""\x22" $1$2  "\x22\x27" "   #  " $1 "/" $2"/" $3"/" $4"/" $5}'

# "\x27\x22" "121060"  "\x22\x27"
# "datacube-alchemist addtoqueue time in [2017-01-01, 2017-01-01]  region_code="
