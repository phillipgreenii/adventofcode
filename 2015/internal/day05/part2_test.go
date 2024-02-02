package day05

import (
	"fmt"
	"testing"

	"github.com/phillipgreenii/adventofcode/2015/internal/common"
)

func TestPart2IsNice(t *testing.T) {

	var tests = []struct {
		input          string
		expectedResult bool
	}{
		{"qjhvhtzxzqqjkmpb", true},
		{"xxyxx", true},
		{"uurcxstgmygtbstg", false},
		{"ieodomkazucvgmuy", false},
	}

	for i, tt := range tests {
		t.Run(fmt.Sprintf("Part2IsNice: %d", i), func(t *testing.T) {
			result := IsNice(tt.input)
			if result != tt.expectedResult {
				t.Fatalf("got %t, expected %t", result, tt.expectedResult)
			}
		})
	}
}

func TestPart2(t *testing.T) {

	t.Run("part 2", func(t *testing.T) {
		var expected = "2"

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
