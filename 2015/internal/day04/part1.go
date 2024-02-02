package day04

import (
	"crypto/md5"
	"fmt"
	"strconv"
	"strings"

	"github.com/phillipgreenii/adventofcode/2015/internal/common"
)

func Part1(input common.Input) string {

	secret_key := input.Lines()[0]

	var md5Val string
	var data []byte
	for i := 0; i < 10000000; i++ {
		data = []byte(fmt.Sprintf("%s%d", secret_key, i))
		md5Val = fmt.Sprintf("%x", md5.Sum(data))
		if strings.HasPrefix(md5Val, "00000") {
			return strconv.Itoa(i)
		}
	}
	return ""
}
