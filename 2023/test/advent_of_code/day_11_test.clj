(ns advent-of-code.day-11-test
  (:require [clojure.test :refer [deftest testing is]]
            [advent-of-code.support :refer [read-file]]
            [advent-of-code.day-11 :refer [part-1 part-2]]
            [clojure.java.io :refer [resource]]))

(def day 11)

(deftest part1
  (let [expected 374]
    (is (= expected (part-1 (read-file day "example"))))))

(deftest part2-1
  (let [expected 1030]
    (is (= expected (part-2 (read-file day "example") :expansion-factor 10 )))))

(deftest part2-2
  (let [expected 8410]
    (is (= expected (part-2 (read-file day "example") :expansion-factor 100)))))
