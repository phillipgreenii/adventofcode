verify() {

  usage="""
  Usage: verify 
  """

  log_file="verify.log"

  non_failed="-"
  failed="%"

  echo "01 02 03 04 05 06 07 08 09 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25"

  echo -n "" >$log_file
  failures=0
  for d in {1..25}
  do 
    if [[ $d -ne 1 ]]; then
      echo -n " "
    fi
    printf "Day %02d\n" $d >>$log_file

    echo "  Part 1" >>$log_file
    cmd="./run --verify $d 1"
    $cmd > /dev/null 2>>$log_file
    if [[ $? -eq 0 ]]; then
      echo "    PASSED" >>$log_file
      echo -n $non_failed
    else
      echo "    FAILED" >>$log_file
      echo -n $failed
      ((failures++))
    fi


    echo "  Part 2" >>$log_file
    cmd="./run --verify $d 2"
    $cmd > /dev/null 2>>$log_file
    if [[ $? -eq 0 ]]; then
      echo "    PASSED" >>$log_file
      echo -n $non_failed
    else
      echo "    FAILED" >>$log_file
      echo -n $failed
      ((failures++))
    fi
  done

  echo 

  return $failures
}