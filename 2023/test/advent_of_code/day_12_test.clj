(ns advent-of-code.day-12-test
  (:require [clojure.test :refer [deftest testing is]]
            [advent-of-code.support :refer [read-file]]
            [advent-of-code.day-12 :refer [part-1 parse-line count-possible-arragements generate-possible-arragements is-valid-arragement part-2 unfold-record]]
            [clojure.java.io :refer [resource]]
            [clojure.string :as str]))

(def day 12)

(deftest test-parse-line
  (let [expected [[\. \? \? \. \. \? \? \. \. \. \? \# \# \.]
                  '(1 1 3)]]
    (is (= expected (parse-line ".??..??...?##. 1,1,3")))))

(deftest test-generate-possible-arragements
  (let [expected '("....###" "..#.###" ".#..###" ".##.###" "#...###" "#.#.###" "##..###" "###.###")]
    (is (= expected (generate-possible-arragements "???.###")))))

(deftest test-is-valid-arragement-1
  (let [expected true]
    (is (= expected (is-valid-arragement '(1 1 3) "#.#.###")))))

(deftest test-is-valid-arragement-1x
  (let [expected false]
    (is (= expected (is-valid-arragement '(2 3) "#.#.###")))))

(deftest test-is-valid-arragement-2
  (let [expected true]
    (is (= expected (is-valid-arragement '(1 1 3) ".#....#...###.")))))

(deftest test-is-valid-arragement-2x
  (let [expected false]
    (is (= expected (is-valid-arragement '(1 1 3) ".#....#....##.")))))

(deftest test-count-possible-arragements-1
  (let [expected 1]
    (is (= expected (count-possible-arragements (parse-line "???.### 1,1,3"))))))

(deftest test-count-possible-arragements-2
  (let [expected 4]
    (is (= expected (count-possible-arragements (parse-line ".??..??...?##. 1,1,3"))))))

(deftest test-count-possible-arragements-all
  (let [expected [1 4 1 1 4 10]]
    (is (= expected (map #(count-possible-arragements (parse-line %))
                         (str/split-lines (read-file day "example")))))))

(deftest part1
  (let [expected 21]
    (is (= expected (part-1 (read-file day "example"))))))

(deftest test-unfold-record-1
  (let [expected [[\. \# \? \. \# \? \. \# \? \. \# \? \. \#]
                  '(1 1 1 1 1)]]
    (is (= expected (unfold-record [[\. \#] '(1)])))))

(deftest test-unfold-record-2
  (let [expected [[\? \? \? \. \# \# \# \? \? \? \? \. \# \# \# \? \? \? \? \. \# \# \# \? \? \? \? \. \# \# \# \? \? \? \? \. \# \# \#]
                  '(1,1,3,1,1,3,1,1,3,1,1,3,1,1,3)]]
    (is (= expected (unfold-record [[\? \? \? \. \# \# \#] '(1,1,3)])))))

(deftest part2
  (let [expected 525152]
    (is (= expected (part-2 (read-file day "example"))))))
