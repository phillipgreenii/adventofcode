package day05

import (
	"regexp"
	"strconv"

	"github.com/phillipgreenii/adventofcode/2015/internal/common"
)

var three_vowels_re = regexp.MustCompile(`[aeiou].*[aeiou].*[aeiou]`)
var contains_duplicate_letter_re = regexp.MustCompile(`([a-z])\\1{1}`)
var has_disallowed_substrings_re = regexp.MustCompile(`ab|cd|pq|xy`)

func IsNice(word string) bool {
	var vowelCount = 0
	var foundDuplicate = false
	var previousChar rune

	for _, char := range word {

		if (previousChar == 'a' && char == 'b') ||
			(previousChar == 'c' && char == 'd') ||
			(previousChar == 'p' && char == 'q') ||
			(previousChar == 'x' && char == 'y') {
			return false
		}

		if 'a' == char ||
			'e' == char ||
			'i' == char ||
			'o' == char ||
			'u' == char {
			vowelCount += 1
		}
		foundDuplicate = foundDuplicate || (previousChar == char)

		previousChar = char
	}

	return vowelCount >= 3 && foundDuplicate

	// fmt.Printf("%s:%t:%t:%t\n", word, three_vowels_re.Match([]byte(word)),
	// 	contains_duplicate_letter_re.Match([]byte(word)),
	// 	!three_vowels_re.Match([]byte(word)))

	// return three_vowels_re.Match([]byte(word)) &&
	// 	contains_duplicate_letter_re.Match([]byte(word)) &&
	// 	!three_vowels_re.Match([]byte(word))
}

func Part1(input common.Input) string {
	niceCount := 0

	for _, word := range input.Lines() {
		if IsNice(word) {
			niceCount += 1
		}
	}

	return strconv.Itoa(niceCount)
}
