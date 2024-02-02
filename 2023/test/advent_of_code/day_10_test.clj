(ns advent-of-code.day-10-test
  (:require [advent-of-code.day-10 :refer [find-edge
                                           find-incoming-connected-neighbors find-loop make-grid
                                           make-pipe-maze part-1 part-2]]
            [clojure.java.io :refer [resource]]
            [advent-of-code.support :refer [read-file]]
            [clojure.string :as str]
            [clojure.test :refer [deftest is]]))


(def day 10)

(deftest test-find-connected-neigbhors
  (let [check (fn [grid [r c] expected-neighbors msg]
                (let [neighbors (find-incoming-connected-neighbors grid [r c])]
                  (is (= neighbors expected-neighbors)
                      (str msg ": is wrong"))))
        grid-1 [[\. \. \.]
                [\. \. \.]
                [\. \. \.]]
        grid-2 [[\7 \| \F]
                [\. \. \.]
                [\L \| \J]]
        grid-3 [[\L \- \J]
                [\. \. \.]
                [\7 \- \F]]
        grid-4 [[\F \. \7]
                [\- \. \-]
                [\L \. \J]]
        grid-5 [[\J \. \L]
                [\| \. \|]
                [\7 \. \F]]]
    (check grid-1 [1 1]
           []
           "all dots should be empty")
    ;; check up/down
    (check grid-2 [1 0]
           [[0 0] [2 0]]
           "include up 7 and down L")
    (check grid-2 [1 1]
           [[0 1] [2 1]]
           "include up | and down |")
    (check grid-2 [1 2]
           [[0 2] [2 2]]
           "include up F and down J")
    (check grid-3 [1 0]
           []
           "exclude up L and down 7")
    (check grid-3 [1 1]
           []
           "exclude up | and down |")
    (check grid-3 [1 2]
           []
           "exclude up J and down F")
    ;; check left/right
    (check grid-4 [0 1]
           [[0 0] [0 2]]
           "include left F and right 7")
    (check grid-4 [1 1]
           [[1 0] [1 2]]
           "include left - and right -")
    (check grid-4 [1 2]
           [[0 2] [2 2]]
           "include left L and right J")
    (check grid-5 [0 1]
           []
           "exclude left J and right L")
    (check grid-5 [1 1]
           []
           "exclude left | and right |")
    (check grid-5 [1 2]
           []
           "exclude left 7 and right F")))


(deftest part1-1
  (let [expected 4]
    (is (= expected (part-1 (read-file day "part1-example-1"))))))

(deftest part1-2
  (let [expected 8]
    (is (= expected (part-1 (read-file day "part1-example-2"))))))

(deftest test-find-edge
  (let [[expected-out expected-in]
        [#{#_()  [0 1] [0 2] [0 3] [0 4] [0 5] [0 6] [0 7] [0 8] [0 9]
           [1 0]                                                       [1 10]
           [2 0]                                                       [2 10]
           [3 0]             [3 3] [3 4] [3 5] [3 6] [3 7]             [3 10]
           [4 0]             [4 3] [4 4] [4 5] [4 6] [4 7]             [4 10]
           [5 0]                         [5 5]                         [5 10]
           [6 0]                         [6 5]                         [6 10]
           [7 0]                         [7 5]                         [7 10]
           #_()  [8 1] [8 2] [8 3] [8 4]       [8 6] [8 7] [8 8] [8 9]}
         #{[6 2] [6 3] [6 7] [6 8]}]
        grid (make-grid (str/split-lines
                         (slurp (resource "day-10-example-1-2.txt"))))
        loop (-> grid make-pipe-maze find-loop)
        [out in] (find-edge grid loop)]
    (is (= expected-out out))
    (is (= expected-in in))))

(deftest part2-1
  (let [expected 4]
    (is (= expected (part-1 (read-file day "part2-example-1"))))))

(deftest part2-2
  (let [expected 4]
    (is (= expected (part-1 (read-file day "part2-example-2"))))))

(deftest part2-3
  (let [expected 8]
    (is (= expected (part-1 (read-file day "part2-example-3"))))))

(deftest part2-4
  (let [expected 10]
    (is (= expected (part-1 (read-file day "part2-example-4"))))))
