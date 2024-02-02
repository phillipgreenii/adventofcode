(ns advent-of-code.day-13-test
  (:require [clojure.test :refer [deftest testing is]]
            [advent-of-code.support :refer [read-file]]
            [advent-of-code.day-13 :refer [part-1 transpose-grid part-2]]
            [clojure.java.io :refer [resource]]))

(def day 13)

(deftest test-transpose-grid-0
  (let [grid
        nil
        expected
        nil]
    (is (= expected (transpose-grid grid)))))

(deftest test-transpose-grid-1
  (let [grid
        [[1]]
        expected
        [[1]]]
    (is (= expected (transpose-grid grid)))))

(deftest test-transpose-grid-2
  (let [grid
        [[1 2]
         [3 4]]
        expected
        [[1 3]
         [2 4]]]
    (is (= expected (transpose-grid grid)))))

(deftest test-transpose-grid-3
  (let [grid
        [[1 2 3]
         [4 5 6]]
        expected
        [[1 4]
         [2 5]
         [3 6]]]
    (is (= expected (transpose-grid grid)))))

(deftest part1
  (let [expected 405]
    (is (= expected (part-1 (read-file day "example"))))))

(deftest part2
  (let [expected 400]
    (is (= expected (part-2 (read-file day "example"))))))
