package cmd

import (
	"errors"
	"fmt"
	"strconv"

	"github.com/spf13/cobra"

	"github.com/phillipgreenii/adventofcode/2015/internal/common"
	"github.com/phillipgreenii/adventofcode/2015/internal/day01"
	"github.com/phillipgreenii/adventofcode/2015/internal/day02"
	"github.com/phillipgreenii/adventofcode/2015/internal/day03"
	"github.com/phillipgreenii/adventofcode/2015/internal/day04"
	"github.com/phillipgreenii/adventofcode/2015/internal/day05"
	"github.com/phillipgreenii/adventofcode/2015/internal/day06"
	"github.com/phillipgreenii/adventofcode/2015/internal/day07"
	"github.com/phillipgreenii/adventofcode/2015/internal/day08"
	"github.com/phillipgreenii/adventofcode/2015/internal/day09"
	"github.com/phillipgreenii/adventofcode/2015/internal/day10"
	"github.com/phillipgreenii/adventofcode/2015/internal/day11"
	"github.com/phillipgreenii/adventofcode/2015/internal/day12"
	"github.com/phillipgreenii/adventofcode/2015/internal/day13"
	"github.com/phillipgreenii/adventofcode/2015/internal/day14"
	"github.com/phillipgreenii/adventofcode/2015/internal/day15"
	"github.com/phillipgreenii/adventofcode/2015/internal/day16"
	"github.com/phillipgreenii/adventofcode/2015/internal/day17"
	"github.com/phillipgreenii/adventofcode/2015/internal/day18"
	"github.com/phillipgreenii/adventofcode/2015/internal/day19"
	"github.com/phillipgreenii/adventofcode/2015/internal/day20"
	"github.com/phillipgreenii/adventofcode/2015/internal/day21"
	"github.com/phillipgreenii/adventofcode/2015/internal/day22"
	"github.com/phillipgreenii/adventofcode/2015/internal/day23"
	"github.com/phillipgreenii/adventofcode/2015/internal/day24"
	"github.com/phillipgreenii/adventofcode/2015/internal/day25"
)

func NewRootCommand() *cobra.Command {

	result := &cobra.Command{
		Use:     "aoc2015",
		Short:   "Advent of Code 2015 Solutions",
		Long:    "Golang implementations for the 2015 Advent of Code problems",
		Example: "go run main.go 1 1",
		Args:    cobra.ExactArgs(2),
		RunE: func(_ *cobra.Command, args []string) error {
			if len(args) != 2 {
				return errors.New("Must have 2 args: day part")
			}
			day, err := strconv.Atoi(args[0])
			if err != nil {
				return err
			}
			part, err := strconv.Atoi(args[1])
			if err != nil {
				return err
			}
			return run(day, part)
		},
	}

	return result
}

var AllSolvers = [...][2]common.Solver{
	day01.Solvers,
	day02.Solvers,
	day03.Solvers,
	day04.Solvers,
	day05.Solvers,
	day06.Solvers,
	day07.Solvers,
	day08.Solvers,
	day09.Solvers,
	day10.Solvers,
	day11.Solvers,
	day12.Solvers,
	day13.Solvers,
	day14.Solvers,
	day15.Solvers,
	day16.Solvers,
	day17.Solvers,
	day18.Solvers,
	day19.Solvers,
	day20.Solvers,
	day21.Solvers,
	day22.Solvers,
	day23.Solvers,
	day24.Solvers,
	day25.Solvers,
}

func run(day int, part int) error {

	if !(1 <= day && day <= len(AllSolvers)) {
		return errors.New(fmt.Sprintf("day must be between 1 and %d", len(AllSolvers)))
	}

	if !(1 <= part && part <= 2) {
		return errors.New("part must be 1 or 2")
	}

	input, err := common.LoadInput(day, part)
	if err != nil {
		return err
	}

	solver := AllSolvers[day-1][part-1]
	answer := solver(input)

	fmt.Printf("%s\n", answer)
	return nil
}
