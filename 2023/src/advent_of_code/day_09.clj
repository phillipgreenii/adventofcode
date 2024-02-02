(ns advent-of-code.day-09
  (:require [clojure.string :as str]))


(defn calc-diffs [numbers]
  (loop [n (first numbers)
         r (rest numbers)
         v []]
    (if (empty? r)
      v
      (recur (first r)
             (rest r)
             (conj v (- (first r) n))))))

(defn extrapolate [histories]
  (let [all-diffs (loop [numbs histories
                         diffs-list [histories]]
                    (if (every? zero? numbs)
                      diffs-list
                      (let [diffs (calc-diffs numbs)]
                        (recur diffs
                               (conj diffs-list diffs)))))]
    (reduce + (map last all-diffs))))

(defn parse-history [line]
  (map #(Integer/parseInt %) (str/split line #" ")))

(defn part-1
  "Day 09 Part 1"
  [input]
  (let [histories (map parse-history (str/split-lines input))
        extrapolated-points (map extrapolate histories)]
    (reduce + extrapolated-points)))

(defn part-2
  "Day 09 Part 2"
  [input]
  (let [histories (map #(reverse (parse-history %)) (str/split-lines input))
       extrapolated-points (map extrapolate histories)]
   (reduce + extrapolated-points)))
