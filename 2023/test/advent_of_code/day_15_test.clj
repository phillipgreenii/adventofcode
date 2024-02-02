(ns advent-of-code.day-15-test
  (:require [clojure.test :refer [deftest testing is are]]
            [advent-of-code.support :refer [read-file]]
            [advent-of-code.day-15 :refer [part-1 apply-step-to-box make-step make-slot score-box score-boxes part-2]]
            [clojure.java.io :refer [resource]]))

(def day 15)

(defn make-box [& slot-infos]
  (seq (map #(apply make-slot %) slot-infos)))

(deftest test-apply-step-to-box
  (let [box (make-box ["ab" 3] ["cd" 5] ["ef" 7])]
    (are [expected actual] (= expected actual)
      ;; with nil 
      nil
      (apply-step-to-box nil (make-step "cd" "-" nil))
      (make-box ["cd" 13])
      (apply-step-to-box nil (make-step "cd" "=" 13))
      ;; with box
      (make-box ["ab" 3] ["ef" 7])
      (apply-step-to-box box (make-step "cd" "-" nil))
      (make-box ["ab" 3] ["cd" 13] ["ef" 7])
      (apply-step-to-box box (make-step "cd" "=" 13))
      (make-box ["ab" 3] ["cd" 5] ["ef" 7] ["al" 27])
      (apply-step-to-box box (make-step "al" "=" 27)))))

(deftest test-score-box
  (let [box (make-box ["ab" 3] ["cd" 5] ["ef" 7])]
    (are [expected actual] (= expected actual)
      0 (score-box nil)
      (+ (* 1 3) (* 2 5) (* 3 7)) (score-box box))))

(deftest test-score-boxes
  (let [boxes [(make-box ["rn" 1] ["cm" 2])
               nil
               nil
               (make-box ["ot" 7] ["ab" 5] ["pc" 6])]
        expected (+ 1 4
                    28 40 72)]
    (is (= expected (score-boxes boxes)))))

(deftest part1
  (let [expected 1320]
    (is (= expected (part-1 (read-file day "example"))))))

(deftest part2
  (let [expected 145]
    (is (= expected (part-2 (read-file day "example"))))))
