package day03

import (
	"fmt"
	"strconv"

	"github.com/phillipgreenii/adventofcode/2015/internal/common"
)

func Part1(input common.Input) string {
	x := 0
	y := 0

	visits := make(map[string]int)
	markVisit := func() {
		p := fmt.Sprintf("%d:%d", x, y)
		visits[p] += 1
	}

	line := input.Lines()[0]
	markVisit()
	for _, dir := range line {
		switch dir {
		case '^':
			y += 1
		case 'v':
			y -= 1
		case '>':
			x += 1
		case '<':
			x -= 1
		}
		markVisit()
	}

	return strconv.Itoa(len(visits))
}
