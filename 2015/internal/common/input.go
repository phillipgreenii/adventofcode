package common

import (
	"bufio"
	"errors"
	"fmt"
	"os"
	"path/filepath"
	"runtime"
	"strings"
)

type Input interface {
	Lines() []string
}

type InputImpl struct {
	lines []string
}

func (c *InputImpl) Lines() []string {
	return c.lines
}

func exists(path string) (bool, error) {
	_, err := os.Stat(path)
	if err == nil {
		return true, nil
	}
	if os.IsNotExist(err) {
		return false, nil
	}
	return false, err
}

func determineDayInputsPath(day int) (path string, error error) {
	_, f, _, ok := runtime.Caller(1)
	if !ok {
		panic("failed to determine input path")
	}

	dayDir := filepath.Join(filepath.Dir(f), "..", fmt.Sprintf("day%02d", day), "inputs")

	fe, err := exists(dayDir)
	if err != nil {
		return "", err
	}
	if !fe {
		return "", errors.New(fmt.Sprintf("day dir [%s] does not exist", dayDir))
	}

	return dayDir, nil
}

func determineInputPath(day int, part int) (path string, error error) {

	dayDir, err := determineDayInputsPath(day)

	if err != nil {
		return "", err
	}

	partInputPath := filepath.Join(dayDir, fmt.Sprintf("part%d-input.private.txt", part))

	fe, err := exists(partInputPath)
	if fe {
		return partInputPath, nil
	}
	if err != nil {
		return "", err
	}

	dayInputPath := filepath.Join(dayDir, "input.private.txt")
	fe, err = exists(dayInputPath)
	if fe {
		return dayInputPath, nil
	}
	if err != nil {
		return "", err
	}
	return "", errors.New("no input found")
}

func AsInput(input string) *InputImpl {
	return &InputImpl{lines: strings.Split(input, "\n")}
}

func LoadInput(day int, part int) (*InputImpl, error) {

	path, err := determineInputPath(day, part)
	if err != nil {
		return nil, err
	}

	file, err := os.Open(path)
	if err != nil {
		return nil, err
	}
	defer file.Close()

	var lines []string
	scanner := bufio.NewScanner(file)
	for scanner.Scan() {
		lines = append(lines, scanner.Text())
	}
	return &InputImpl{lines: lines}, scanner.Err()
}

func LoadFile(day int, name string) (*InputImpl, error) {

	dayDir, err := determineDayInputsPath(day)

	if err != nil {
		return nil, err
	}

	filePath := filepath.Join(dayDir, fmt.Sprintf("%s.private.txt", name))
	fe, err := exists(filePath)
	if err != nil {
		return nil, err
	}
	if !fe {
		return nil, errors.New(fmt.Sprintf("file not found: %s.private.txt", name))
	}

	file, err := os.Open(filePath)
	if err != nil {
		return nil, err
	}
	defer file.Close()

	var lines []string
	scanner := bufio.NewScanner(file)
	for scanner.Scan() {
		lines = append(lines, scanner.Text())
	}
	return &InputImpl{lines: lines}, scanner.Err()
}

type Solver func(Input) string
