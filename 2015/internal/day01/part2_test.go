package day01

import (
	"fmt"
	"testing"

	"github.com/phillipgreenii/adventofcode/2015/internal/common"
)

func TestPart2(t *testing.T) {

	var tests = []struct {
		input          string
		expectedResult string
	}{
		{")", "1"},
		{"()())", "5"},
	}

	for i, tt := range tests {
		t.Run(fmt.Sprintf("part 2: %d", i), func(t *testing.T) {
			input := common.AsInput(tt.input)
			result := Part2(input)
			if result != tt.expectedResult {
				t.Fatalf("got %s, expected %s", result, tt.expectedResult)
			}
		})
	}
}
