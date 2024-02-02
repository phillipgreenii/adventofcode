WORK_DIR=`mktemp -d --suffix upst`
function cleanup {      
  rm -rf "$WORK_DIR"
}
trap cleanup EXIT

# | Day | Stars | Status             |
# |----:|------:|:-------------------|
# |   1 |     0 | Part 1 Not Working |
# |   2 |     2 | Solved             |
# |   3 |     1 | Part 2 Not Working |
# |   3 |     1 | Part 2 Not Started |
# |   4 |     2 | Solved             |

_generate_status_header() {

cat <<EOF
| Day | Stars | Status             |
|----:|------:|:-------------------|
EOF

}

_generate_day_status() {
  question=${1}
  stars=${2}
 
  if [[ $stars -eq 2 ]]; then
    desc="Solved"
  elif [[ $stars -eq 1 && $question -eq 2 ]]; then
    desc="Part 2 Not Working"
  elif [[ $stars -eq 1 && $question -eq 1 ]]; then
    desc="Part 2 Not Started"
  elif [[ $stars -eq 0 && $question -eq 1 ]]; then
    desc="Part 1 Not Working"
  elif [[ $stars -eq 0 && $question -eq 0 ]]; then
    desc="Part 1 Not Started"
  else
    desc="!Unknown!"
  fi
  
  printf '| %3s | %5s | %-18s |\n' "$d" "$stars" "$desc"
}

_generate_status_table() {
    dirpath_pattern=$1

_generate_status_header
for d in {1..25}
do 
  questions=0
  stars=0

  base_path=$(printf "${dirpath_pattern}" ${d})

  if [[ ! -d $base_path ]]; then 
    continue
  fi

  if [[ -s "${base_path}/part1-question.private.txt" ]]; then
    ((questions++))
  fi
  if [[ -s "${base_path}/part2-question.private.txt" ]]; then
    ((questions++))
  fi

  if [[ -s "${base_path}/part1-answer.private.txt" ]]; then
    ((stars++))
  fi
  if [[ -s "${base_path}/part2-answer.private.txt" ]]; then
    ((stars++))
  fi
  
  _generate_day_status $questions $stars

done

}

update-status () {
    if [[ "$#" -ne 1 ]]; then
        echo "update-status fn requires inputs_dir_pattern"
        exit 2
    fi

    inputs_dir_pattern="${1}"

    readme="./README.md"

    s=$(grep -n -m 1 STATUS_TABLE_START ${readme} |sed  's/\([0-9]*\).*/\1/')
    e=$(grep -n -m 1 STATUS_TABLE_END ${readme} |sed  's/\([0-9]*\).*/\1/')

    if [[ "$s" -eq "" || "$e" -eq "" ]]; then
    echo "STATUS_TABLE_START comment or STATUS_TABLE_END comment not found"  >&2
    exit 2
    fi

    tmp_readme="${WORK_DIR}/README.md.tmp"
    (
    head -n $s ${readme}
    _generate_status_table "${inputs_dir_pattern}"
    tail -n +$e ${readme}
    ) > ${tmp_readme}
    cat ${tmp_readme} > ${readme}

}