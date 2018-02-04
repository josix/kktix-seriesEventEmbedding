awk -F, '
  {
    if( $11 != "" && $5 != "" && $3 != "" && (index($15, "2015") || index($15, "2016"))){
      # print $5, $11, $15, $16
      print $5, $11
    }
  }'  ../entertainment_transactions_v7.csv > entertainment_transactions_v6_Before20161231.data
