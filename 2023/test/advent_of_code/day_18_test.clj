(ns advent-of-code.day-18-test
  (:require [clojure.test :refer [deftest testing is]]
            [advent-of-code.support :refer [read-file]]
            [advent-of-code.day-18 :refer [part-1 part-2]]
            [clojure.java.io :refer [resource]]))

(def day 18)

(deftest part1
  (let [expected 62]
    (is (= expected (part-1 (read-file day "example"))))))

(deftest part2
  (let [expected "PART2_NOT_IMPLEMENTED"]
    (is (= expected (part-2 (read-file day "example"))))))
