(ns advent-of-code.day-07-test
  (:require [clojure.test :refer [deftest testing is]]
            [advent-of-code.support :refer [read-file]]
            [advent-of-code.day-07 :refer [part-1 part-2 handle-jokers]]
            [clojure.java.io :refer [resource]]))

(def day 7)

(deftest test-handle-jokers
  (let [check (fn [before expected-after msg]
                (let [after (handle-jokers before)]
                  ;; (prn "before" before)
                  ;; (prn "after" after)
                  ;; (prn "expected-after" expected-after)
                  (is (= after expected-after)
                      (str msg ": is wrong"))))]
    ;; 0
    (check (hash-map \A 1 \K 4)
           (hash-map \A 1 \K 4)
           "no jokers should do nothing")
    ;; 1
    (check (hash-map \X 1 \K 1 \Q 1 \T 1 \9 1)
           (hash-map \K 1 \Q 1 \T 1 \9 2)
           "1 joker, high card should become one pair")
    (check (hash-map \X 1 \Q 1 \T 1 \9 2)
           (hash-map \Q 1 \T 1 \9 3)
           "1 joker, 1 pair should become three-of-kind")
    (check (hash-map \X 1 \T 1 \9 3)
           (hash-map \T 1 \9 4)
           "1 joker, three-of-kind should become four-of-kind")
    (check (hash-map \X 1 \9 4)
           (hash-map \9 5)
           "1 joker, four-of-kind should become five-of-kind")
    (check (hash-map \X 1 \T 2 \9 2)
           (hash-map  \T 2 \9 3)
           "1 joker, 2 pair should become full-house")
    ;;2 
    (check (hash-map \X 2 \Q 1 \T 1 \9 1)
           (hash-map \Q 1 \T 1 \9 3)
           "2 joker, high card should become three-of-kind")
    (check (hash-map \X 2 \T 1 \9 2)
           (hash-map \T 1 \9 4)
           "2 joker, 1 pair should become four-of-kind")
    (check (hash-map \X 2 \9 3)
           (hash-map \9 5)
           "2 joker, three-of-kind should become five-of-kind")
    ;;3
    (check (hash-map \X 3 \T 1 \9 1)
           (hash-map \T 1 \9 4)
           "3 joker, high card should become four-of-kind")
    (check (hash-map \X 3 \9 2)
           (hash-map \9 5)
           "3 joker, 1 pair should become five-of-kind")
    ;;4
    (check (hash-map \X 4 \9 1)
           (hash-map \9 5)
           "5 joker, high card should become five-of-kind")
    ;;5
    (check (hash-map \X 5)
           (hash-map \X 5)
           "5 joker, five-of-kind remains")))

(deftest part1
  (let [expected 6440]
    (is (= expected (part-1 (read-file day "example"))))))

(deftest part2
  (let [expected 5905]
    (is (= expected (part-2 (read-file day "example"))))))
