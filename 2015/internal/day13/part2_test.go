package day13

import (
	"testing"

	"github.com/phillipgreenii/adventofcode/2015/internal/common"
)

func TestPart2(t *testing.T) {

	t.Run("part 2", func(t *testing.T) {
		var expected = "PART2-EXAMPLE-EXPECTED"

		input, err := common.LoadFile(Day, "part2-example")

		if err != nil {
			t.Fatalf("unable to load example: %v", err)
		}
		result := Part2(input)
		if result != expected {
			t.Fatalf("got %s, expected %s", result, expected)
		}
	})

}
