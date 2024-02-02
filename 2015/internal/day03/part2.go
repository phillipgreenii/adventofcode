package day03

import (
	"fmt"
	"strconv"

	"github.com/phillipgreenii/adventofcode/2015/internal/common"
)

type Mover struct {
	x int
	y int
}

func (m *Mover) MoveAndMark(dir rune, visitStore map[string]int) {
	switch dir {
	case '^':
		m.y += 1
	case 'v':
		m.y -= 1
	case '>':
		m.x += 1
	case '<':
		m.x -= 1
	}
	p := fmt.Sprintf("%d:%d", m.x, m.y)

	visitStore[p] += 1
}

func Part2(input common.Input) string {
	visits := make(map[string]int)

	santa := Mover{}
	robot := Mover{}

	line := input.Lines()[0]
	move_santa := true
	santa.MoveAndMark('.', visits)
	robot.MoveAndMark('.', visits)
	for _, dir := range line {
		if move_santa {
			santa.MoveAndMark(dir, visits)
		} else {
			robot.MoveAndMark(dir, visits)
		}
		move_santa = !move_santa
	}

	return strconv.Itoa(len(visits))
}
