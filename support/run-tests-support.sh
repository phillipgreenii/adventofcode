
if [[ "$#" -gt 2 ]]; then
	echo "usage: run-tests [\$day] [\$pattern]"
    exit 1
fi
d="${1}"
pattern="${2}"

run-tests() {
    if [[ "$#" -ne 3 ]]; then
        echo "run-tests fn requires all_tests day_tests day_pattern_tests"
        exit 2
    fi
    all_tests="${1}"
    day_tests="${2}"
    day_pattern_tests="${3}"

    if [[ "$d" == "" ]]; then
        $all_tests
    elif [[ "$pattern" == "" ]]; then
        $day_tests $d
    else 
        $day_pattern_tests $d $pattern
    fi
}


