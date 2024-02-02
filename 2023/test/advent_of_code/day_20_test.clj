(ns advent-of-code.day-20-test
  (:require [clojure.test :refer [deftest testing is]]
            [advent-of-code.support :refer [read-file]]
            [advent-of-code.day-20 :refer [receive make-flip-flop make-conjunction make-broadcaster make-output
                                           make-high-pulse
                                           make-low-pulse
                                           part-1 part-2]]
            [clojure.java.io :refer [resource]]))

(def day 20)

(deftest test-flip-flop
  (let [flip-flop (make-flip-flop "test" ["a" "b"])]
    (is (= nil (receive flip-flop (make-high-pulse "x" "test"))))
    (is (= [(make-high-pulse "test" "a") (make-high-pulse "test" "b")]
           (receive flip-flop (make-low-pulse "x" "test"))))
    (is (= [(make-low-pulse "test" "a") (make-low-pulse "test" "b")]
           (receive flip-flop (make-low-pulse "x" "test"))))
    (is (= [(make-high-pulse "test" "a") (make-high-pulse "test" "b")]
           (receive flip-flop (make-low-pulse "x" "test"))))
    (is (= nil (receive flip-flop (make-high-pulse "x" "test"))))))


(deftest test-conjunction
  (let [conjunction (make-conjunction "test" ["c" "d"] ["a" "b"])]
    (is (= [(make-high-pulse "test" "a") (make-high-pulse "test" "b")]
           (receive conjunction (make-high-pulse "c" "test"))))
    (is (= [(make-low-pulse "test" "a") (make-low-pulse "test" "b")]
           (receive conjunction (make-high-pulse "d" "test"))))
    (is (= [(make-high-pulse "test" "a") (make-high-pulse "test" "b")]
           (receive conjunction (make-low-pulse "d" "test"))))))

(deftest test-broadcaster
  (let [broadcaster (make-broadcaster ["a" "b"])]
    (is (= [(make-high-pulse "broadcaster" "a") (make-high-pulse "broadcaster" "b")]
           (receive broadcaster (make-high-pulse "c" "broadcaster"))))
    (is (= [(make-low-pulse "broadcaster" "a") (make-low-pulse "broadcaster" "b")]
           (receive broadcaster (make-low-pulse "d" "broadcaster"))))))

(deftest test-output
  (let [output (make-output "test")]
    (is (= nil (receive output (make-high-pulse "c" "test"))))
    (is (= nil (receive output (make-low-pulse "d" "test"))))))

(deftest part1-1
  (let [expected 32000000]
    (is (= expected (part-1 (read-file day "example-1"))))))

(deftest part1-2
  (let [expected 11687500]
    (is (= expected (part-1 (read-file day "example-2"))))))

(deftest part2
  (let [expected "PART2_NOT_IMPLEMENTED"]
    (is (= expected (part-2 (read-file day "example-1"))))))
