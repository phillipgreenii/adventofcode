(ns advent-of-code.day-16-test
  (:require [clojure.test :refer [deftest testing is]]
            [advent-of-code.support :refer [read-file]]
            [advent-of-code.day-16 :refer [part-1 part-2]]
            [clojure.java.io :refer [resource]]))

(def day 16)

(deftest part1
  (let [expected 46]
    (is (= expected (part-1 (read-file day "example"))))))

(deftest part2
  (let [expected 51]
    (is (= expected (part-2 (read-file day "example"))))))
