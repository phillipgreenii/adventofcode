(ns advent-of-code.day-16
  (:require [clojure.set :as set]
            [clojure.string :as str]))

(defn parse-grid [input]
  (vec
   (map vec
        (str/split-lines input))))

(defn energize [grid starting-visit]
  (letfn [(step [[r c] direction]
            (case direction
              \< [[r (dec c)] direction]
              \> [[r (inc c)] direction]
              \^ [[(dec r) c] direction]
              \v [[(inc r) c] direction]))
          (determine-next-visits [point direction]
            (case (get-in grid point nil)
              \. [(step point direction)]
              \\ (case direction
                   \< [(step point \^)]
                   \> [(step point \v)]
                   \v [(step point \>)]
                   \^ [(step point \<)])
              \/ (case direction
                   \< [(step point \v)]
                   \> [(step point \^)]
                   \v [(step point \<)]
                   \^ [(step point \>)])
              \| (if (or (= direction \<)
                         (= direction \>))
                   [(step point \^) (step point \v)]
                   [(step point direction)])
              \-  (if (or (= direction \v)
                          (= direction \^))
                    [(step point \<) (step point \>)]
                    [(step point direction)])
              nil))
          (coalesce-cells [cells]
            (letfn [(convert-cell [[point direction]]
                      (hash-map point (set [direction])))]
              (apply merge-with
                     set/union
                     (map convert-cell
                          cells))))]
    (loop [[current-point current-direction] starting-visit
           energized-cells #{}
           to-visit nil]
      (if (nil? current-point)
        (coalesce-cells energized-cells)
        (let [visit [current-point current-direction]
              been-here-before (contains? energized-cells visit)
              updated-to-visit (if been-here-before
                                 to-visit
                                 (concat to-visit
                                         (determine-next-visits current-point current-direction)))]
          (recur
           (first updated-to-visit)
           (if (or been-here-before
                   (nil? (get-in grid current-point nil)))
             energized-cells
             (conj energized-cells visit))
           (rest updated-to-visit)))))))

(defn part-1
  "Day 16 Part 1"
  [input]
  (let [grid (parse-grid input)
        energized-cells (energize grid [[0 0] \>])]
    (count energized-cells)))

(defn part-2
  "Day 16 Part 2"
  [input]
  (let [grid (parse-grid input)
        max-r (count grid)
        max-c (count (first grid))]
    ;; not optimized, just let it run for each initial position, which took minutes.
    (apply max
           (map-indexed (fn [i c]
                          ;; (prn i c)
                          c)
                        (for [r (range max-r)
                              c (range max-c)
                              d [\< \> \v \^]
                              :let [visit [[r c] d]]
                              :when (or (= r 0) (= r (dec max-r))
                                        (= c 0) (= c (dec max-c)))]
                          (count
                           (energize grid visit)))))))
