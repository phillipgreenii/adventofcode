package main

import (
	"os"

	"github.com/phillipgreenii/adventofcode/2015/cmd"
)

func main() {
	if err := cmd.NewRootCommand().Execute(); err != nil {
		os.Exit(1)
	}
}
