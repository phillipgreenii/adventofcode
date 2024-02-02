(ns advent-of-code.day-08-test
  (:require [clojure.test :refer [deftest testing is]]
            [advent-of-code.support :refer [read-file]]
            [advent-of-code.day-08 :refer [part-1 part-2
                                           new-path-segment generate-path-segment-key
                                           lcm]]
            [clojure.java.io :refer [resource]]))

(def day 8)

(deftest test-generate-path-segment-key
  (let [expected "AAA-2-ZZZ-5-12"]
    (is (= expected (generate-path-segment-key (new-path-segment "AAA" 2 "ZZZ" 5 12))))))

(deftest test-lcm-1
  (let [expected 156]
    (is (= expected (lcm 13 12)))))

(deftest test-lcm-2
  (let [expected 36]
    (is (= expected (lcm 9 12)))))

(deftest part1-1
  (let [expected 2]
    (is (= expected (part-1 (read-file day "part1-example-1"))))))

(deftest part1-2
  (let [expected 6]
    (is (= expected (part-1 (read-file day "part1-example-2"))))))

(deftest part2
  (let [expected 6]
    (is (= expected (part-2 (read-file day "part2-example"))))))
