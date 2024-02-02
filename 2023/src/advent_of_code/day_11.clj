(ns advent-of-code.day-11
  (:require [clojure.string :as str]
            [clojure.set :as set]))

(defn parse-galaxy-locations [input]
  (let [lines (str/split-lines input)]
    (loop [current-line (first lines)
           current-r 0
           remaining-lines (rest lines)
           galaxies []]
      (if (nil? current-line)
        galaxies
        (recur (first remaining-lines)
               (inc current-r)
               (rest remaining-lines)
               (concat galaxies
                       (remove nil?
                               (map-indexed #(when (= \# %2)
                                               [current-r %1])
                                            current-line))))))))

(defn expand-space [expansion-factor galaxies]
  (let [cols (map second galaxies)
        min-col (apply min cols)
        max-col (apply max cols)
        rows (map first galaxies)
        min-row (apply min rows)
        max-row (apply max rows)
        empty-cols (set/difference (set
                                    (range (inc min-col) max-col))
                                   (set cols))
        empty-rows (set/difference (set
                                    (range (inc min-row) max-row))
                                   (set rows))
        expand-galaxy (fn [galaxy]
                        ;; NOTE: we use dec to account for the current row
                        ;; 3 empty gaps with factor of 2 would multipy to 6,
                        ;; but the current dimensions include the original 3, so 
                        ;; dec to remove them for 3 * 1 = 3, which is what should
                        ;; be added.
                        (let [expand-c (* (dec expansion-factor)
                                          (count (filter #(< % (second galaxy)) empty-cols)))
                              expand-r (* (dec expansion-factor)
                                          (count (filter #(< % (first galaxy)) empty-rows)))]
                          [(+ (first galaxy)  expand-r)
                           (+ (second galaxy) expand-c)]))]
    (map expand-galaxy galaxies)))

(defn solve [input expansion-factor]
  (let [galaxies (parse-galaxy-locations input)
        corrected-galaxies (expand-space expansion-factor galaxies)
        indexed-galaxies (map-indexed vector corrected-galaxies)
        distances
        (for [[i1 g1] indexed-galaxies
              [i2 g2] indexed-galaxies
              :let [distance (+ (Math/abs (- (first g1)  (first g2)))
                                (Math/abs (- (second g1) (second g2))))]
              :when (< i1 i2)]
          distance)]
    (reduce + distances)))

(defn part-1
  "Day 11 Part 1"
  [input]
  (solve input 2))

(defn part-2
  "Day 11 Part 2"
  [input & {:keys [expansion-factor] :or {expansion-factor 1000000}}]
  (solve input expansion-factor))
