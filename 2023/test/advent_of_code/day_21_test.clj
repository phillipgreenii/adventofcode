(ns advent-of-code.day-21-test
  (:require [clojure.test :refer [deftest testing is]]
            [advent-of-code.support :refer [read-file]]
            [advent-of-code.day-21 :refer [part-1 part-2]]
            [clojure.java.io :refer [resource]]))

(def day 21)

(deftest part1
  (let [input (read-file day "example")]
    (is (= 16 (part-1 input 6)))
    (is (= 42 (part-1 input)))))

(deftest part2
  (let [expected "PART2_NOT_IMPLEMENTED"]
    (is (= expected (part-2 (read-file day "example"))))))
