run_usage="""
Usage: run [--verify] \$day \$part
where day is 1-25 and part is either 1 or 2
"""

if [[ "$#" -eq 2 ]]; then
    verify=""
    d="${1}"
    p="${2}"
elif [[ "$#" -eq 3 && "$1" == "--verify" ]]; then
    verify="1"
    d="${2}"
    p="${3}"
else
	echo "${run_usage}"
    exit 1
fi

run() {
    cmd_fn="${1}"
    inputs_dir_fn="${2}"

    cmd="$(cmd_fn $d $p)"

    # not verify, then run the command
    if [[ "$verify" -eq "" ]]; then
        time $cmd
        exit $?
    fi

    answer_file="$(inputs_dir_fn $d $p)/part${p}-answer.private.txt"
    if [[ ! -s "$answer_file" ]]; then
        echo "Skipping, not solved" >&2
        exit
    fi

    expected=$(cat $answer_file)
    result=$($cmd)

    if [[ "${expected}" != "${result}" ]]; then
        echo "${expected} <> ${result}" >&2
        exit 2
    fi
}
