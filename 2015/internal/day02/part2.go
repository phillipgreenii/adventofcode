package day02

import (
	"strconv"

	"github.com/phillipgreenii/adventofcode/2015/internal/common"
)

func Part2(input common.Input) string {
	total := 0
	for _, line := range input.Lines() {
		if line == "" {
			continue
		}

		dimensions, err := parseDimensions(line)
		if err != nil {
			panic(err.Error())
		}

		biggest := max(dimensions[0], dimensions[1], dimensions[2])

		wrap := 2 * (dimensions[0] + dimensions[1] + dimensions[2] - biggest)

		bow := dimensions[0] * dimensions[1] * dimensions[2]

		total += wrap + bow
	}
	return strconv.Itoa(total)
}
