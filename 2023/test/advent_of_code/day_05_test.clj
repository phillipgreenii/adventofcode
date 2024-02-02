(ns advent-of-code.day-05-test
  (:require [advent-of-code.support :refer [read-file]]
            [advent-of-code.day-05 :refer [cm-lookup
                                           cm-lookup-ranges
                                           cmpp-src-to-dest cmpp-src-range-to-dest-range
                                           new-category-map new-category-mapping
                                           new-range parse-input-as-seed-ranges parse-input-as-single-seeds
                                           part-1 part-2
                                           range-partition range-coalesce]]
            [clojure.data :as data]
            [clojure.test :refer [deftest is]]))

(def day 5)

(deftest test-range-partition
  (let [check (fn [r1 r2 expected-in expected-out msg]
                (let [[r-in r-out] (range-partition r1 r2)
                      ;; in-diff (data/diff expected-in r-in)
                      ;; out-diff (data/diff expected-out r-out)
                      ]
                  ;; (prn "r-in" r-in)
                  ;; (prn "r-out" r-out)
                  (is (= r-in expected-in)
                      (str msg ":'in' is wrong"))
                  ;; (prn "in-diff" (first in-diff) (second in-diff))
                  (is (= r-out expected-out)
                      (str msg ":'out' is wrong"))
                  ;; (prn "out-diff" (first out-diff) (second out-diff))
                  ))]
    (check (new-range 10 5) (new-range 10 5)
           (new-range 10 5) nil
           "r1 equal to r2, so in should be r1 and out should be nil")
    (check (new-range 10 5) (new-range 5 15)
           (new-range 10 5) nil
           "r1 totally in r2, so in should be r1 and out should be nil")
    (check (new-range 10 5) (new-range 12 6)
           (new-range 12 3) (seq [(new-range 10 2)])
           "r1 starts outside of r2 so later part should be in and first part out")
    (check (new-range 15 5) (new-range 12 6)
           (new-range 15 3) (seq [(new-range 18 2)])
           "r1 ends outside of r2 so later part should be out and first part in")
    (check (new-range 15 5) (new-range 12 6)
           (new-range 15 3) (seq [(new-range 18 2)])
           "r1 ends outside of r2 so later part should be out and first part in")
    (check (new-range 15 5) (new-range 25 6)
           nil (seq [(new-range 15 5)])
           "r1 and r2 are disjoint so all of r1 is out")
    (check (new-range 5 15) (new-range 10 5)
           (new-range 10 5) (seq [(new-range 5 5) (new-range 15 5)])
           "r2 inside of r1 so r2 is in and ends of r1 are out")
    (check (new-range 0 100) (new-range 98 2)
           (new-range 98 2) (seq [(new-range 0 98)])
           "from example")))

(deftest test-range-coalesce
  (is (= (range-coalesce (new-range 5 5) (new-range 5 5))
         (seq [(new-range 5 5)]))
      "equal should return equal")
  (is (= (range-coalesce (new-range 5 5) (new-range 15 5))
         (seq [(new-range 5 5) (new-range 15 5)]))
      "disjoint")
  (is (= (range-coalesce (new-range 5 12) (new-range 15 5))
         (seq [(new-range 5 15)]))
      "overlap should merge")
  (is (= (range-coalesce (new-range 5 10) (new-range 15 5))
         (seq [(new-range 5 15)]))
      "side by side should merge"))

(def expected-category-maps
  (hash-map
   "seed-to-soil"
   (new-category-map "seed-to-soil"  [(new-category-mapping 50 98 2)
                                      (new-category-mapping 52 50 48)])
   "soil-to-fertilizer"
   (new-category-map "soil-to-fertilizer"  [(new-category-mapping 0 15 37)
                                            (new-category-mapping 37 52 2)
                                            (new-category-mapping 39 0 15)])
   "fertilizer-to-water"
   (new-category-map "fertilizer-to-water" [(new-category-mapping 49 53 8)
                                            (new-category-mapping 0 11 42)
                                            (new-category-mapping 42 0 7)
                                            (new-category-mapping 57 7 4)])

   "water-to-light"
   (new-category-map "water-to-light" [(new-category-mapping 88 18 7)
                                       (new-category-mapping 18 25 70)])

   "light-to-temperature"
   (new-category-map "light-to-temperature" [(new-category-mapping 45 77 23)
                                             (new-category-mapping 81 45 19)
                                             (new-category-mapping 68 64 13)])

   "temperature-to-humidity"
   (new-category-map "temperature-to-humidity" [(new-category-mapping 0 69 1)
                                                (new-category-mapping 1 0 69)])

   "humidity-to-location"
   (new-category-map "humidity-to-location" [(new-category-mapping 60 56 37)
                                             (new-category-mapping 56 93 4)])))

