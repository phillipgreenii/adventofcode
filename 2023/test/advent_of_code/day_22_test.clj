(ns advent-of-code.day-22-test
  (:require [clojure.test :refer [deftest testing is]]
            [advent-of-code.support :refer [read-file]]
            [advent-of-code.day-22 :refer [part-1 part-2
                                           make-brick-stack
                                           slice intersects?
                                           squish squish-into squishable?
                                           generate-labels
                                           shift-down]]
            [clojure.java.io :refer [resource]]))

(def day 22)

(deftest test-shift-down
  (let [a (make-brick-stack "a" 1 2 3 1 2 6)
        b (make-brick-stack "a" 1 2 1 1 2 4)]
    (is (identical? a (shift-down a 0)))
    (is (= b (shift-down a 2)))))

(deftest test-slice
  (let [a (make-brick-stack "a" 1 1 1, 1 1 2)
        b (make-brick-stack "b" 1 1 2, 1 1 3)
        c (make-brick-stack "c" 1 1 1, 1 2 1)
        d (make-brick-stack "d" 1 1 2, 2 1 2)
        bs-list  [a b c d]
        expected [[3 [b]]
                  [2 [a b d]]
                  [1 [a c]]]]
    (is (= expected (slice bs-list)))))

(deftest test-intersects
  (let [a (make-brick-stack "a" 1 1 1, 1 1 2)
        b (make-brick-stack "b" 1 1 2, 1 1 3)
        c (make-brick-stack "c" 1 1 1, 1 2 1)
        d (make-brick-stack "d" 1 1 2, 2 1 2)
        bs-list  [a b c d]]
    ; true
    (is (true? (intersects? bs-list
                            a)))
    (is (true? (intersects? bs-list
                            (make-brick-stack "x" 1 1 1, 1 1 1))))
    (is (true? (intersects? bs-list
                            (make-brick-stack "x" 1 1 1, 2 1 1))))
    (is (true? (intersects? bs-list
                            (make-brick-stack "x" 1 1 1, 1 2 1))))
    ; true, but large z because it should be ignored
    (is (true? (intersects? bs-list
                            (make-brick-stack "x" 1 1 9, 1 1 9))))
    (is (true? (intersects? bs-list
                            (make-brick-stack "x" 1 1 9, 2 1 9))))
    (is (true? (intersects? bs-list
                            (make-brick-stack "x" 1 1 9, 1 2 9))))
    ; true, from debugging
    (is (true? (intersects? [(make-brick-stack "a" 1 0 1, 1 2 1)]
                            (shift-down (make-brick-stack "b" 0 0 2, 2 0 2) 1))))
    (is (true? (intersects? [(make-brick-stack "a" 1 0 1, 1 2 1)]
                            (make-brick-stack "b" 0 0 2, 2 0 2))))
    ; false
    (is (false? (intersects? bs-list
                             (make-brick-stack "x" 3 1 1, 3 1 1))))
    (is (false? (intersects? bs-list
                             (make-brick-stack "x" 1 3 1, 1 3 1))))))

(deftest test-squish-into
  (let [a (make-brick-stack "a" 1 1 1, 1 1 1)
        a-2 (make-brick-stack "a" 1 1 2, 1 1 2)
        b (make-brick-stack "b" 3 3 1, 3 3 1)
        b-4 (make-brick-stack "b" 3 3 4, 3 3 4)
        c-2 (make-brick-stack "c" 1 1 2, 1 1 2)
        c-4 (make-brick-stack "c" 1 1 4, 1 1 4)]
    (is (= [a]
           (squish-into nil a))
        "single piece on bottom should do nothing")
    (is (= [a]
           (squish-into nil a-2))
        "single piece will squish to bottom")
    (is (= [a b]
           (squish-into [a] b-4))
        "non-intercepting piece will squish to bottom")
    (is (= [a c-2]
           (squish-into [a] c-2))
        "intercepting piece will not move")
    (is (= [a c-2]
           (squish-into [a] c-4))
        "piece will squish to on top of intercepted piece")
    ; true, from debugging
    (let [ex-a (make-brick-stack "a" 1 0 1, 1 2 1)
          ex-b (make-brick-stack "b" 0 0 2, 2 0 2)]
      (is (= [ex-a ex-b]
             (squish-into [ex-a] ex-b))))))

(deftest test-squish
  (let [a (make-brick-stack "a" 1 1 2, 1 1 2)
        b (make-brick-stack "b" 2 2 3, 2 2 3)
        c (make-brick-stack "c" 3 3 4, 3 3 4)]
    (is (= [(make-brick-stack "a" 1 1 1, 1 1 1)]
           (squish [a]))
        "single piece will squish to bottom")
    (is (= [(make-brick-stack "a" 1 1 1, 1 1 1)
            (make-brick-stack "b" 2 2 1, 2 2 1)
            (make-brick-stack "c" 3 3 1, 3 3 1)]
           (squish [a b c]))
        "non-intersecting brick-stacks will squish to bottom")))

(deftest test-squishable
  (let [a (make-brick-stack "a" 1 1 1, 1 1 1)
        a-2 (make-brick-stack "a" 1 1 2, 1 1 2)
        a-3 (make-brick-stack "a" 1 1 3, 1 1 3)]
    ;false
    (is (false? (squishable? nil))
        "empty is not squishable")
    (is (false? (squishable? [a]))
        "single item at lowest point is not squishable")
    (is (false? (squishable? [a a-2]))
        "fully squished is not squishable")
    ;true
    (is (true? (squishable? [a-2]))
        "single item at not lowest point is squishable")
    (is (true? (squishable? [a a-3]))
        "multiple with gaps is squishable")))

(deftest test-generate-labels
  (let [expected ["A" "B" "C" "D" "E" "F" "G" "H" "I" "J" "K" "L" "M" "N" "O" "P" "Q" "R" "S" "T" "U" "V" "W" "X" "Y" "Z" "AA"]]
    (is (= expected (take 27 (generate-labels))))
    (is (= '() (take 0 (generate-labels))))
    (is (= ["A"] (take 1 (generate-labels))))
    (is (= ["A" "B" "C"] (take 3 (generate-labels))))))

(deftest part1
  (let [expected 5]
    (is (= expected (part-1 (read-file day "example"))))))

(deftest part2
  (let [expected "PART2_NOT_IMPLEMENTED"]
    (is (= expected (part-2 (read-file day "example"))))))
