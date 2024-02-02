package day01

import (
	"fmt"
	"testing"

	"github.com/phillipgreenii/adventofcode/2015/internal/common"
)

func TestPart1(t *testing.T) {

	var tests = []struct {
		input          string
		expectedResult string
	}{
		{"(())", "0"},
		{"()()", "0"},
		{"(((", "3"},
		{"(()(()(", "3"},
		{"))(((((", "3"},
		{"())", "-1"},
		{"))(", "-1"},
		{")))", "-3"},
		{")())())", "-3"},
	}

	for i, tt := range tests {
		t.Run(fmt.Sprintf("part 1: %d", i), func(t *testing.T) {
			input := common.AsInput(tt.input)
			result := Part1(input)
			if result != tt.expectedResult {
				t.Fatalf("got %s, expected %s", result, tt.expectedResult)
			}
		})
	}
}
