package day02

import (
	"testing"

	"github.com/phillipgreenii/adventofcode/2015/internal/common"
)

func TestPart1(t *testing.T) {

	t.Run("part 1", func(t *testing.T) {
		var expected = "101"

		input, err := common.LoadFile(Day, "example")

		if err != nil {
			t.Fatalf("unable to load example: %v", err)
		}
		result := Part1(input)
		if result != expected {
			t.Fatalf("got %s, expected %s", result, expected)
		}
	})

}