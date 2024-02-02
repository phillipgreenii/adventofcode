package day03

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
		{"^v", "3"},
		{"^>v<", "3"},
		{"^v^v^v^v^v", "11"},
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
