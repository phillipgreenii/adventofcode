package day06

import (
	"regexp"
	"strconv"
	"strings"

	"github.com/phillipgreenii/adventofcode/2015/internal/common"
)

type Rect struct {
	UL [2]int
	LR [2]int
}

func (r *Rect) Contains(x, y int) bool {
	return (r.UL[0] <= x && x <= r.LR[0]) &&
		(r.UL[1] <= y && y <= r.LR[1])
}

type RectOperation struct {
	Code rune
	R    Rect
}

var r = regexp.MustCompile("([^0-9]+)([0-9]+),([0-9]+)[^0-9]+([0-9]+),([0-9]+)")

func ParseOperation(line string) RectOperation {
	parts := r.FindStringSubmatch(line)
	var code rune
	if strings.Contains(parts[1], "on") {
		code = '1'
	} else if strings.Contains(parts[1], "off") {
		code = '0'
	} else {
		code = 'T'
	}

	ulX, _ := strconv.Atoi(parts[2])
	ulY, _ := strconv.Atoi(parts[3])

	lrX, _ := strconv.Atoi(parts[4])
	lrY, _ := strconv.Atoi(parts[5])

	return RectOperation{
		Code: code,
		R: Rect{
			UL: [2]int{ulX, ulY},
			LR: [2]int{lrX, lrY},
		},
	}
}

func CountLights(operations []RectOperation) int {
	var onLights = 0

	var l bool
	for x := 0; x < 1000; x++ {
		for y := 0; y < 1000; y++ {
			l = false
			for _, o := range operations {
				if o.R.Contains(x, y) {
					if o.Code == '1' {
						l = true
					} else if o.Code == '0' {
						l = false
					} else {
						l = !l
					}

				}
			}
			if l {
				onLights += 1
			}

		}
	}
	return onLights
}

func Part1(input common.Input) string {

	operations := make([]RectOperation, 0)

	for _, line := range input.Lines() {
		if line == "" {
			continue
		}
		operation := ParseOperation(line)
		operations = append(operations, operation)
	}
	onLightsCount := CountLights(operations)

	return strconv.Itoa(onLightsCount)
}
