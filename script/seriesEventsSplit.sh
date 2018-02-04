#!/bin/bash

stuff="./eventTimeList.data"
sort -k 4 -t , $stuff > tempfile
# show events amount of each year
# awk -F, 'BEGIN{
#   year2015 = 0;
#   year2016 = 0;
#   year2017 = 0;
#   year2018 = 0;
#   others = 0;
#   }
#    {
#      print $4;
#      if(index($4,"2015")) {
#        year2015 += 1;
#      } else if(index($4, "2016")) {
#        year2016 += 1;
#      } else if (index($4, "2017")) {
#        year2017 += 1;
#      } else if (index($4, "2018")) {
#        year2018 += 1;
#      } else {
#        others += 1;
#      }
#    }
#     END{
#     print year2015, year2016, year2017, year2018, others;
#   }'
awk -F, '$4~  /201[56]/ {print $0}' tempfile > eventsBefore20161231.data
awk -F, '$4~  /201[78]/ {print $0}' tempfile > eventsAfter20161231.data
rm tempfile
