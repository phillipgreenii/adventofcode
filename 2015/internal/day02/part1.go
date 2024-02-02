package day02

import (
	"strconv"
	"strings"

	"github.com/phillipgreenii/adventofcode/2015/internal/common"
)

func parseDimensions(line string) ([3]int, error) {
	dimensionsAsStr := strings.SplitN(line, "x", 3)

	var dimensions [3]int
	n, err := strconv.Atoi(dimensionsAsStr[0])
	if err != nil {
		return dimensions, err
	}
	dimensions[0] = n

	n, err = strconv.Atoi(dimensionsAsStr[1])
	if err != nil {
		return dimensions, err
	}
	dimensions[1] = n

	n, err = strconv.Atoi(dimensionsAsStr[2])
	if err != nil {
		return dimensions, err
	}
	dimensions[2] = n

	return dimensions, nil
}

func Part1(input common.Input) string {
	total := 0
	for _, line := range input.Lines() {
		if line == "" {
			continue
		}

		dimensions, err := parseDimensions(line)
		if err != nil {
			panic(err.Error())
		}
		lw := dimensions[0] * dimensions[1]
		wh := dimensions[1] * dimensions[2]
		hl := dimensions[2] * dimensions[0]

		smallest := min(lw, wh, hl)

		total += (2 * lw) + (2 * wh) + (2 * hl) + smallest
	}
	return strconv.Itoa(total)
}
