package day01

import (
	"strconv"

	"github.com/phillipgreenii/adventofcode/2015/internal/common"
)

func Part1(input common.Input) string {
	floor := 0
	for _, character := range input.Lines()[0] {
		if character == '(' {
			floor += 1
		} else if character == ')' {
			floor -= 1
		}
	}
	return strconv.Itoa(floor)
}
