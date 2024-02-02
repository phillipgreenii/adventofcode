package day01

import (
	"strconv"

	"github.com/phillipgreenii/adventofcode/2015/internal/common"
)

func Part2(input common.Input) string {
	l := input.Lines()[0]
	floor := 0
	for position, character := range l {
		if character == '(' {
			floor += 1
		} else if character == ')' {
			floor -= 1
		}
		if floor < 0 {
			return strconv.Itoa(position + 1)
		}
	}
	return strconv.Itoa(len(l))
}
