(ns advent-of-code.day-01-test
  (:require [clojure.test :refer [deftest testing is]]
            [advent-of-code.support :refer [read-file]]
            [advent-of-code.day-01 :refer [part-1 part-2]]
            [clojure.java.io :refer [resource]]))

(def day 1)

(deftest part1
  (let [expected 142]
    (is (= expected (part-1 (read-file day "part1-example"))))))

(deftest part2
  (let [expected 281]
    (is (= expected (part-2 (read-file day "part2-example"))))))