(deftest test-parse-input-as-single-seeds
  (let [expected-seeds (seq [79 14 55 13])
        [seeds category-maps]  (parse-input-as-single-seeds (read-file day "example"))]
    (is (= expected-seeds seeds))
    (is (= expected-category-maps category-maps))))

(deftest test-parse-input-as-seed-ranges
  (let [expected-seed-ranges (seq [(new-range 79 14)
                                   (new-range 55 13)])
        [seed-ranges  category-maps]  (parse-input-as-seed-ranges (read-file day "example"))]
    (is (= expected-seed-ranges  seed-ranges))
    (is (= expected-category-maps category-maps))))

(deftest  test-cmpp-src-to-dest
  (let [category-mapping (new-category-mapping 100 200 10)]
    (is (= (cmpp-src-to-dest category-mapping 10)
           nil))
    (is (= (cmpp-src-to-dest category-mapping 200)
           100))
    (is (= (cmpp-src-to-dest category-mapping 209)
           109))
    (is (= (cmpp-src-to-dest category-mapping 210)
           nil))))

(deftest test-cmpp-src-range-to-dest-range
  (let [category-mapping (new-category-mapping 100 200 10)
        check (fn [r expected-in expected-out msg]
                (let [[r-in r-out] (cmpp-src-range-to-dest-range category-mapping r)
                      ;; in-diff (data/diff expected-in r-in)
                      ;; out-diff (data/diff expected-out r-out)
                      ]
                  (is (= r-in expected-in)
                      (str msg ":'in' is wrong"))
                  ;; (prn "in-diff" (first in-diff) (second in-diff))
                  (is (= r-out expected-out)
                      (str msg ":'out' is wrong"))
                  ;; (prn "out-diff" (first out-diff) (second out-diff))
                  ))]
    (check (new-range 1 5)
           nil (seq [(new-range 1 5)])
           "disjoint should return range as out")
    (check (new-range 200 5)
           (new-range 100 5) nil
           "range which starts on edge will be shifted")
    (check (new-range 202 2)
           (new-range 102 2) nil
           "range in middle will be shifted")
    (check (new-range 205 5)
           (new-range 105 5) nil
           "range which end on edge will be shifted")
    (check (new-range 195 10)
           (new-range 100 5) (seq [(new-range 195 5)])
           "range starting before should have spill under")
    (check (new-range 205 10)
           (new-range 105 5) (seq [(new-range 210 5)])
           "range ending after should have spill over")
    (check (new-range 195 20)
           (new-range 100 10) (seq [(new-range 195 5) (new-range 210 5)])
           "range larger than map will have end lopped off")))

(deftest test-cmpp-src-range-to-dest-range-2
  (let [category-mapping (new-category-mapping 50 98 2)
        check (fn [r expected-in expected-out msg]
                (let [[r-in r-out] (cmpp-src-range-to-dest-range category-mapping r)
                      ;; in-diff (data/diff expected-in r-in)
                      ;; out-diff (data/diff expected-out r-out)
                      ]
                  ;; (prn "r-in" r-in)
                  ;; (prn "r-out" r-out)
                  (is (= r-in expected-in)
                      (str msg ":'in' is wrong"))
                  ;; (prn "in-diff" (first in-diff) (second in-diff))
                  (is (= r-out expected-out)
                      (str msg ":'out' is wrong"))
                  ;; (prn "out-diff" (first out-diff) (second out-diff))
                  ))]
    (check (new-range 0 100)
           (new-range 50 2) (seq [(new-range 0 98)])
           "from example")))

(deftest test-cm-lookup
  (let [category-map (new-category-map "example"
                                       [(new-category-mapping 50 98 2)
                                        (new-category-mapping 52 50 48)])]
    (is (= (cm-lookup category-map 79)
           81))
    (is (= (cm-lookup category-map 14)
           14))
    (is (= (cm-lookup category-map 55)
           57))
    (is (= (cm-lookup category-map 13)
           13))))

(deftest test-cm-lookup-ranges
  (let [category-map (new-category-map "example"
                                       [(new-category-mapping 50 98 2)
                                        (new-category-mapping 52 50 48)])

        check (fn [ranges  expected-out msg]
                (let [out (cm-lookup-ranges category-map (seq ranges))
                      ;; out-diff (data/diff expected-out out)
                      ]
                  (is (= out (seq expected-out))
                      (str msg " is wrong"))
                  ;; (prn "out" out)
                  ;; (prn "out-diff" (first out-diff)  "|" (second out-diff)  "|" (nth out-diff 2))
                  ))]
    (check [(new-range 95 6)]
           [(new-range 50 2) (new-range 97 3) (new-range 100 1)]
           "range should split and convert")))

(deftest part1
  (let [expected 35]
    (is (= expected (part-1 (read-file day "example"))))))

(deftest part2
  (let [expected 46]
    (is (= expected (part-2 (read-file day "example"))))))
