package day06

import (
	"strconv"

	"github.com/phillipgreenii/adventofcode/2015/internal/common"
)

func CountLightBrightness(operations []RectOperation) int {
	var totalBrightness = 0

	var l int
	for x := 0; x < 1000; x++ {
		for y := 0; y < 1000; y++ {
			l = 0
			for _, o := range operations {
				if o.R.Contains(x, y) {
					if o.Code == '1' {
						l += 1
					} else if o.Code == '0' {
						l = max(0, l-1)
					} else {
						l += 2
					}

				}
			}
			totalBrightness += l

		}
	}
	return totalBrightness
}

func Part2(input common.Input) string {

	operations := make([]RectOperation, 0)

	for _, line := range input.Lines() {
		if line == "" {
			continue
		}
		operation := ParseOperation(line)
		operations = append(operations, operation)
	}
	lightBrightness := CountLightBrightness(operations)

	return strconv.Itoa(lightBrightness)
}
