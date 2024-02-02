(ns advent-of-code.day-03-test
  (:require [clojure.test :refer [deftest testing is]]
            [advent-of-code.support :refer [read-file]]
            [advent-of-code.day-03 :refer [new-sym new-num is-symbol? is-part-number? extract-number-from-row part-1 part-2]]
            [clojure.java.io :refer [resource]]))

(def day 3)

(deftest test-extract-number-from-row
  (doseq [[line expected] [["123456"  [(new-num 123456 1 0 5)]]
                           ["45..56"  [(new-num 45 1 0 1) (new-num 56 1 4 5)]]
                           ["1....."  [(new-num 1 1 0 0)]]
                           ["..2..."  [(new-num 2 1 2 2)]]
                           [".....3"  [(new-num 3 1 5 5)]]
                           ["......"  nil]]]
    (is  (= expected (extract-number-from-row 1 line)))))


(deftest test-is-symbol
  (doseq [[expected c] [[true \#]
                        [true \$]
                        [true \%]
                        [true \+]
                        [true \*]
                        [false nil]
                        [false \.]
                        [false \0]
                        [false \5]
                        [false \9]]]
    (is  (= expected (is-symbol? c))
         (str c " is expected? " expected))))

(deftest test-is-part-number
          ;; grid
          ;; "0.....#4" 
          ;; ".9.7.3.."
          ;; "..$....."
          ;; "..2...8."
          ;; "...5..%."
          ;; "6*.....1"
  (let [syms [(new-sym \# 0 6)
              (new-sym \$ 2 2)
              (new-sym \% 4 6)
              (new-sym \* 5 1)]]
    (doseq [[expected n] [[false (new-num 0 0 0 0)]
                          [true (new-num 1 5 7 7)]
                          [true (new-num 2 3 2 2)]
                          [true (new-num 3 1 5 5)]
                          [true (new-num 4 0 7 7)]
                          [false (new-num 5 4 3 3)]
                          [true (new-num 6 5 0 0)]
                          [true (new-num 7 1 3 3)]
                          [true (new-num 8 3 6 6)]
                          [true (new-num 9 1 1 1)]]]
      (is  (= expected (true? (is-part-number?  n syms)))
           (str n " is expected? " expected)))))

(deftest part1
  (let [expected 4361]
    (is (= expected (part-1 (read-file day "example"))))))

(deftest part2
  (let [expected 467835]
    (is (= expected (part-2 (read-file day "example"))))))
